import os
from kink import di
from os.path import join, dirname
from dotenv import load_dotenv

from app.application.service import IBMDashboardService
from app.infrastructure import GoogleCloudStorage, PostgreSQLUserRepository,\
    BcryptEncrypter


def bootstrap_di():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

    bucket_name = "ibm-dashboard_test_bucket"

    di[IBMDashboardService] = IBMDashboardService(
            encrypter=BcryptEncrypter(),
            object_storage=GoogleCloudStorage(bucket_name),
            user_repository=PostgreSQLUserRepository(),
            )
