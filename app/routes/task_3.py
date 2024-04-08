from fastapi import APIRouter

from app.models import BigJson

router = APIRouter(tags=["Стажировка"])

"""
Задание_3. Валидация json

В теле запроса передаётся json. Необходимо проверять его на наличие полей и типов данных.
Поля обязательные, если не написано иное.
Например:
{
    "user": {
        "name": "Ivan",  
        "age": 23,  # не может быть меньше 0 и больше 100 
        "adult": true,  # вычислять на основании возраста
        "message": ""  # необязательное
    },
    "meta": {
        "last_modification": "20/05/2023",  # формат даты должен соответствовать данному формату
        "list_of_skills": ["ловкий", "смелый"], # необязательное
        "mapping": {
            list_of_ids: [1, "два"],
            tags: {"стажировка", }  
        },
    
    }
}

Напишите валидатор в модуле app.models для класса BigJson.

Используйте библиотеку pydantic.

"""
@router.post("/check_json", description="Задание_3. Валидация json")
async def check_json(body: BigJson) -> BigJson:
    """ """

    return body
