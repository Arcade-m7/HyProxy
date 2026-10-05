import pytest

from hyproxy.policy import ACTIONS, NETADDRESS, Policy, RouteInfo, SimpleRule
from hyproxy.policy.models import DOMAIN, IP, PORT, Wip, isip


@pytest.mark.parametrize("value, expected", [("127.0.0.1", True), ("10.0.0.0/8", True), ("bad-host", False)])
def test_ip_helpers_validate_and_wrap_addresses(value, expected):
    assert isip(value) is expected
    assert bool(Wip(value)) is expected


def test_address_value_objects_match_addresses_networks_domains_and_ports():
    assert IP("127.0.0.1") == IP("127.0.0.1")
    assert IP("127.0.0.0/24") == IP("127.0.0.42")
    assert DOMAIN(r".*\\.example\\.com") == DOMAIN("api.example.com")
    assert PORT(range(80, 82)) == 80
    assert PORT(443) == 443
    assert str(PORT(443)) == "443"


def test_netaddress_and_route_info_support_partial_matching():
    rule = RouteInfo(dst=NETADDRESS(ip="127.0.0.0/24", port=range(8000, 9000)))
    request = RouteInfo(src=NETADDRESS(ip="127.0.0.1", port=1), dst=NETADDRESS(ip="127.0.0.5", port=8080))
    assert rule == request
    assert "RouteInfo" in repr(request)
    address = NETADDRESS()
    address.SetIP("127.0.0.1")
    address.SetDomain("localhost")
    assert str(address.ip) == "127.0.0.1"
    with pytest.raises(ValueError):
        NETADDRESS(ip="not-an-ip")
    with pytest.raises(AssertionError):
        NETADDRESS(port="80")


def test_policy_respects_first_matching_rule_and_supports_mutation():
    policy = Policy()
    deny = SimpleRule(RouteInfo(dst=NETADDRESS(port=25)), "block smtp", ACTIONS.DENY)
    allow = SimpleRule(RouteInfo(dst=NETADDRESS(port=443)), "allow https", ACTIONS.ALLOW)
    policy.addrule(deny)
    policy.addrule(allow)
    assert policy(RouteInfo(dst=NETADDRESS(port=25))) is False
    assert policy(RouteInfo(dst=NETADDRESS(port=443))) is True
    assert policy(RouteInfo(dst=NETADDRESS(port=22))) is True
    assert policy.poprule(0) is deny
    assert policy.showrules() == [allow]
    with pytest.raises(ValueError):
        policy.addrule("not a rule")


@pytest.mark.xfail(reason="Policy currently discards a non-empty constructor rules list")
def test_policy_constructor_preserves_rules():
    rule = SimpleRule(RouteInfo(dst=NETADDRESS(port=25)))
    assert Policy([rule]).showrules() == [rule]
