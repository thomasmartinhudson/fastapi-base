import logging

from fastapi import APIRouter, Response


logger = logging.getLogger(__name__)

api_v1_router = APIRouter()


@api_v1_router.get("/health-check", tags=["Development"])
def health_check() -> Response:
    """Health Check Endpoint"""
    return Response(
        status_code=200,
        content="Health Check Successful",
    )
