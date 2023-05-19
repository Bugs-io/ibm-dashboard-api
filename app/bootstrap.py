from kink import di

from app.config import Config
from app.application.service import IBMDashboardService
from app.infrastructure import GoogleCloudStorage, PonyORMUserRepository,\
    BcryptEncrypter, JWTManager, PonyORMInternalDatasetRepository

MILLISECONDS_IN_A_DAY = 86400000


def bootstrap_di():
    di[IBMDashboardService] = IBMDashboardService(
            encrypter=BcryptEncrypter(),
            internal_dataset_repository=PonyORMInternalDatasetRepository(),
            object_storage=GoogleCloudStorage(
                bucket_name=Config.BUCKET_NAME
                ),
            token_manager=JWTManager(
                algorithm=Config.JWT_ALGORITHM,
                secret_key=Config.JWT_SECRET,
                expiration_delta=MILLISECONDS_IN_A_DAY
                ),
            user_repository=PonyORMUserRepository(),
            )
