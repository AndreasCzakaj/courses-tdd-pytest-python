import hashlib
import os
import re
import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.post("/uss/login")
def login():
    c = None
    try:
        d = request.get_json(silent=True)
        if d and isinstance(d, dict):
            if "username" in d and isinstance(d["username"], str):
                if len(d["username"]) >= 8:
                    if len(d["username"]) <= 20:
                        if re.fullmatch(r"[a-zA-Z0-9\-_]+", d["username"]):
                            if "password" in d and isinstance(d["password"], str):
                                if len(d["password"]) >= 12 and len(d["password"]) <= 32:
                                    if re.fullmatch(r"[a-zA-Z0-9\-_.,+]+", d["password"]):
                                        # check db
                                        c = sqlite3.connect(os.environ.get("USS_DB", "uss.db"))
                                        r = c.execute(
                                            "SELECT * FROM accounts WHERE username = ?", (d["username"],)
                                        ).fetchone()
                                        if r:
                                            tmp = r[2].split(":")
                                            h = hashlib.scrypt(
                                                d["password"].encode(),
                                                salt=tmp[0].encode(), n=16384, r=8, p=1, dklen=64,
                                            ).hex()
                                            if h == tmp[1]:
                                                if r[5] == "verified":
                                                    return jsonify(
                                                        {"accountId": r[0], "username": r[1], "email": r[3]}
                                                    ), 200
                                                else:
                                                    return jsonify({"error": "account not verified"}), 400
                                            else:
                                                return jsonify({"error": "unknown username or wrong password"}), 401
                                        else:
                                            return jsonify({"error": "unknown username or wrong password"}), 401
                                    else:
                                        return jsonify({"error": "invalid: password"}), 400
                                else:
                                    return jsonify({"error": "invalid: password"}), 400
                            else:
                                return jsonify({"error": "invalid: password"}), 400
                        else:
                            return jsonify({"error": "invalid: username"}), 400
                    else:
                        return jsonify({"error": "invalid: username"}), 400
                else:
                    return jsonify({"error": "invalid: username"}), 400
            else:
                return jsonify({"error": "invalid: username"}), 400
        else:
            return jsonify({"error": "invalid: username"}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": "try again later"}), 500
    finally:
        if c:
            c.close()
