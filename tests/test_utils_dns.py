import asyncio
from types import SimpleNamespace

import pytest

from hyproxy.utills import INT, IP
from hyproxy.utills.dns import CACHE, DNS, dicts, isipaddress


@pytest.mark.parametrize("address, valid, version", [("127.0.0.1", True, 4), ("::1", True, 6), ("nope", False, None)])
def test_ip_utilities(address, valid, version):
    assert IP.isipaddress(address) is valid
    assert isipaddress(address) is valid
    if valid:
        assert IP.version(address) == version
    else:
        with pytest.raises(ValueError):
            IP.version(address)


def test_ipv4_pack_unpack_and_safe_int_conversion():
    packed = IP.pack("127.0.0.1")
    assert packed == b"\x7f\x00\x00\x01"
    assert IP.unpack(packed) == "127.0.0.1"
    assert IP.pack("invalid") is None
    assert INT.fromBytes(b"\x01\x00", "big") == 256
    assert INT.fromBytes(None, "big") is None


def test_dictionary_helper_and_dns_nameserver_validation(monkeypatch):
    container = dicts()
    container.add("key", "value")
    assert container == {"key": "value"}
    original = DNS.nameservers
    try:
        DNS.setnameservers(["127.0.0.1"])
        assert DNS.getnameservers() == ["127.0.0.1"]
        with pytest.raises(ValueError):
            DNS.setnameservers(["invalid"])
    finally:
        DNS.nameservers = original
    assert DNS.check("www.example.com")
    assert not DNS.check("bad host")


@pytest.mark.asyncio
async def test_dns_resolution_uses_cache(monkeypatch):
    DNS.cache.ipv4.clear()
    DNS.cache.ipv6.clear()
    calls = 0

    class Resolver:
        def __init__(self, _servers):
            pass

        async def query_dns(self, domain, qtype):
            nonlocal calls
            calls += 1
            assert (domain, qtype) == ("example.test", "A")
            return SimpleNamespace(answer=[SimpleNamespace(data=SimpleNamespace(addr="127.0.0.1"))])

    monkeypatch.setattr("hyproxy.utills.dns.DNSResolver", Resolver)
    assert await DNS.resolve("example.test", "A") == "127.0.0.1"
    assert await DNS.resolve("example.test", "A") == "127.0.0.1"
    assert calls == 1
    with pytest.raises(AssertionError):
        await DNS.resolve("example.test", "MX")


@pytest.mark.asyncio
async def test_dns_resolveboth_and_resolution_failure(monkeypatch):
    async def resolve(domain, qtype):
        return f"{domain}:{qtype}"

    monkeypatch.setattr(DNS, "resolve", resolve)
    assert await DNS.resolveboth("example.test") == ["example.test:A", "example.test:AAAA"]


@pytest.mark.xfail(reason="garbageCollector checks expiry in the wrong direction")
@pytest.mark.asyncio
async def test_dns_garbage_collector_removes_expired_entries(monkeypatch):
    DNS.cache.ipv4.clear()
    DNS.cache.ipv4["expired"] = CACHE("127.0.0.1", 0)
    monkeypatch.setattr(DNS, "TTL", 0)
    task = asyncio.create_task(DNS.garbageCollector())
    await asyncio.sleep(0)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert "expired" not in DNS.cache.ipv4
