from locust import HttpUser, task
from uuid import uuid4

LOGIN_PAYLOAD = {
                "email": "testuser@ibm.com",
                "password": "somepass"
                }


class ProtectedRoutesSetUp(HttpUser):
    auth_token = ""

    def on_start(self):
        self.login()

    def login(self):
        headers = {"Content-Type": "application/json"}
        payload = LOGIN_PAYLOAD
        response = self.client.post("/login", json=payload, headers=headers)
        self.auth_token = response.json()["id_token"]


class LoginTest(HttpUser):
    @task
    def login_loading_test(self):
        payload = LOGIN_PAYLOAD
        self.client.post("/login", json=payload)


class SignupTest(HttpUser):
    @task
    def signup_loading_test(self):
        payload = {
                "email": f"{str(uuid4())}@ibm.com",
                "password": "somepass",
                "first_name": "John",
                "last_name": "Doe"
                }
        self.client.post("/signup", json=payload)


class UploadInternalDatasetTest(ProtectedRoutesSetUp):
    @task
    def upload_internal_dataset_loading_test(self):
        if self.auth_token == "":
            self.login()
        headers = {
                "Authorization": f"Bearer {self.auth_token}"
                }

        with open("./badges.xlsx", 'rb') as file:
            self.client.post(
                "/upload-internal-dataset",
                files={"file": file},
                headers=headers
                )


class MostAttendedCertificationsTest(ProtectedRoutesSetUp):
    @task
    def upload_internal_dataset_loading_test(self):
        if self.auth_token == "":
            self.login()
        headers = {
                "Authorization": f"Bearer {self.auth_token}"
                }
        self.client.get(
            "/graphs/most-attended-certifications",
            params={"limit": 10, "target_period": "last_year"},
            headers=headers
            )


class MeTest(ProtectedRoutesSetUp):
    @task
    def me_load_test(self):
        if self.auth_token == "":
            self.login()
        headers = {
                "Authorization": f"Bearer {self.auth_token}"
                }
        self.client.get(
            "/me",
            headers=headers
            )
