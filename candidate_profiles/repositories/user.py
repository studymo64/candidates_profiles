from . import BaseRepository
from config.database import users_collection
from main.schemas import UserSchema


class UserRepository(BaseRepository):
    def __init__(self):
        self._collection = users_collection

    def get_all(self):
        users = UserSchema.list_serial(self._collection.find())
        return users

    def get_by_id(self, item_id):
        user = self._collection.find_one({"_id": item_id})
        return user if user is not None else None

    def get_by_email(self, email):
        user = self._collection.find_one({"email": email})
        return user if user is not None else None

    def create(self, item):
        self._collection.insert_one(item)

    def update(self, item):
        raise NotImplementedError

    def delete(self, item_id):
        raise NotImplementedError
