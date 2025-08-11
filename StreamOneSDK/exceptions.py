
class StreamOneIONSDKException(Exception):
    """
    Base exception for all StreamOneIONSDK errors.
    """

    def __init__(self, message=None):
        if message is None:
            message = "An error occurred in the StreamOneIONSDK."
        super().__init__(message)


class AuthenticationError(StreamOneIONSDKException):
    """
    Raised when authentication fails (e.g., invalid credentials or expired token).
    """

    def __init__(self, message=None):
        if message is None:
            message = "Authentication failed. Please check your credentials."
        super().__init__(message)


class AuthorizationError(StreamOneIONSDKException):
    """
    Raised when the user does not have permission to perform an action.
    """

    def __init__(self, message=None):
        if message is None:
            message = "You are not authorized to perform this action."
        super().__init__(message)


class NotFoundError(StreamOneIONSDKException):
    """
    Raised when a requested resource is not found.
    """

    def __init__(self, message=None):
        if message is None:
            message = "The requested resource was not found."
        super().__init__(message)


class ServerError(StreamOneIONSDKException):
    """
    Raised when a server-side error occurs (HTTP 5xx).
    """

    def __init__(self, message=None):
        if message is None:
            message = "A server error occurred. Please try again later."
        super().__init__(message)


class BadRequestError(StreamOneIONSDKException):
    """
    Raised when a request is malformed or invalid (HTTP 400).
    """

    def __init__(self, message=None):
        if message is None:
            message = "The request was invalid or cannot be processed."
        super().__init__(message)
