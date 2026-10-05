from uss.account import UserSession
from uss.controller_utils import HttpResult, respond
from uss.user_self_service import UserSelfService


class LoginController:
    def __init__(self, service: UserSelfService):
        self._service = service

    def action(self, body: object) -> HttpResult:
        # the body is untrusted input: the service validates it
        return respond(200, lambda: _to_json(self._service.login(body)))


def _to_json(session: UserSession) -> dict:
    return {
        "accountId": session.account_id,
        "username": session.username,
        "email": session.email,
    }
