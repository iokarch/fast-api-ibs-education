from fastapi import APIRouter

from app.core import DataGenerator
from app.models import SAVE_PATH, FileMatrixGeneration

router = APIRouter(tags=["API для хранения файлов"])

"""
Задание_6. 

Изучите следущие классы в модуле app.core: BaseWriter, DataGenerator

API должно принимать json, по типу:
{
    "file_type": "json",  # или "csv", "yaml"
    "matrix_size": int    # число от 4 до 15
}
В ответ на удачную генерацию файла должен приходить id для скачивания.

Добавьте реализацию методов класса DataGenerator.
Добавьте аннотации типов и (если требуется) модели в модуль app.models.

(Подумать, как переисползовать код из задания 5)
"""
@router.post("/generate_file", description="Задание_6. Конвертер")
async def generate_file(json : FileMatrixGeneration) -> int:
    """
    Принимает json по типу:
    {
    "file_type": "json",  # или "csv", "yaml"
    "matrix_size": int    # число от 4 до 15
    }

    Возвращает id сгенерированного файла для скачивания
    """

    data = DataGenerator()
    data.generate(json.matrix_size)
    data.to_file(SAVE_PATH, json.file_type)
    file_id: int = data.file_id

    return file_id
