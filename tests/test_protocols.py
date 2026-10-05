import asyncio

import pytest

from hyproxy import Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5
from hyproxy.protocols.base import BaseProtocol
from hyproxy.protocols.http.parser import REQUEST, RESPONSE


def test_http_request_response_parser_round_trip_and_invalid_uri():
    request = REQUEST(b"GET", b"http://127.0.0.1:8080/path", b"HTTP/1.1", {b"X-Test": b"yes"}, b"body")
    assert REQUEST.HTTPParser(request.compose()).body == b"body"
    response = RESPONSE(b"HTTP/1.1", b"200", b"OK", {b"Content-Length": b"2"}, b"ok")
    assert RESPONSE.HTTPParser(response.compose()).status_code == b"200"
    with pytest.raises(ValueError):
        REQUEST(b"GET", b"not a valid uri", b"HTTP/1.1")


def test_protocol_configuration_and_address_type_validation():
    config = Config()
    socks4, socks5, http = SOCKS4(config), SOCKS5(config), HTTP1O1(config)
    assert str(socks4) == "SOCKS4"
    assert str(socks5) == "SOCKS5"
    assert str(http) == "HTTP"
    assert socks5.atyp(1, "127.0.0.1") is True
    assert socks5.atyp(4, "::1") is False
    assert socks5.atyp(3, "www.example.com") is True


@pytest.mark.asyncio
async def test_base_protocol_dns_fallback_respects_configuration(monkeypatch):
    config = Config()
    protocol = BaseProtocol(config)

    async def resolve(domain, qtype):
        return {"A": "127.0.0.1", "AAAA": "::1"}[qtype]

    monkeypatch.setattr("hyproxy.protocols.base.Utils.dns.resolve", resolve)
    assert await protocol.dns("example.com", 4) == "127.0.0.1"
    assert await protocol.dnsrb("example.com") == "127.0.0.1"
    assert await protocol.dnsrb("bad host") is None


@pytest.mark.asyncio
async def test_connection_limit_serializes_protocol_reply():
    config = Config()
    config.connection.setmaxconnections(1)
    entered = asyncio.Event()
    release = asyncio.Event()

    class Protocol(BaseProtocol):
        async def rreply(self, value):
            entered.set()
            await release.wait()
            return value

    protocol = Protocol(config)
    first = asyncio.create_task(protocol.reply("first"))
    await entered.wait()
    second = asyncio.create_task(protocol.reply("second"))
    await asyncio.sleep(0)
    assert not second.done()
    release.set()
    assert await first == "first"
    assert await second == "second"
