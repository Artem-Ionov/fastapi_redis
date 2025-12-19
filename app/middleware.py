import logging

from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)

async def catch_exceptions_middleware(request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Произошла ошибка в {request.method}, {request.url}: {e}")
        return JSONResponse(status_code=500, content={"detail": "Внутренняя ошибка сервера"})