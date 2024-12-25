import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash incoming password.

    :param password: plain password to hash.
    :return: hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def verify_password(password: str, hashed_password: bytes) -> bool:
    """
    Verify if incoming password is correct to hashed one.

    :param password: plain password.
    :param hashed_password: hashed password.
    :return: True if passwords are equal, False otherwise.
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
