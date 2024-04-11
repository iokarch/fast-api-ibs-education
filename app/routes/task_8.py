from fastapi import APIRouter
from functools import wraps

from app.models import CountModel


router = APIRouter(tags=["Стажировка"])

count_model = CountModel()

"""
Задание_8. Декоратор - счётчик запросов.

Напишите декоратор который будет считать кол-во запросов сделанных к приложению.
Оберните роут new_request() этим декоратором.
Подумать, как хранить переменную с кол-вом сделаных запросов.
"""
def count_requests(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        
        count_model.count += 1

        return await func(*args, **kwargs)
    return wrapper


@router.get("/new_request", description="Задание_8. Декоратор - счётчик запросов.")
@count_requests
async def new_request():
    """Возвращает кол-во сделанных запросов."""
    count = count_model.count
    return count
