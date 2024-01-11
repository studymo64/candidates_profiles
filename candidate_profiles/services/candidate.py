"""
    A place where we write the business logic, validations for the candidates
"""
import re
import uuid
from datetime import datetime as dt

from main.enums import PaginationState
from main.request_filters import CreateCandidateRequest
from main.schemas import CandidateSchema
from bson.objectid import ObjectId

from services.paginator import PaginationService


class CandidateService:

    def __init__(self, repository):
        self.__candidate_repository = repository()

    def get(self, item_id):
        candidate = self.__candidate_repository.get_by_id(ObjectId(item_id))
        if not candidate:
            return None, False

        candidate = CandidateSchema().individual_serial(candidate)
        return candidate, True

    def create(self, candidate_request: CreateCandidateRequest):
        try:
            is_already_created = self.__candidate_repository.get_by_email(candidate_request.email)
            if is_already_created:
                return None, False

            candidate_dict = {key: value for key, value in candidate_request}
            candidate_dict.update({"uuid": uuid.uuid4()})

            result = self.__candidate_repository.create(candidate_dict)

            candidate_id = result.inserted_id
            candidate = CandidateSchema.individual_serial(self.__candidate_repository.get_by_id(ObjectId(candidate_id)))
            return candidate, True
        except Exception as exc:
            print(f"{dt.utcnow()} | Exception in CandidateService.create: {exc}")

    def update(self, candidate_id, candidate_request):
        try:
            candidate = self.__candidate_repository.get_by_id(ObjectId(candidate_id))
            if not candidate:
                return None, False

            candidate_dict = {key: value for key, value in candidate_request if value is not None and value != ""}
            candidate_dict.update({"id": ObjectId(candidate_id)})
            updated_candidate = self.__candidate_repository.update(candidate_dict)

            candidate = CandidateSchema.individual_serial(updated_candidate)
            return candidate, True
        except Exception as exc:
            print(f"{dt.utcnow()} | Exception in CandidateService.create: {exc}")

    def delete(self, item_id) -> bool:
        """
            Here We could allow deletion only if:
            - The logged-in user is the same as the candidate.
            - Or only allow deletion if this logged-in user is the one who created the candidate.
            - Or users with specific flag (let's say admin) are allowed to delete different candidates
        """
        result = self.__candidate_repository.delete(ObjectId(item_id))
        return True if result.deleted_count == 1 else False

    def get_all_candidates(self, candidate_search_request, user):
        """
            1- populate the filters
            2- get cursor:
                - cursor means the last candidate_id that was retrieved from the previous request.
                - Check PaginationService() for extra details.
            3- retrieve the candidates based on the search terms && build the cursor for the next request.

            :param candidate_search_request:
            :param user: logged-in user
            :return: List(Candidate, cursor)
        """

        page_size = candidate_search_request.page_size if candidate_search_request.page_size else 5
        request_cursor = candidate_search_request.cursor if candidate_search_request.cursor else ""
        global_search_term = candidate_search_request.global_search_term

        if global_search_term is not None:
            # Create a regex pattern for the search term to match against all fields
            regex_pattern = re.compile(f".*{global_search_term}.*", re.IGNORECASE)
            sample_document = self.__candidate_repository.get_random_document()
            field_names = list(sample_document.keys())

            # Construct the query with $or and $regex for each field
            or_conditions = [{f"{field}": {"$regex": regex_pattern}} for field in field_names]
            filter_terms = {"$or": or_conditions}

        elif candidate_search_request:
            filter_terms = {key: value for key, value in candidate_search_request if key not in ["cursor", "page_size"] and value is not None}
        else:
            request_cursor = None
            filter_terms = {}

        # Decode cursor and paginate
        cursor = PaginationService().get_cursor(request_cursor)
        if cursor['cursor_id']:
            filter_terms.update({"_id": {"$gt": ObjectId(cursor['cursor_id'])}})
            db_res = self.__candidate_repository.filter_candidates(filter_terms, page_size + 1)  # We get 1 more document than the page size to know if there is a next page
            first_load = False
        else:
            db_res = self.__candidate_repository.filter_candidates(filter_terms, page_size + 1)
            first_load = True

        candidates = [c for c in db_res]    # no need to load them in generators. max page_size is 50

        next_cursor = PaginationService().build_cursor(page_size, str(user["_id"]), candidates, first_load)
        candidates = CandidateSchema().list_serial(candidates[:page_size])

        if next_cursor == PaginationState.END_REACHED.value:
            return candidates, next_cursor
        else:
            return candidates, next_cursor
