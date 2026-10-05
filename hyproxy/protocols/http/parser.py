from io import BytesIO
from re import match

class REQUEST:

    def __init__(self, method: bytes, requesturi: bytes, version: bytes, headers: dict = {}, body: bytes = b""):
        """
        Construct a `REQUEST` object and validate the request URI format.
        params:
            method : bytes : HTTP method token
            requesturi : bytes : request URI or absolute URI
            version : bytes : HTTP version string
            headers : dict : mapping of header bytes to bytes
            body : bytes : optional body
        returns:
            None
        errors:
            ValueError : if requesturi is invalid
        """
        self.method = method
        if match(r"(^https?://)?((([A-Za-z0-9-]+\.)+[A-Za-z]{2,})|((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)|localhost)(:\d{1,5})?([/?#][^\s]*)?$".encode(), requesturi):
            self.requesturi = requesturi
        else:
            raise ValueError("Invalid request URI")
        self.version = version
        self.headers = headers
        self.body = body

    def compose(self):
        """
        Serialize the `REQUEST` object into raw HTTP bytes.
        params:
            None
        returns:
            bytes : serialized HTTP request
        errors:
            Exception : on serialization failure
        """
        request = self.method + b" " + self.requesturi + b" " + self.version + b"\r\n"
        for key, value in self.headers.items():
            request += key + b": " + value + b"\r\n"
        request += b"\r\n" + self.body
        return request

    @staticmethod
    def HTTPParser(content: bytes):
        """
        Parse raw HTTP request bytes and return a `REQUEST` instance.
        params:
            content : bytes : raw HTTP bytes
        returns:
            REQUEST : parsed request object
        errors:
            Exception : if parsing fails
        """
        content = BytesIO(content) ; headers = {} ; body = b""
        method, requesturi, version = content.readline().strip().split()
        while (line:=content.readline().strip()):
            key, value = line.split(b":",1)
            headers[key.strip()] = value.strip()
        body = content.read()
        return REQUEST(method, requesturi, version, headers, body)
    
class RESPONSE:

    def __init__(self, version: bytes, status_code: bytes, reason_phrase: bytes = b"", headers: dict = {}, body: bytes = b""):
        """
        Construct a `RESPONSE` object representing an HTTP response.
        params:
            version : bytes : HTTP version
            status_code : bytes : HTTP status code
            reason_phrase : bytes : reason phrase
            headers : dict : headers mapping
            body : bytes : optional body
        returns:
            None
        errors:
            None
        """
        self.version = version
        self.status_code = status_code
        self.reason_phrase = reason_phrase
        self.headers = headers
        self.body = body

    def compose(self):
        """
        Serialize the `RESPONSE` object into raw HTTP bytes.
        params:
            None
        returns:
            bytes : serialized HTTP response
        errors:
            Exception : on serialization failure
        """
        response = self.version + b" " + self.status_code + b" " + self.reason_phrase + b"\r\n"
        for key, value in self.headers.items():
            response += key + b": " + value + b"\r\n"
        response += b"\r\n" + self.body
        return response
    
    @staticmethod
    def HTTPParser(content: bytes):
        """
        Parse raw HTTP response bytes and return a `RESPONSE` instance.
        params:
            content : bytes : raw HTTP response bytes
        returns:
            RESPONSE : parsed response object
        errors:
            Exception : if parsing fails
        """
        content = BytesIO(content) ; headers = {} ; body = b""
        version, status_code, reason_phrase = content.readline().strip().split(b" ",2)
        while (line:=content.readline().strip()):
            key, value = line.split(b":",1)
            headers[key.strip()] = value.strip()
        body = content.read()
        return RESPONSE(version, status_code, reason_phrase, headers, body)