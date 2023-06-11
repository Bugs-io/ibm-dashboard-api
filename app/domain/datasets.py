class InternalDataset:
    def __init__(
            self,
            id,
            processed_file_path,
            raw_file_path,
            is_active,
            uploaded_at):
        self.id = id
        self.processed_file_path = processed_file_path
        self.raw_file_path = raw_file_path
        self.is_active = is_active
        self.uploaded_at = uploaded_at
