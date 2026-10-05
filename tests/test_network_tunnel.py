import asyncio
from contextlib import suppress

import pytest

from hyproxy import Config
from hyproxy.net.const import ConnectionInfo
from hyproxy.net.network import BytesParser, Stream, forwardfunction
from hyproxy.net.tunnel import Tunnel
from hyproxy.server.serv import PROTOCOLES, randid


@pytest.mark.parametrize("payload, protocol", [(b"\x04", "SOCKS4"), (b"\x05", "SOCKS5"), (b"GET /", "HTTP"), (b"", "HTTP")])
def test_protocol_detector(payload, protocol):
    assert BytesParser(payload) == protocol


def test_listener_protocol_registry_and_random_identifier():
    identifier = randid()
    assert len(identifier) == 12 and set(identifier) <= set("0123456789ABCDEF")
    registry = PROTOCOLES.add([str, bytes])
    assert registry == [("<class 'str'>", str), ("<class 'bytes'>", bytes)]
    with pytest.raises(AssertionError):
        PROTOCOLES.add((str,))


@pytest.mark.asyncio
async def test_stream_send_receive_counters_timeout_and_close():
    received = asyncio.Event()

    async def target(reader, writer):
        data = await reader.read(100)
        received.set()
        writer.write(data.upper())
        await writer.drain()
        writer.close()

    server = await asyncio.start_server(target, "127.0.0.1", 0)
    host, port = server.sockets[0].getsockname()[:2]
    reader, writer = await asyncio.open_connection(host, port)
    stream = Stream(reader, writer, timeout=1)
    assert await stream.sendbuffer(b"hello") is None
    error, data = await stream.recvbuffer()
    assert error is None and data == b"HELLO"
    assert stream.datasent() == 5 and stream.datarecv() == 5
    stream.settimeout(0.1)
    assert stream.gettimeout() == 0.1
    with pytest.raises(ValueError):
        stream.settimeout("slow")
    stream.close()
    await stream.wait_closed()
    server.close()
    await server.wait_closed()


@pytest.mark.asyncio
async def test_tunnel_link_call_forward_and_connection_record(echo_server):
    host, port = echo_server.sockets[0].getsockname()[:2]
    captured = []

    async def client_handler(reader, writer):
        source = Stream(reader, writer, timeout=1)
        config = Config()
        config.call = lambda tunnel, timeout: forwardfunction(tunnel, timeout)
        tunnel = Tunnel.tunnel(source, config, "TEST", "listener")
        assert await tunnel.link(host, port) is None
        await tunnel.call(1)
        captured.append(tunnel.history.record())

    server = await asyncio.start_server(client_handler, "127.0.0.1", 0)
    proxy_host, proxy_port = server.sockets[0].getsockname()[:2]
    reader, writer = await asyncio.open_connection(proxy_host, proxy_port)
    writer.write(b"through-tunnel")
    await writer.drain()
    assert await asyncio.wait_for(reader.readexactly(14), 2) == b"through-tunnel"
    writer.close()
    await writer.wait_closed()
    await asyncio.sleep(0)
    server.close()
    await server.wait_closed()
    assert captured and captured[0].protocol == "TEST"
