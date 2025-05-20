class StreamOneSDKException(Exception):
    pass

class AuthenticationError(StreamOneSDKException):
    pass

class AuthorizationError(StreamOneSDKException):
    pass

class NotFoundError(StreamOneSDKException):
    pass

class ServerError(StreamOneSDKException):
    pass

class BadRequestError(StreamOneSDKException):
    pass