from uss.account import Account, UserSession
from uss.account_dao import AccountDao, DaoError
from uss.password import verify_password
from uss.validation import validate_credentials


class UserSelfServiceError(Exception):
    pass


class AuthenticationError(UserSelfServiceError):
    """The SAME error for an unknown username and for a wrong password:
    the response must not reveal which usernames exist."""

    def __init__(self):
        super().__init__("unknown username or wrong password")


class AccountNotVerifiedError(UserSelfServiceError):
    def __init__(self):
        super().__init__("account not verified")


class ServerError(UserSelfServiceError):
    pass


class UserSelfService:
    def __init__(self, account_dao: AccountDao):
        self.account_dao = account_dao

    def login(self, credentials: object) -> UserSession:
        valid_credentials = validate_credentials(credentials)

        account = self._find_account(valid_credentials.username)
        if account is None or not verify_password(valid_credentials.password, account.password_hash):
            raise AuthenticationError()
        if account.status != "verified":
            raise AccountNotVerifiedError()

        return UserSession(account_id=account.id, username=account.username, email=account.email)

    def _find_account(self, username: str) -> Account | None:
        try:
            return self.account_dao.find_by_username(username)
        except DaoError as e:
            raise ServerError("Database not available. Try later.") from e
