from fastapi import APIRouter, Response

router = APIRouter(tags=["Стажировка"])

"""
Задание_8. Декоратор - счётчик запросов.

Напишите декоратор который будет считать кол-во запросов сделанных к приложению.
Оберните роут new_request() этим декоратором.
Подумать, как хранить переменную с кол-вом сделаных запросов.
"""
def count_requests():
    pass


@router.get("/new_request", description="Задание_8. Декоратор - счётчик запросов.")
async def new_request():
    """Возвращает кол-во сделанных запросов."""

    return Response()
