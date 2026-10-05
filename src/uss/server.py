from flask import Flask, jsonify, request

from uss.account_dao_sqlite_impl import AccountDaoSqliteImpl
from uss.login_controller import LoginController
from uss.user_self_service import UserSelfService

# Integration code only: wires the parts and defines the routes.
# No logic here => nothing to unit test, the integration test covers it.


def create_app(db_path: str) -> Flask:
    account_dao = AccountDaoSqliteImpl(db_path)
    service = UserSelfService(account_dao)
    login_controller = LoginController(service)

    app = Flask(__name__)

    @app.post("/uss/login")
    def login():
        body, status = login_controller.action(request.get_json(silent=True))
        return jsonify(body), status

    return app
