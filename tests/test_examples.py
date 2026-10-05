"""Smoke-test reusable configuration helpers from the documented examples."""

import importlib.util
from pathlib import Path

import pytest


EXAMPLES = Path(__file__).parents[1] / "examples"


def load_example(relative_path):
    path = EXAMPLES / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_policy_rules_example_builds_the_documented_ordered_policy():
    example = load_example("config_policy/02_simple_rules.py")
    config = example.build_config()
    names = [rule.name for rule in config.policy.showrules()]
    assert names == [
        "Block www.example.com",
        "Allow HTTPS",
        "Allow HTTP",
        "Allow DNS",
        "Deny everything else",
    ]


@pytest.mark.parametrize(
    ("factory", "timeout", "connections"),
    [
        ("create_fast_config", 30, 5000),
        ("create_stable_config", 60, 1000),
        ("create_resilient_config", 120, 500),
    ],
)
def test_socket_configuration_examples_create_their_advertised_settings(factory, timeout, connections):
    example = load_example("config_sock/03_timeouts_limits.py")
    config = getattr(example, factory)()
    assert config.connection.timeout == timeout
    assert config.connection.max_connections == connections


@pytest.mark.parametrize(
    ("factory", "servers", "ttl"),
    [
        ("internal_network_config", ["192.168.1.1", "192.168.1.2"], 300),
        ("privacy_focused_config", ["1.1.1.1", "9.9.9.9"], 180),
        ("performance_focused_config", ["8.8.8.8", "8.8.4.4"], 3600),
    ],
)
def test_dns_configuration_examples_apply_their_documented_globals(factory, servers, ttl):
    example = load_example("utills_dns/03_advanced_config.py")
    from hyproxy.utills.dns import DNS

    try:
        getattr(example, factory)()
        assert DNS.nameservers == servers
        assert DNS.TTL == ttl
    finally:
        DNS.nameservers = ["8.8.8.8", "1.1.1.1"]
        DNS.TTL = 180
