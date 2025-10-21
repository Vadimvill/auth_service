from datetime import timedelta, datetime
from uuid import UUID

from jose import jwt
from passlib.context import CryptContext

from src.config import settings


class PasswordHasher:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        if self.pwd_context.verify(plain_password, hashed_password):
            return True
        raise ValueError("passwords not equal")


class JWT:
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        for key, value in to_encode.items():
            if isinstance(value, UUID):
                to_encode[key] = str(value)
        if expires_delta:
            expire_minutes = int(expires_delta)
            expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, str(settings.SECRET_KEY), algorithm=settings.ALGORITHM
        )
        return encoded_jwt
