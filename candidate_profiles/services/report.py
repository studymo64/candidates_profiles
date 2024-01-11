import csv
import os
from concurrent.futures import ThreadPoolExecutor

from main.models import Candidate, UserBase


class ReportService:
    THREAD_COUNT = 2
    PAGE_SIZE = 5

    def __init__(self, repository):
        self.__candidate_repository = repository()

    def __get_count(self) -> int:
        """ Get the total count of candidates to paginate efficiently over them """
        return self.__candidate_repository.get_candidates_count()

    def __fetch_documents(self, page):
        skip_value = page * self.PAGE_SIZE
        cursor = self.__candidate_repository.paginate_candidates_for_report(skip_value, self.PAGE_SIZE)
        return list(cursor)

    def __paginated_generator(self, total_pages):
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = [executor.submit(self.__fetch_documents, page) for page in range(total_pages)]

            for future in futures:
                documents = future.result()
                for document in documents:
                    yield document

    @staticmethod
    def __write_to_csv(file_path, document):
        fieldnames_candidate = set(Candidate.__annotations__.keys())
        fieldnames_userbase = set(UserBase.__annotations__.keys())
        combined_fieldnames = fieldnames_candidate.union(fieldnames_userbase, {"_id"})
        file_exists = os.path.isfile(file_path)

        with open(file_path, "a", encoding="UTF8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=combined_fieldnames)

            if not file_exists:
                writer.writeheader()

            row_data = {}
            for field in combined_fieldnames:
                # Use get() to handle the case where the field might not be present in the document
                if document.get(field, None):
                    row_data[field] = document[field]
            writer.writerow(row_data)

    def generate_report(self):
        try:
            total_documents = self.__get_count()
            total_pages = (total_documents + self.PAGE_SIZE - 1) // self.PAGE_SIZE
            for document in self.__paginated_generator(total_pages):
                self.__write_to_csv("candidates.csv", document)
        except Exception as exc:
            print(f"Exception in generate_report: {exc}")
