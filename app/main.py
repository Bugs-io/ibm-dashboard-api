import os
import logging
from uuid import uuid4

import magic
from fastapi import FastAPI, UploadFile, status, HTTPException
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

app = FastAPI()
storage_client = storage.Client()

EXCEL_MIME_TYPE = [
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
]
BUCKET_NAME = os.environ["BUCKET_NAME"]

bucket = storage_client.get_bucket(BUCKET_NAME)


async def cloud_upload(content: bytes, key: str):
    logging.info(f"Uploading file: {key} to cloud bucket")

    blob = bucket.blob(key)
    blob.upload_from_string(content)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/upload")
async def upload(file: UploadFile | None = None):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No file was uploaded"
        )

    content = await file.read()

    file_type = magic.from_buffer(content, mime=True)

    if file_type not in EXCEL_MIME_TYPE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File type is not supported"
        )

    file_name = f"{uuid4()}.xlsx"
    await cloud_upload(content=content, key=file_name)

    return {"file_name": file_name}
