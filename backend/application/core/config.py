import logging
import os
from pathlib import Path

from pydantic import BaseModel


logger = logging.getLogger(__name__)


class BaseConfig(BaseModel):
    """Config for app that is independent of dev/production requirements

    :param BaseModel: Pydantic BaseModel inheritance model
    :type BaseModel: BaseModel

    Args:
        uri (str | None, optional): Predefined URI to be used.
            Defaults to None.
    """

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    API_V1_STR: str = "/api/v1"
    BASE_PATH: Path = Path(__file__).resolve().parent.parent
    CORS_ORIGINS: list[str] = [
        url.strip() for url in os.getenv("BACKEND_CORS_ORIGINS", "").split(",")
    ]
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "5"))


settings = BaseConfig()


# endpoints to be excluded from request log
# All endpoints that handle files need to be excluded or application will hang
REQUEST_LOG_EXCLUDED_ENDPOINTS: list[str] = []
