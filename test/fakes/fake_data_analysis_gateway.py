from app.application.ports import DataAnalysisGateway


class FakeDataAnalysisGateway(DataAnalysisGateway):
    def clean_internal_dataset(self, file_name: str, file_content: bytes) -> bytes:
        return b"cleaned file content"
