import base64
import json

from main.enums import PaginationState
from main.models import Candidate


class PaginationService:

    @classmethod
    def __encode_cursor(cls, user_id=None, cursor_id=""):
        """
            In a real world app here we will encrypt the cursor and add user-specific identifiers to:
                - Track user activity.
                - Improve user engagement by serving better results from using this data in ML projects.

            param:: user_id: logged-in user.
            param:: cursor_id: last object_id
        """
        cursor = {
            "user_id": user_id,
            "cursor_id": cursor_id
        }
        cursor_bytes = json.dumps(cursor).encode("utf-8")
        base64_bytes = base64.b64encode(cursor_bytes)
        base64_cursor = base64_bytes.decode("utf-8")
        return base64_cursor

    @classmethod
    def __decode_cursor(cls, cursor):
        base64_bytes = cursor.encode("utf-8")
        text_bytes = base64.b64decode(base64_bytes)
        decoded_cursor = json.loads(text_bytes.decode("utf-8"))
        return decoded_cursor

    @classmethod
    def get_cursor(cls, cursor: str):
        if cursor and cursor != "load":
            cursor = cls.__decode_cursor(cursor)
        else:
            cursor = {"user_id": None, "cursor_id": 0}
        return cursor

    @classmethod
    def build_cursor(cls, page_size=5, user_id=None, candidates: Candidate = None, first_load: bool = False) -> str:
        """
        param candidates: Note: don't user mutable types (like lists) as default values in function parameters.
        param first_load: if True -> it means it is the first page/ first request
        :return:
        """
        if not candidates:
            candidates = []

        if len(candidates) > page_size:
            next_cursor_id = list(candidates[:page_size])[-1]["_id"]    # get the last candidate id (ObjectId)
            next_cursor = cls.__encode_cursor(user_id, str(next_cursor_id))
        else:  # ex: last page had 2 candidates
            next_cursor = PaginationState.END_REACHED.value if not first_load else None
        return next_cursor

    @classmethod
    def efficiently_paginate(cls, iterabble):
        """ simple yield values """