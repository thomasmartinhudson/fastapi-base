from fastapi import Request


def create_exception_log_detail(
    request: Request,
    exc: Exception,
) -> dict:
    """Gathers necessary info from request and raised exception"""
    info = {
        "client": getattr(request.client, "host", "n/a"),
        "server": request.get("server", ("n/a", ""))[0],
        "method": request.method,
        "components": request.url.components,
    }
    return {
        "detail": str(exc).strip(),
        "info": info,
    }
