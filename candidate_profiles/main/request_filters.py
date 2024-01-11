from typing import Literal, Optional
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr, field_validator

from main.decorators import partial_model
from main.enums import CandidateCareerLevel, DegreeType, GenderType


class UserRequestBase(BaseModel):
    email: EmailStr
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)


class CreateUserRequest(UserRequestBase):
    password: str = Field(min_length=8, max_length=64)


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


class CreateCandidateRequest(UserRequestBase):
    career_level: CandidateCareerLevel
    job_major: str = Field(max_length=64)
    years_of_experience: int = Field(None, ge=-1, le=70)
    degree_type: DegreeType
    skills: list
    nationality: str  # could be refactored to validate the nationality
    city: str = Field(max_length=30)
    salary: int
    gender: Literal[GenderType.MALE, GenderType.FEMALE, GenderType.NOT_SPECIFIED]


@partial_model
class UpdateCandidateRequest(CreateCandidateRequest):
    pass


@partial_model
class CandidatesSearchRequest(CreateCandidateRequest):
    page_size: int = Field(5, ge=5, le=51)
    cursor: str = Field(default="")   # cursor is used for pagination purposes
    global_search_term: str = Field(default="")
