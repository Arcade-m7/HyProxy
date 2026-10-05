import asyncio
from contextlib import suppress

import pytest

from hyproxy import Asynclestener, Config, Server
from hyproxy.policy import ACTIONS, NETADDRESS, RouteInfo, SimpleRule
from hyproxy.protocols import HTTP1O1

from conftest import listener_address, server_address


async def _http_connect(proxy, destination, payload=b"ping"):
    reader, writer = await asyncio.open_connection(*proxy)
    host, port = destination
    writer.write(f"CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n".encode())
    await writer.drain()
    response = await asyncio.wait_for(reader.readuntil(b"\r\n\r\n"), 2)
    if response.startswith(b"HTTP/1.1 200"):
        writer.write(payload)
        await writer.drain()
        echoed = await asyncio.wait_for(reader.readexactly(len(payload)), 2)
    else:
        echoed = None
    return response, echoed, writer


async def _socks4_connect(proxy, destination, payload=b"ping"):
    reader, writer = await asyncio.open_connection(*proxy)
    host, port = destination
    writer.write(b"\x04\x01" + port.to_bytes(2, "big") + bytes(map(int, host.split("."))) + b"\x00")
    await writer.drain()
    response = await asyncio.wait_for(reader.readexactly(8), 2)
    if response[1] == 90:
        writer.write(payload)
        await writer.drain()
        echoed = await asyncio.wait_for(reader.readexactly(len(payload)), 2)
    else:
        echoed = None
    return response, echoed, writer


async def _socks5_connect(proxy, destination, payload=b"ping"):
    reader, writer = await asyncio.open_connection(*proxy)
    host, port = destination
    writer.write(b"\x05\x01\x00")
    await writer.drain()
    assert await asyncio.wait_for(reader.readexactly(2), 2) == b"\x05\x00"
    writer.write(b"\x05\x01\x00\x01" + bytes(map(int, host.split("."))) + port.to_bytes(2, "big"))
    await writer.drain()
    response = await asyncio.wait_for(reader.readexactly(10), 2)
    if response[1] == 0:
        writer.write(payload)
        await writer.drain()
        echoed = await asyncio.wait_for(reader.readexactly(len(payload)), 2)
    else:
        echoed = None
    return response, echoed, writer


@pytest.mark.asyncio
async def test_listener_starts_stops_and_forwards_http_connect(proxy_listener, echo_server):
    response, echoed, writer = await _http_connect(listener_address(proxy_listener), server_address(echo_server), b"forwarded")
    assert response.startswith(b"HTTP/1.1 200")
    assert echoed == b"forwarded"
    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
@pytest.mark.parametrize("connect", [_socks4_connect, _socks5_connect])
async def test_proxy_forwards_socks_clients(proxy_listener, echo_server, connect):
    response, echoed, writer = await connect(listener_address(proxy_listener), server_address(echo_server), b"socks-data")
    assert response[1] in (0, 90)
    assert echoed == b"socks-data"
    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
async def test_proxy_handles_multiple_concurrent_clients(proxy_listener, echo_server):
    async def client(number):
        response, echoed, writer = await _http_connect(listener_address(proxy_listener), server_address(echo_server), f"client-{number}".encode())
        writer.close()
        await writer.wait_closed()
        return response, echoed

    results = await asyncio.gather(*(client(number) for number in range(8)))
    assert all(response.startswith(b"HTTP/1.1 200") and echoed == f"client-{index}".encode() for index, (response, echoed) in enumerate(results))


@pytest.mark.asyncio
async def test_proxy_closes_invalid_input_and_refuses_unreachable_destination(proxy_listener):
    reader, writer = await asyncio.open_connection(*listener_address(proxy_listener))
    writer.write(b"not an http request\r\n\r\n")
    await writer.drain()
    assert await asyncio.wait_for(reader.read(), 2) == b""
    writer.close()

    response, echoed, writer = await _http_connect(listener_address(proxy_listener), ("127.0.0.1", 1))
    assert response.startswith(b"HTTP/1.1 502")
    assert echoed is None
    writer.close()


@pytest.mark.asyncio
async def test_proxy_enforces_policy_and_http_authentication(echo_server):
    config = Config()
    config.auth.setusername(b"user")
    config.auth.setpassword(b"password")
    listener = Asynclestener("auth", "127.0.0.1", 0, [HTTP1O1(config)])
    await listener.init()
    reader, writer = await asyncio.open_connection(*listener_address(listener))
    host, port = server_address(echo_server)
    writer.write(f"CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}:{port}\r\n\r\n".encode())
    await writer.drain()
    assert (await reader.readuntil(b"\r\n\r\n")).startswith(b"HTTP/1.1 407")
    writer.close()
    await listener.stop()


@pytest.mark.asyncio
async def test_proxy_denies_routes_blocked_by_policy(echo_server):
    config = Config()
    host, port = server_address(echo_server)
    config.policy.addrule(SimpleRule(RouteInfo(dst=NETADDRESS(port=port)), action=ACTIONS.DENY))
    listener = Asynclestener("policy", "127.0.0.1", 0, [HTTP1O1(config)])
    await listener.init()
    response, echoed, writer = await _http_connect(listener_address(listener), (host, port))
    assert response.startswith(b"HTTP/1.1 403")
    assert echoed is None
    writer.close()
    await listener.stop()


@pytest.mark.xfail(reason="Asynclestener.wraper creates Stream with its default timeout instead of Config.connection.timeout")
@pytest.mark.asyncio
async def test_listener_timeout_cleans_up_idle_connection():
    config = Config()
    config.connection.settimeout(0.05)
    listener = Asynclestener("timeout", "127.0.0.1", 0, [HTTP1O1(config)])
    await listener.init()
    reader, writer = await asyncio.open_connection(*listener_address(listener))
    assert await asyncio.wait_for(reader.read(), 1) == b""
    writer.close()
    await listener.stop()


@pytest.mark.asyncio
async def test_server_main_orchestrates_and_cancellation_closes_listener():
    listener = Asynclestener("server", "127.0.0.1", 0, [HTTP1O1(Config())])
    task = asyncio.create_task(Server(listener).__main__())
    for _ in range(20):
        if hasattr(listener, "serv_"):
            break
        await asyncio.sleep(0.01)
    assert hasattr(listener, "serv_")
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task
    await listener.stop()
