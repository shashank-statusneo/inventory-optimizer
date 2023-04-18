"""custom exception class to replace flask abort.
flask abort catches under error handler and modifies the response"""

import random
from enum import Enum

DEFAULT_MESSAGES = [
    "Psst This is unexpected! Please Contact Dev Support.",
    "Oh we're sorry for this. Please Contact Dev Support.",
    "Something unusual happened. Please Contact Dev Support.",
    "This should not have happened. Please Contact Dev Support.",
]

# ! All used HTTP ERROR CODES should be mentioned here
HTTP_CODES = {
    400: "Request body can not be correctly processed",
    401: "Invalid Authorization",
    403: "Access Forbidden",
    500: "Something Went Wrong !!",
}


class StarterKitExceptions(Enum):
    """
    * all custom exceptions with their respective internal codes.
    ! if adding new exception make sure to list it here.
    """

    # * system generated error codes. dont interfere with these
    UnknownErrorCodeException = "STRKIT001"
    DuplicateErrorCodeException = "STRKIT002"
    UnknownHttpCodeException = "STRKIT003"
    InternalServerErrorException = "STRKIT004"
    DatabaseErrorException = "STRKIT005"
    CustomException = "STRKIT006"
    AuthorizationException = "STRKIT007"

    # * code level errors
    InvalidRequestBodyException = "STRKIT101"
    ResourceDoesNotExistException = "STRKIT102"


class APIException(Exception):
    """
    # ! Parent Exception Class raised for reporting any error.

    Attributes:
        http_code -- http status code that need to be sent
        debug_message -- explanation of the error
    """

    def __init__(
        self,
        http_code: int,
        debug_message: str = None,
        message: str = None,
    ) -> None:
        self.http_code = http_code
        self.debug_message = debug_message
        self.exception_name = type(self).__name__
        self.starter_kit_code = self.__get_subexception()
        self.message = message if message else self.__get_error_message()

        super().__init__(self.message)

    def __get_subexception(self):
        try:
            starter_kit_exception = StarterKitExceptions[self.exception_name]
            if (
                str(starter_kit_exception)
                != f"StarterKitExceptions.{self.exception_name}"
            ):
                raise DuplicateErrorCodeException from self
            return starter_kit_exception.value
        except KeyError as err:
            raise UnknownErrorCodeException from err

    def __get_error_message(self):
        if self.http_code in HTTP_CODES:
            return HTTP_CODES[self.http_code]
        raise UnknownHttpCodeException


class InvalidRequestBodyException(APIException):
    """
    * Used when jsonschema doesn't matches with the schema
    * raised from utility payload validator
    """

    def __init__(self, payload_error: str) -> None:
        self.http_code = 400
        self.debug_message = str(payload_error)
        super().__init__(
            http_code=self.http_code, debug_message=self.debug_message
        )


class ResourceDoesNotExistException(APIException):
    """
    * to use when resource id is not found in database
    """

    def __init__(self, resource_name: str, resource_id: str) -> None:
        self.http_code = 400
        error_message = "Invalid Resource accessed."
        self.debug_message = (
            f"{resource_name.title()} with id: `{resource_id}`"
            " is either inactive or invalid."
        )
        super().__init__(
            http_code=self.http_code,
            debug_message=self.debug_message,
            message=error_message,
        )


class CustomException(APIException):
    """
    * to use when a specific module fails
    """

    def __init__(
        self, debug_message: str, error_message: str, http_code=500
    ) -> None:
        self.http_code = http_code
        self.debug_message = f"{debug_message}"
        self.message = f"{error_message}"
        super().__init__(
            http_code=self.http_code,
            debug_message=self.debug_message,
            message=error_message,
        )


class AuthorizationException(APIException):
    """
    * to use when authorization fails
    """

    def __init__(
        self, http_code: int, debug_message: str, error_message: str
    ) -> None:
        self.http_code = http_code
        self.debug_message = f"{debug_message}"
        self.message = f"{error_message}"
        super().__init__(
            http_code=self.http_code,
            debug_message=self.debug_message,
            message=error_message,
        )


# * --------->>>ADD OTHER CUSTOM EXCEPTIONS HERE<<<---------


class InternalServerErrorException(APIException):
    """
    # ! FOR INTERNAL USE ONLY
    # ! Used when any code level error has occured
    """

    def __init__(self) -> None:
        self.http_code = 500
        self.debug_message = random.choice(DEFAULT_MESSAGES)
        super().__init__(
            http_code=self.http_code, debug_message=self.debug_message
        )


class DatabaseErrorException(APIException):
    """
    # ! FOR INTERNAL USE ONLY
    # ! Used when any database related error has occured
    """

    def __init__(self, debug_message: str, error_message: str) -> None:
        self.http_code = 500
        self.debug_message = f"{debug_message}"
        self.message = f"{error_message}"
        super().__init__(
            http_code=self.http_code,
            debug_message=self.debug_message,
            message=error_message,
        )


class DuplicateErrorCodeException(APIException):
    """
    # ! FOR INTERNAL USE ONLY
    # ! Used when registered starter_kit error code has already been used
    """

    def __init__(self) -> None:
        self.http_code = 500
        self.debug_message = random.choice(DEFAULT_MESSAGES)
        super().__init__(
            http_code=self.http_code, debug_message=self.debug_message
        )


class UnknownErrorCodeException(APIException):
    """
    # ! FOR INTERNAL USE ONLY
    # ! Used when starter_kit error code
    # has not been registered in `StarterKitExceptions`
    """

    def __init__(self) -> None:
        self.http_code = 500
        self.debug_message = random.choice(DEFAULT_MESSAGES)
        super().__init__(
            http_code=self.http_code, debug_message=self.debug_message
        )


class UnknownHttpCodeException(APIException):
    """
    # ! FOR INTERNAL USE ONLY
    # ! Used when http status code is not in `HTTP_CODES`
    """

    def __init__(self) -> None:
        self.http_code = 500
        self.debug_message = random.choice(DEFAULT_MESSAGES)
        super().__init__(
            http_code=self.http_code, debug_message=self.debug_message
        )
