"""Shared fixtures and small wire-protocol helpers for HyProxy tests."""

import asyncio
from contextlib import suppress

import pytest_asyncio

from hyproxy import Asynclestener, Config
from hyproxy.protocols import HTTP1O1, SOCKS4, SOCKS5


@pytest_asyncio.fixture
async def echo_server():
    """A real TCP echo target used by proxy integration tests."""
    async def echo(reader, writer):
        try:
            while data := await reader.read(65536):
                writer.write(data)
                await writer.drain()
        finally:
            writer.close()
            with suppress(Exception):
                await writer.wait_closed()

    server = await asyncio.start_server(echo, "127.0.0.1", 0)
    yield server
    server.close()
    await server.wait_closed()


@pytest_asyncio.fixture
async def proxy_listener():
    """Start an ephemeral listener configured like the mixed-protocol example."""
    config = Config()
    listener = Asynclestener(
        name="pytest-proxy",
        ip="127.0.0.1",
        port=0,
        protocols=[HTTP1O1(config), SOCKS4(config), SOCKS5(config)],
    )
    await listener.init()
    yield listener
    await listener.stop()


def listener_address(listener):
    return listener.serv_.sockets[0].getsockname()[:2]


def server_address(server):
    return server.sockets[0].getsockname()[:2]
