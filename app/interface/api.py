from fastapi import FastAPI, UploadFile, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from kink import di

from app.application.service import IBMDashboardService

app = FastAPI()


@app.post("/upload-internal-dataset")
async def upload_internal_dataset(
        file: UploadFile | None = None,
        service: IBMDashboardService = Depends(lambda: di[IBMDashboardService])
):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file was uploaded"
            )

    content = await file.read()
    result = service.upload_internal_dataset(file.filename, content)

    return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=result.dict()
            )
