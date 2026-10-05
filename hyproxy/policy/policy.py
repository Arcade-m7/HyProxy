from .rules import SimpleRule
from .models import RouteInfo

class Policy:
    """Policy engine for proxy tunnel filtering.

    The Policy object holds a list of SimpleRule instances and evaluates
    whether a connection is allowed.

    - `rules` is a list of SimpleRule objects.
    - `__call__` returns False if any rule matches (deny) else True (allow).
    """

    def __init__(self,rules: list[SimpleRule] = []):
        """
        params:
            rules : list[SimpleRule] : list of simple rules for the policy
        returns:
            None
        errors:
            AssertionError : if rules is not a list
        """
        assert type(rules) is list

        if rules:
            rules = []
        self.rules = rules

    def __call__(self, info: RouteInfo):
        """Evaluate tunnel permission.

        Returns False if any rule blocks the pipe, otherwise True.

        `info` is a `RouteInfo(src, dst)` worth evaluation.
        """
        for rule in self.rules:
            if rule(info) :
                return bool(rule.action.value)
        return True

    def addrule(self,rule:SimpleRule):
        """Add a rule to policy."""
        if not isinstance(rule,SimpleRule):
            raise ValueError(f'rule must be SimpleRule class')
        self.rules.append(rule)

    def poprule(self,*args):
        """Remove and return rule by index."""
        return self.rules.pop(*args)
    
    def showrules(self):
        return self.rules
        
