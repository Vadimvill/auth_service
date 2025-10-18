from passlib.context import CryptContext


class PasswordHasher:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        if self.pwd_context.verify(plain_password, hashed_password):
            return True
        raise ValueError("passwords not equal")
