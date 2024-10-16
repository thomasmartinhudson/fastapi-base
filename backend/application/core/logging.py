import logging


def setup_logging(log_level: str) -> None:
    """Create logger for application

    Args:
        log_level (str): Log level (error/debug/info)
    """
    log_levels = {
        "critical": logging.CRITICAL,
        "error": logging.ERROR,
        "warning": logging.WARNING,
        "info": logging.INFO,
        "debug": logging.DEBUG,
        "notset": logging.NOTSET,
    }
    logging.basicConfig(
        level=log_levels.get(log_level.lower(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
