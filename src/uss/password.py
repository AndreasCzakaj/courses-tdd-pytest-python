import hashlib
import hmac
import secrets

SALT_BYTES = 16
HASH_BYTES = 64
SEPARATOR = ":"


def hash_password(password: str, salt: str | None = None) -> str:
    """Returns "<salt>:<hash>", both hex encoded."""
    salt = salt or secrets.token_hex(SALT_BYTES)
    return salt + SEPARATOR + _calc_hash(password, salt)


def verify_password(password: str, password_hash: str) -> bool:
    salt, _, expected = password_hash.partition(SEPARATOR)
    actual = _calc_hash(password, salt)
    # constant time: the duration must not reveal how many chars match
    return hmac.compare_digest(actual, expected)


def _calc_hash(password: str, salt: str) -> str:
    return hashlib.scrypt(password.encode(), salt=salt.encode(), n=16384, r=8, p=1, dklen=HASH_BYTES).hex()
