from pymongo import ReturnDocument

from . import BaseRepository
from config.database import candidates_collection
from main.schemas import CandidateSchema


class CandidateRepository(BaseRepository):
    def __init__(self):
        self._collection = candidates_collection

    def get_all(self):
        candidates = CandidateSchema.list_serial(self._collection.find())
        return candidates

    def get_by_id(self, item_id):
        candidate = self._collection.find_one({"_id": item_id})
        return candidate if candidate is not None else None

    def get_by_email(self, email):
        candidate = self._collection.find_one({"email": email})
        return candidate if candidate is not None else None

    def search_by_field(self, search_field):
        candidate = self._collection.find_one({f"{search_field}": search_field})
        return candidate if candidate is not None else None

    def create(self, item):
        return self._collection.insert_one(item)

    def update(self, item: dict):
        return self._collection.find_one_and_update(filter={"_id": item["id"]}, update={"$set": dict(item)}, return_document=ReturnDocument.AFTER)

    def delete(self, item_id):
        return self._collection.delete_one({"_id": item_id})

    def get_random_document(self):
        return self._collection.find_one()

    def filter_candidates(self, filter_terms: dict, page_size: int):
        return self._collection.find(filter=filter_terms).limit(page_size).sort("_id", 1)

    def get_candidates_count(self):
        return self._collection.count_documents({})

    def paginate_candidates_for_report(self, skip_value: int, page_size: int):
        return self._collection.find({}).skip(skip_value).limit(page_size).sort("_id", 1)
