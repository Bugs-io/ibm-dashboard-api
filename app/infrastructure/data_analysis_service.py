import requests
from app.config import Config
from app.application.ports import DataAnalysisGateway
from app.application.errors import ProcessedFileCreationError, \
        DataAnalysisServiceError


class DataAnalysisService(DataAnalysisGateway):
    def __init__(self):
        self.base_url = Config.ANALYSIS_SERVICE_URL

    def clean_internal_dataset(
            self,
            file_name: str,
            file_content: bytes) -> bytes:
        file = (file_name, file_content)
        url = self.base_url + "/clean-internal-dataset"

        response = requests.post(url, files={"file": file}, timeout=5)

        if response.status_code != 200:
            raise ProcessedFileCreationError

        return response.content

    def test_graph(self, file_name: str, file_content: bytes):
        file = (file_name, file_content)
        url = self.base_url + "/test-graph"

        response = requests.post(url, files={"file": file}, timeout=5)

        if response.status_code != 200:
            raise DataAnalysisServiceError

        return response.json()
