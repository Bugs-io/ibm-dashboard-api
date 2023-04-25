import os
from kink import di
from dotenv import load_dotenv

from app.application.service import IBMDashboardService
from app.infrastructure import GoogleCloudStorage, PostgreSQLUserRepository,\
    BcryptEncrypter, JWTManager, PostgreSQLInternalDatasetRepository

MILLISECONDS_IN_A_DAY = 86400000



def bootstrap_di():
    di[IBMDashboardService] = IBMDashboardService(
            encrypter=BcryptEncrypter(),
            internal_dataset_repository=PostgreSQLInternalDatasetRepository(),
            object_storage=GoogleCloudStorage(
                bucket_name=os.getenv('BUCKET_NAME'),
                ),
            token_manager=JWTManager(
                algorithm=os.getenv('JWT_ALGORITHM'),
                secret_key=os.getenv('JWT_SECRET_KEY'),
                expiration_delta=MILLISECONDS_IN_A_DAY
                ),
            user_repository=PostgreSQLUserRepository(),
            )
