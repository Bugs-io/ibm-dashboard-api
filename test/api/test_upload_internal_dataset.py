import tempfile
import openpyxl
from pytest_schema import schema


def create_mock_file():
    mock_file = tempfile.NamedTemporaryFile(suffix='.xlsx')
    workbook = openpyxl.Workbook()

    sheet = workbook.active
    sheet["A1"] = "some"
    sheet["B1"] = "header"

    workbook.save(mock_file.name)

    workbook.close()

    return mock_file


def test_upload_internal_dataset(client, bearer_token):
    mock_file = create_mock_file()

    payload = {"file": mock_file}
    headers = {"Authorization": f"Bearer {bearer_token}"}

    response = client.post(
            "/upload-internal-dataset",
            files=payload,
            headers=headers
            )

    assert response.status_code == 201
    assert response.json() == schema({
        "id": str,
        "raw_file_path": str,
        "processed_file_path": str,
        })
