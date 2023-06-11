from typing import Optional
from jwt import InvalidTokenError
from kink import di
from fastapi import FastAPI, UploadFile, status, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

from app.config import Config
from app.application.service import IBMDashboardService
from app.application.dtos import AuthRequestDTO, SignUpRequestDTO
from app.application.errors import UserAlreadyExistsError, InvalidEmailError,\
    UserCreationError, InvalidPasswordError, UserDoesNotExistError, \
    ProcessedFileCreationError, InvalidFileTypeError, \
    InternalDatasetCreationError

PUBLIC_ROUTES = ["/login", "/signup", "/docs", "/openapi.json"]
A_WEEK_IN_SECONDS = 604800

app = FastAPI()


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(Config.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


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
        token: Optional[str] = request.headers.get(
            "authorization").split(" ")[1]

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
        return build_json_failure_response(
            status.HTTP_400_BAD_REQUEST,
            "NO_FILE_UPLOADED"
        )

    content = await file.read()

    try:
        result = service.upload_internal_dataset(file.filename, content)
        return build_json_success_response(
            status_code=status.HTTP_201_CREATED,
            content=result.dict()
        )
    except ProcessedFileCreationError:
        return build_json_failure_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "FAILED_PROCESSING_FILE"
        )
    except InvalidFileTypeError:
        return build_json_failure_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "INVALID_FILE_TYPE_ERROR"
        )
    except InternalDatasetCreationError:
        return build_json_failure_response(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "INTERNAL_DATASET_CREATION_ERROR"
        )
    return build_json_failure_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "'UNEXPECTED_ERROR"
    )


@app.post("/signup")
async def signup(
        req: SignUpRequestDTO,
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
    try:
        user = request.state.user
        result = service.get_user_by_id(user.id)
        return build_json_success_response(
            status.HTTP_200_OK,
            result.dict()
        )
    except UserDoesNotExistError:
        return build_json_failure_response(
            status.HTTP_404_NOT_FOUND,
            "USER_DOES_NOT_EXIST"
        )
    return build_json_failure_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR,
        "UNEXPECTED_ERROR"
    )


@app.get("/graphs/most-attended-certifications")
async def get_most_attended_certifications(
        limit: int,
        target_period: str,
        service: IBMDashboardService = Depends(lambda: di[IBMDashboardService])
):
    response = service.get_most_attended_certifications(target_period, limit)

    return build_json_success_response(
        status.HTTP_200_OK,
        response
    )


@app.get("/graphs/matched-certifications")
async def get_percentage_of_matched_certifications(
        service: IBMDashboardService = Depends(lambda: di[IBMDashboardService])
):
    response = service.get_percentage_of_matched_certifications()

    return build_json_success_response(
        status.HTTP_200_OK,
        response
    )


@app.get("/graphs/top-industry-courses")
@cache(expire=A_WEEK_IN_SECONDS)
async def get_top_industry_courseS(service: IBMDashboardService =
                                   Depends(lambda: di[IBMDashboardService])):
    response = service.get_top_industry_courses()

    return build_json_success_response(
        status.HTTP_200_OK,
        response
    )


@app.get("/graphs/certifications-taken-over-the-years")
async def get_certifications_taken_over_the_years(
        service: IBMDashboardService = Depends(lambda: di[IBMDashboardService])
):
    response = service.get_certifications_taken_over_the_years()
    return build_json_success_response(
        status.HTTP_200_OK,
        response
    )


@app.get("/graphs/certifications-categorized")
async def get_certifications_categorized(
        service: IBMDashboardService = Depends(lambda: di[IBMDashboardService])
):
    response = service.get_certifications_categorized()
    return build_json_success_response(
        status.HTTP_200_OK,
        response
    )


@app.get("/graphs/employees/{employee_id}/certifications-categorized")
async def get_employee_certifications_categorized(
        employee_id: str,
        service: IBMDashboardService = Depends(lambda: di[IBMDashboardService])
):
    response = service.get_employee_certifications_categorized(employee_id)
    return build_json_success_response(
        status.HTTP_200_OK,
        response
    )


@app.get("/graphs/certifications-distribution")
async def get_certifications_distribution(
        service: IBMDashboardService = Depends(lambda: di[IBMDashboardService])
):
    response = service.get_certifications_distribution()
    return build_json_success_response(
        status.HTTP_200_OK,
        response
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


allowed_origins = [Config.CLIENT_URL, Config.CLIENT_URL_LOCAL]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=Config.CLIENT_URL_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
