from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, EmailStr
from .enums import CandidateCareerLevel, DegreeType, GenderType


class UserBase(BaseModel):
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    email: EmailStr
    uuid: UUID


class User(UserBase):
    pass


class Candidate(UserBase):
    career_level: CandidateCareerLevel
    job_major: str = Field(max_length=64)
    years_of_experience: int = Field(None, ge=-1, le=70)
    degree_type: DegreeType
    skills: list
    nationality: str    # could be refactored to validate the nationality
    city: str = Field(max_length=30)
    salary: int
    gender: Literal[GenderType.MALE, GenderType.FEMALE, GenderType.NOT_SPECIFIED]


