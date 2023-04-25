import os
from kink import di
from os.path import join, dirname
from dotenv import load_dotenv

from app.application.service import IBMDashboardService
from app.infrastructure import GoogleCloudStorage, PostgreSQLUserRepository,\
    BcryptEncrypter, JWTManager, PostgreSQLInternalDatasetRepository

JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = "secret"
MILLISECONDS_IN_A_DAY = 86400000
GOOGLE_APPLICATION_CREDENTIALS = "credentials.json"
BUCKET_NAME = "ibm-dashboard_test_bucket"


def bootstrap_di():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

    di[IBMDashboardService] = IBMDashboardService(
            encrypter=BcryptEncrypter(),
            internal_dataset_repository=PostgreSQLInternalDatasetRepository(),
            object_storage=GoogleCloudStorage(
                bucket_name=BUCKET_NAME
                ),
            token_manager=JWTManager(
                algorithm=JWT_ALGORITHM,
                secret_key=JWT_SECRET_KEY,
                expiration_delta=MILLISECONDS_IN_A_DAY
                ),
            user_repository=PostgreSQLUserRepository(),
            )
