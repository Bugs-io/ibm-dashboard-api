from kink import di

from app.config import Config
from app.application.ports import ObjectStorage, UserRepository,\
        Encrypter, TokenManager, InternalDatasetRepository, DataAnalysisGateway
from app.infrastructure import GoogleCloudStorage, PonyORMUserRepository,\
    BcryptEncrypter, JWTManager, PonyORMInternalDatasetRepository,\
    DataAnalysisService

from test.fakes import FakeObjectStorage, FakeDataAnalysisGateway

MILLISECONDS_IN_A_DAY = 86400000


def bootstrap_di_testing():
    di[Encrypter] = BcryptEncrypter()
    di[TokenManager] = JWTManager(
            algorithm=Config.JWT_ALGORITHM,
            secret_key=Config.JWT_SECRET,
            expiration_delta=MILLISECONDS_IN_A_DAY
            )
    di[InternalDatasetRepository] = PonyORMInternalDatasetRepository()
    di[UserRepository] = PonyORMUserRepository()

    di[ObjectStorage] = FakeObjectStorage()
    di[DataAnalysisGateway] = FakeDataAnalysisGateway()


def bootstrap_di_production():
    di[Encrypter] = BcryptEncrypter()
    di[ObjectStorage] = GoogleCloudStorage(bucket_name=Config.BUCKET_NAME)
    di[TokenManager] = JWTManager(
            algorithm=Config.JWT_ALGORITHM,
            secret_key=Config.JWT_SECRET,
            expiration_delta=MILLISECONDS_IN_A_DAY
            )
    di[InternalDatasetRepository] = PonyORMInternalDatasetRepository()
    di[UserRepository] = PonyORMUserRepository()
    di[DataAnalysisGateway] = DataAnalysisService()


def bootstrap_di():
    if Config.TESTING:
        bootstrap_di_testing()
    else:
        bootstrap_di_production()
