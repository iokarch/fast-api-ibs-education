import time

import logging
import logging.config
from contextvars import ContextVar

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

FORMAT = '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)-5s | %(exectime)s sec | %(httpmethod)-5s | %(url)-15s | %(status)-8s'

logging.basicConfig(format=FORMAT, 
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)

output_log = logging.getLogger("output")
client_host: ContextVar[str | None] = ContextVar("client_host", default=None)

"""
Задание_7. Логирование в FastAPI с использованием middleware.

Написать конфигурационный файл для логгера "output"
Формат выводимых логов:
[CURRENT_DATETIME] {file: line} LOG_LEVEL - | EXECUTION_TIME_SEC | HTTP_METHOD | URL | STATUS_CODE |
[2023-12-15 00:00:00] {example:62} INFO | 12 | GET | http://localhost/example | 200 |


Дописать класс CustomMiddleware.
Добавить middleware в приложение (app).
"""
class CustomMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        """Load request ID from headers if present. Generate one otherwise."""
        client_host.set(request.client.host)

        start_time = time.time()
        
        # Откоментить, когда идет тестирование
        #  |    |   |   |
        #  V    V   V   V
        # response = await call_next(request)

        try:
            response = await call_next(request)
        except:
            response = Response("Internal Server Error", status_code=500)

        process_time = time.time() - start_time
        response.headers["process-time"] = str(process_time)

        d = {'exectime': f"{process_time}", 
             'httpmethod': f"{request.method}", 
             'url': f"{request.url}", 
             'status': f"{response.status_code}"}
        
        output_log.info("%s", extra=d)

        return response
