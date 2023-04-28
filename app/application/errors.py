class InvalidFileTypeError(Exception):
    pass


class InvalidEmailError(Exception):
    pass


class UserAlreadyExistsError(Exception):
    pass


class UserCreationError(Exception):
    pass


class UserDoesNotExistError(Exception):
    pass


class InvalidPasswordError(Exception):
    pass


class ProcessedFileCreationError(Exception):
    pass


class InternalDatasetCreationError(Exception):
    pass
