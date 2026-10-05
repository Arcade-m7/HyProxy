from .models import ACTIONS, RouteInfo

class SimpleRule:
    """Simple rule wrapper for a single pipeline match.

    The rule is deny-oriented when `rule` is RULES.DENY.
    Comparing `pipe` equality triggers rule acceptance.
    """
    def __init__(
            self,
            tunnel: RouteInfo,
            name: str = None,
            action: int = ACTIONS.DENY
        ):
        """
        Initialize a rule for route matching.
        params:
            tunnel : RouteInfo : the route info to match against
            action : int : the rule type (allow or deny)
            name : str : the name of the rule
        returns:
            None
        errors:
            Exception : general error during initialization
        """
        self.tunnel = tunnel
        self.action = action
        self.name = name

    def __call__(self, tunnel: RouteInfo):
        """
        Evaluate if the given tunnel matches this rule.
        params:
            tunnel : RouteInfo : the route info to check against the rule
        returns:
            bool : whether the rule matches the tunnel
        errors:
            Exception : general error during rule evaluation
        """
        return self.tunnel == tunnel
    
    def __repr__(self):
        return f"SimpleRule(name={self.name} ,tunnel={self.tunnel}, action={self.action})"
    

__all__ = [
    'SimpleRule'
]