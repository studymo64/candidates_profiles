"""
    A place where we write the business logic, validations for the users of the application
"""
import uuid
from typing import List, Tuple
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from bson.objectid import ObjectId

from config.database import users_collection
from main.models import User
from main.request_filters import CreateUserRequest
from main.schemas import UserSchema
from . import AuthService


class UserService:

    def __init__(self, repository):
        self.__user_repository = repository()
        self.__bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.auth_service = AuthService()

    def __prep_user_data(self, create_user_request: CreateUserRequest) -> dict:
        """ Build the dictionary required so user will be inserted in the db """
        user_uuid = uuid.uuid4()
        return {
            "first_name": create_user_request.first_name,
            "last_name": create_user_request.last_name,
            "email": create_user_request.email,
            "password": self.auth_service.hash_password(create_user_request.password),
            "uuid": user_uuid
        }

    def signup(self, create_user_request: CreateUserRequest) -> bool:
        try:
            is_already_created = self.__user_repository.get_by_email(create_user_request.email)
            if is_already_created:
                return False

            user_dict = self.__prep_user_data(create_user_request)
            self.__user_repository.create(user_dict)
            return True
        except Exception as exc:
            # TODO:: implement logger
            print(f"Exception in signup service. exc: {exc}")

    def login(self, form_data):
        user = self.__user_repository.get_by_email(form_data.email)
        if not user:
            return None, False
        if not self.auth_service.verify_password_hash(form_data.password, user["password"]):
            return None, False

        # User is valid. # create tokens
        tokens = self.auth_service.create_access_token(user["first_name"], str(user["_id"]))
        return tokens, True

    def get_user(self, user_id):
        return self.__user_repository.get_by_id(ObjectId(user_id))

    @classmethod
    def list_users(cls) -> List[User]:
        try:
            users = UserSchema.list_serial(users_collection.find())
            # TODO:: Paginate this
            return users
        except Exception as exc:
            # TODO:: implement logger
            print(f"Exception in signup service. exc: {exc}")
