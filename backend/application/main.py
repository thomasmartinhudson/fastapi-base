import logging
import time
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette import status
from starlette.concurrency import iterate_in_threadpool
from starlette.responses import StreamingResponse

from application.api.api_v1.api import api_v1_router
from application.core.config import REQUEST_LOG_EXCLUDED_ENDPOINTS, settings
from application.core.exceptions import create_exception_log_detail
from application.core.logging import setup_logging
from application.docs.docs import APP_DESCRIPTION, TAGS_METADATA


logger = logging.getLogger(__name__)
setup_logging(settings.LOG_LEVEL)


class EndpointFilter(logging.Filter):
    """Filter out healthcheck logging"""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("/api/") == -1


async def aux_set_body(request: Request, body: bytes):
    """Part of workaround to get request body in middleware"""

    async def receive():
        """Part of workaround to get request body in middleware"""
        return {"type": "http.request", "body": body}

    request._receive = receive  # pylint: disable=protected-access


async def aux_get_body(request: Request) -> bytes:
    """Part of workaround to get request body in middleware"""
    body = await request.body()
    await aux_set_body(request, body)
    return body


logging.getLogger("uvicorn.access").addFilter(EndpointFilter())


app = FastAPI(
    title="fastapi-base",
    description=APP_DESCRIPTION,
    version="0.0.1",
    openapi_tags=TAGS_METADATA,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Method to capture service request validation failures and log them

    Args:
        request (Request): FastAPI request object
        exc (RequestValidationError): Validation exception

    Returns:
        JSONResponse: JSON response of the failed validation
    """

    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logger.error(
        "%s: %s",
        str(request.base_url),
        str(exc),
    )
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


# global error handler
@app.middleware("http")
async def global_exception_handler(
    request: Request,
    call_next: Callable[[Request], Awaitable[StreamingResponse]],
):
    """Error handler to capture any internal server error"""
    start_time = time.time()

    # get request body
    # this needs to happen before "await call_next(request)"
    request_body_info = ""
    if not any(
        exclude in request.url.path
        for exclude in REQUEST_LOG_EXCLUDED_ENDPOINTS
    ):
        await aux_set_body(request, await request.body())
        request_body_info = (await aux_get_body(request)).decode()

    try:
        response = await call_next(request)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        log_info = create_exception_log_detail(
            request=request,
            exc=exc,
        )
        logger.critical(exc, exc_info=True)
        logger.info(log_info)
        return JSONResponse(content=log_info, status_code=500)

    response_body_info = ""
    if response.status_code not in {200}:
        # get response body
        response_body = [
            chunk async for chunk in response.body_iterator  # type: ignore
        ]
        response.body_iterator = iterate_in_threadpool(  # type: ignore
            iter(response_body)
        )
        response_body_info = (b"".join(response_body)).decode()  # type: ignore

    process_time = time.time() - start_time

    if "health-check" not in request.url.path:
        logger.info(
            '"%s %s" %s (%ss) [%s] [%s]',
            request.method,
            request.url.path,
            response.status_code,
            f"{process_time:.3f}",
            request_body_info,
            response_body_info,
        )
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(api_v1_router, prefix=settings.API_V1_STR)

# Ensure no redirects with trailing forward slashes
app.router.redirect_slashes = False
