class connect:

    def __init__(self):
        """
        Initialize the `connect` command as enabled by default.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.isenabled = True
    
    def enable(self):
        """
        Enable the command.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.isenabled = True

    def desible(self):
        """
        Disable the command.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.isenabled = False

class bind:

    def __init__(self):
        """
        Initialize the `bind` command as enabled by default.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.isenabled = True

    def enable(self):
        """
        Enable the command.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.isenabled = True

    def desible(self):
        """
        Disable the command.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.isenabled = False

class udp:

    def __init__(self):
        """
        Initialize the `udp` command as enabled by default.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.isenabled = True

    def enable(self):
        """
        Enable the command.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.isenabled = True

    def desible(self):
        """
        Disable the command.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.isenabled = False
    
class __cmd__:

    def __init__(self):
        """
        Initialize the command set container with default command objects.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.connect = connect()
        self.bind = bind()
        self.udp = udp()

    def get(self,option: int):
        """
        Return whether the requested command option is enabled.
        params:
            option : int : option number (1=connect,2=bind,3=udp)
        returns:
            bool : whether the requested command is enabled
        errors:
            None
        """
        match option:
            case 1:
                return self.connect.isenabled
            
            case 2:
                return self.bind.isenabled
            
            case 3:
                return self.udp.isenabled
        
            case _:
                return False