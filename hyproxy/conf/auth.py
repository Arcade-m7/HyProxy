class __auth__:

    def __init__(self):
        """
        Create an authentication container holding username and password.
        params:
            None
        returns:
            None
        errors:
            None
        """
        self.username = None
        self.password = None

    def __repr__(self):
        """
        Return a readable string representing the authentication values.
        params:
            None
        returns:
            str : string representation of auth object
        errors:
            None
        """
        return f"Auth(username={self.username}, password={self.password})"

    def setusername(self,username: bytes):
        """
        Set the username to the provided bytes value.
        params:
            username : bytes : username in bytes
        returns:
            None
        errors:
            AssertionError : if username is not bytes
        """
        assert type(username) is bytes
        self.username = username

    def setpassword(self,password: bytes):
        """
        Set the password to the provided bytes value.
        params:
            password : bytes : password in bytes
        returns:
            None
        errors:
            AssertionError : if password is not bytes
        """
        assert type(password) is bytes
        self.password = password
