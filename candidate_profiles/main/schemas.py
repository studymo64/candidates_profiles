from typing import Union, List
from .models import User, Candidate


class BaseSchema:
    """
        - Serves the common schema representation for the collections
        - Child classes could implement their own methods and create a task-specific schemas repers
    """

    @classmethod
    def individual_serial(cls, obj: Union[User, Candidate], is_candidate=False):
        base_schema = {
            "id": str(obj["_id"]),
            "first_name": str(obj["first_name"]),
            "last_name": str(obj["last_name"]),
            "email": str(obj["email"]),
            "uuid": str(obj["uuid"])
        }

        if is_candidate:
            extra = {
                "career_level": str(obj["career_level"]),
                "job_major": str(obj["job_major"]),
                "years_of_experience": str(obj["years_of_experience"]),
                "degree_type": str(obj["degree_type"]),
                "skills": list(obj["skills"]),
                "nationality": str(obj["nationality"]),
                "city": str(obj["city"]),
                "salary": str(obj["salary"]),
                "gender": str(obj["gender"])
            }
            base_schema.update(extra)
        return base_schema

    @classmethod
    def list_serial(cls, objs: List, is_candidate=False) -> list:
        return [cls.individual_serial(obj, is_candidate) for obj in objs]


class UserSchema(BaseSchema):

    @classmethod
    def individual_serial(cls, user, is_candidate=False) -> dict:
        schema = super().individual_serial(user)
        return schema

    @classmethod
    def list_serial(cls, users: List, is_candidate=False) -> list:
        schema = super().list_serial(users)
        return schema


class CandidateSchema(BaseSchema):

    @classmethod
    def individual_serial(cls, candidate, is_candidate=True) -> dict:
        schema = super().individual_serial(candidate, is_candidate)
        return schema

    @classmethod
    def list_serial(cls, candidates: List, is_candidate=True) -> list:
        schema = super().list_serial(candidates, is_candidate)
        return schema
