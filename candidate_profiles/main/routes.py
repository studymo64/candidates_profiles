from typing import Optional

from main.request_filters import CreateUserRequest, LoginRequest, CreateCandidateRequest, UpdateCandidateRequest, \
    CandidatesSearchRequest, Token
from services import UserService, CandidateService
from repositories import UserRepository, CandidateRepository

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from services import AuthService
from services.report import ReportService

auth_middleware = AuthService.get_current_user
router = APIRouter()


# Health check
@router.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return "Server is up and running"


@router.post("/user", status_code=status.HTTP_201_CREATED)
async def signup(create_user_request: CreateUserRequest):
    service = UserService(UserRepository)
    created = service.signup(create_user_request)
    if not created:
        return HTTPException(status_code=400)


@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login(form_data: LoginRequest):
    service = UserService(UserRepository)
    access_token, authenticated = service.login(form_data)
    if not authenticated:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/candidate/{candidate_id}", status_code=status.HTTP_200_OK)
async def get_candidate(candidate_id: str, user: str = Depends(auth_middleware)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")

    service = CandidateService(CandidateRepository)
    candidate, exists = service.get(candidate_id)
    if not exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="candidate with this id does not exist!")
    return candidate


@router.post("/candidate", status_code=status.HTTP_201_CREATED)
async def create_candidate(candidate: CreateCandidateRequest, user: str = Depends(auth_middleware)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")

    service = CandidateService(CandidateRepository)
    candidate, created = service.create(candidate)
    if not created:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="candidate with this email already exists!")
    return candidate


@router.put("/candidate/{candidate_id}", status_code=status.HTTP_201_CREATED)
async def update_candidate(candidate_id: str, candidate_request: Optional[UpdateCandidateRequest] = None,
                           user: str = Depends(auth_middleware)
                           ):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")

    service = CandidateService(CandidateRepository)
    candidate, updated = service.update(candidate_id, candidate_request)
    if not updated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="candidate with this id does not exist!")
    return candidate


@router.delete("/candidate/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(candidate_id: str, user: str = Depends(auth_middleware)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")

    service = CandidateService(CandidateRepository)
    deleted = service.delete(candidate_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="candidate with this id does not exist!")


@router.get("/all-candidates", status_code=status.HTTP_200_OK)
async def search_candidate(candidate_search_request: CandidatesSearchRequest,
                           user: str = Depends(auth_middleware)
                           ):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")

    service = CandidateService(CandidateRepository)
    candidates, next_cursor = service.get_all_candidates(candidate_search_request, user)
    return {"cursor": next_cursor, "candidates": candidates}


@router.post("/generate-report", status_code=status.HTTP_200_OK)
async def generate_report(user: str = Depends(auth_middleware)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization Failed")

    service = ReportService(CandidateRepository)
    service.generate_report()
