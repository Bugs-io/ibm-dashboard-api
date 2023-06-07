import requests
from app.config import Config
from app.domain.file import File
from app.application.ports import DataAnalysisGateway
from app.application.errors import ProcessedFileCreationError, \
        DataAnalysisServiceError


class DataAnalysisService(DataAnalysisGateway):
    def __init__(self):
        self.base_url = Config.ANALYSIS_SERVICE_URL

    def clean_internal_dataset(self, dataset_file: File) -> bytes:
        url = self.base_url + "/clean-internal-dataset"

        response = requests.post(url, files={"file": dataset_file.tuple()}, timeout=5)

        if response.status_code != 200:
            raise ProcessedFileCreationError

        return response.content

    def get_most_attended_certifications(self, dataset_file: File, since_years: int, limit: int):
        url = self.base_url + "/graphs/query-most-attended-certifications"

        files = {"dataset": dataset_file.tuple()}
        params = {"since_years": since_years, "limit": limit}

        print("sending params", params)

        response = requests.post(url, files=files, data=params, timeout=5)

        if response.status_code != 200:
            raise DataAnalysisServiceError

        return response.json()

    def get_percentage_of_matched_certifications(self, dataset_file: File):
        url = self.base_url + "/graphs/query-matched-certifications"

        files = {"dataset": dataset_file.tuple()}

        response = requests.post(url, files=files)

        if response.status_code != 200:
            raise DataAnalysisServiceError

        return response.json()
    
    def get_top_industry_courses(self):
        url = self.base_url + "/graphs/top-industry-courses"

        response = requests.get(url)

        if response.status_code != 200:
            raise DataAnalysisServiceError
    
        return response.json()

