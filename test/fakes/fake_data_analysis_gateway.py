from app.application.ports import DataAnalysisGateway
from app.domain.file import File


class FakeDataAnalysisGateway(DataAnalysisGateway):
    def clean_internal_dataset(self, dataset_file: File) -> bytes:
        return b"cleaned file content"
