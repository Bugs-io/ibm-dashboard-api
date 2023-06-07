from app.domain.file import File


class DataAnalysisGateway:
    def clean_internal_dataset(self, dataset_file: File) -> bytes:
        return

    def get_most_attended_certifications(self, dataset_file: File, since_years: int, limit: int):
        return

    def get_percentage_of_matched_certifications(self, dataset_file: File):
        return

    def get_top_industry_courses(self):
        return

    def get_certifications_taken_over_the_years(self, dataset_file: File):
        return

    def get_employee_certifications_categorized(
            self,
            dataset_file: File,
            emplooye_id: str):
        return
