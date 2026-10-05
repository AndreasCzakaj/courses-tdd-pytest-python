import logging
from collections.abc import Callable

from uss.user_self_service import AccountNotVerifiedError, AuthenticationError
from uss.validation import ValidationError

MESSAGE_SERVER_ERROR = "try again later"

# The errors that are the client's fault, with their HTTP status
CLIENT_ERRORS: tuple[tuple[type[Exception], int], ...] = (
    (ValidationError, 400),
    (AuthenticationError, 401),
    (AccountNotVerifiedError, 400),
)

# (JSON body, HTTP status): what a controller returns, independent of the web framework
HttpResult = tuple[dict, int]

logger = logging.getLogger(__name__)


def calc_http_error_code(e: Exception) -> int:
    return next((status for error_type, status in CLIENT_ERRORS if isinstance(e, error_type)), 500)


def calc_error_message(e: Exception) -> str:
    """Clients get the details of their own errors only, never the server's internals."""
    return str(e) if calc_http_error_code(e) < 500 else MESSAGE_SERVER_ERROR


def respond(success_status: int, service_call: Callable[[], dict]) -> HttpResult:
    """Runs a service call and maps its outcome to the HTTP result:
    the result with the given status, or an error status with a message."""
    try:
        return service_call(), success_status
    except Exception as service_error:
        status = calc_http_error_code(service_error)
        if status >= 500:
            logger.exception("server error")
        return {"error": calc_error_message(service_error)}, status
