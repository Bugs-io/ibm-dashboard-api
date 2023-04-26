from os import getenv
from fastapi import FastAPI, UploadFile, status, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from kink import di
from typing import Optional
from jwt import InvalidTokenError

from app.application.service import IBMDashboardService
from app.application.dtos import AuthRequestDTO
from app.application.errors import UserAlreadyExistsError, InvalidEmailError,\
    UserCreationError, InvalidPasswordError, UserDoesNotExistError

PUBLIC_ROUTES = ["/login", "/signup"]

app = FastAPI()

origins = [
    getenv("CLIENT_URL")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def auth_middleware(
        request: Request,
        call_next,
        service: IBMDashboardService = di[IBMDashboardService]
):
    if request.url.path in PUBLIC_ROUTES:
        response = await call_next(request)
        return response
    
    token = None
    if request.headers.get("authorization"):
        token: Optional[str] = request.headers.get("authorization").split(" ")[1]
    if token is None:
        return build_json_failure_response(
                status.HTTP_401_UNAUTHORIZED,
                "NOT_AUTHENTICATED"
                )

    try:
        payload = service.token_manager.validate_token(token)
        user_id = payload.get("user_id")
        user = service.user_repository.get_by_id(user_id)

        request.state.user = user
    except InvalidTokenError:
        return build_json_failure_response(
                status.HTTP_401_UNAUTHORIZED,
                "INVALID_TOKEN"
                )
    except UserDoesNotExistError:
        return build_json_failure_response(
                status.HTTP_401_UNAUTHORIZED,
                "USER_DOES_NOT_EXIST"
                )

    response = await call_next(request)
    return response


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
    result = service.upload_files(file.filename, content)
    return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=result.dict()
            )


@app.post("/signup")
async def signup(
        req: AuthRequestDTO,
        service: IBMDashboardService = Depends(lambda: di[IBMDashboardService])
):
    try:
        result = service.signup(req)
        return build_json_success_response(
                status.HTTP_201_CREATED,
                result.dict()
                )
    except UserAlreadyExistsError:
        return build_json_failure_response(
                status.HTTP_409_CONFLICT,
                "USER_ALREADY_EXISTS"
                )
    except InvalidEmailError:
        return build_json_failure_response(
                status.HTTP_400_BAD_REQUEST,
                "INVALID_EMAIL"
                )
    except UserCreationError:
        return build_json_failure_response(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "USER_CREATION_ERROR"
                )

    return build_json_failure_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "UNEXPECTED_ERROR"
            )

@app.post("/login")
async def login(
        req: AuthRequestDTO,
        service: IBMDashboardService = Depends(lambda: di[IBMDashboardService])
):
    try:
        result = service.login(req)
        return build_json_success_response(
                status.HTTP_200_OK,
                result.dict()
                )
    except UserDoesNotExistError:
        return build_json_failure_response(
                status.HTTP_404_NOT_FOUND,
                "USER_DOES_NOT_EXIST"
                )
    except InvalidPasswordError:
        return build_json_failure_response(
                status.HTTP_401_UNAUTHORIZED,
                "INVALID_PASSWORD"
                )
    return build_json_failure_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "UNEXPECTED_ERROR"
            )


@app.get("/me")
async def me(
        request: Request,
        service: IBMDashboardService = Depends(lambda: di[IBMDashboardService])
):
    user = request.state.user
    result = service.get_user_by_id(user.id)

    return build_json_success_response(
            status.HTTP_200_OK,
            result.dict()
            )


def build_json_success_response(status_code, content) -> JSONResponse:
    return JSONResponse(
            status_code=status_code,
            content=content
            )


def build_json_failure_response(status_code, error_code) -> JSONResponse:
    return JSONResponse(
            status_code=status_code,
            content={"error_code": error_code}
            )
