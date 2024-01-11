from datetime import datetime as dt, timedelta
from fastapi import Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
import settings
from repositories import UserRepository

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/token")


class AuthService:
    """ Verify passwords and JWT tokens"""
    def __init__(self):
        self.__bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.__bcrypt_context.hash(password)

    def verify_password_hash(self, plain_password: str, user_hash: str) -> bool:
        return self.__bcrypt_context.verify(plain_password, user_hash)

    @classmethod
    def create_access_token(cls, first_name, user_id):
        expires = dt.utcnow() + timedelta(minutes=settings.JWT_CONFIG["TTL_MINUTES"])
        data = {"sub": first_name, "id": user_id, "exp": expires}
        return jwt.encode(data, settings.JWT_CONFIG["SECRET_KEY"], algorithm=settings.JWT_CONFIG["ALGORITHM"])

    @classmethod
    def get_current_user(cls, access_token: str = Depends(oauth2_bearer)):
        from services import UserService    # quick fix to evade circular import

        try:
            payload = jwt.decode(access_token, settings.JWT_CONFIG["SECRET_KEY"], algorithms=settings.JWT_CONFIG["ALGORITHM"])
            first_name: str = payload.get("sub", "")
            user_id: int = payload.get("id", 0)
            if not first_name or not user_id:
                return None

            user_service = UserService(UserRepository)
            user = user_service.get_user(user_id)
            return user
        except JWTError:
            return None
