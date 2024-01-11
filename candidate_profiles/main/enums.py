from enum import Enum


class CandidateCareerLevel(str, Enum):
    INTERN = "Intern"
    JUNIOR = "Junior"
    MID_LEVEL = "Mid Level"
    SENIOR = "Senior"
    TEAM_LEAD = "Team Lead"


class DegreeType(str, Enum):
    HIGH_SCHOOL = "High School"
    BACHELOR = "Bachelor"
    MASTERS = "Masters"


class GenderType(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    NOT_SPECIFIED = "Not Specified”"


class PaginationState(Enum):
    END_REACHED = "end"
