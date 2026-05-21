import bcrypt


def get_hash_password(password: str) -> str:
    """哈希密码，bcrypt 限制 72 字节"""
    password_bytes = password.encode()[:72]
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    password_bytes = plain_password.encode()[:72]
    return bcrypt.checkpw(password_bytes, hashed_password.encode())
