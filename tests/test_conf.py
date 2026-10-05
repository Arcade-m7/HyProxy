import asyncio
import io
import logging

import pytest

from hyproxy import Config
from hyproxy.conf.auth import __auth__
from hyproxy.conf.cmd import __cmd__, bind, connect, udp
from hyproxy.conf.log import StreamOutput, __log__
from hyproxy.conf.sock import __connection__, base, ipv4, ipv6
from hyproxy.net.const import CONNECTIONINFO


@pytest.mark.parametrize("command", [connect, bind, udp])
def test_command_toggles(command):
    value = command()
    assert value.isenabled is True
    value.desible()
    assert value.isenabled is False
    value.enable()
    assert value.isenabled is True


def test_command_container_reports_known_and_unknown_options():
    commands = __cmd__()
    assert [commands.get(option) for option in (1, 2, 3)] == [True, True, True]
    commands.connect.desible()
    assert commands.get(1) is False
    assert commands.get(99) is False


def test_auth_requires_bytes_and_has_readable_representation():
    auth = __auth__()
    auth.setusername(b"user")
    auth.setpassword(b"secret")
    assert repr(auth) == "Auth(username=b'user', password=b'secret')"
    with pytest.raises(AssertionError):
        auth.setusername("user")
    with pytest.raises(AssertionError):
        auth.setpassword("secret")


def test_connection_settings_and_feature_toggles():
    feature = base()
    feature.disable()
    assert feature.isenabled is False
    feature.enable()
    assert feature.isenabled is True
    assert ipv4().isenabled is True
    assert ipv6().isenabled is False

    connection = __connection__()
    connection.settimeout(1.5)
    connection.setmaxconnections(2)
    assert connection.timeout == 1.5
    assert connection.sameas is not None
    connection.setmaxconnections(None)
    assert connection.sameas is None
    with pytest.raises(AssertionError):
        connection.settimeout("fast")
    with pytest.raises(AssertionError):
        connection.setmaxconnections("two")


def test_config_callbacks_and_defaults():
    config = Config()
    callback = lambda *_: None
    config.setprivatemethod(callback)
    config.setmitm(callback)
    assert config.privatemethod is callback
    assert config.mitm is callback
    with pytest.raises(ValueError):
        config.setprivatemethod(None)
    with pytest.raises(ValueError):
        config.setmitm(None)


def test_log_format_and_stream_handler_lifecycle():
    logger = __log__("pytest-log", logging.INFO)
    record = CONNECTIONINFO("id", 1, 2, "listener", "HTTP", "src", "dst", 3, 4)
    assert "UUID=id" in logger.format(record)

    output = StreamOutput(logger, io.StringIO())
    output.enable()
    assert output in logger.handlers
    output.disable()
    assert output not in logger.handlers
    logger.stream.disable()
