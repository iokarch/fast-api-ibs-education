import os.path
import zipfile

from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse

from app.core import CustomException
from app.models import SAVE_PATH, FileStorage, file_storage_db_get, file_storage_db_add, file_storage_db_get_last_id


router = APIRouter(tags=["API для хранения файлов"])

"""
Задание_5. API для хранения файлов

a.	Написать API для добавления(POST) "/upload_file" и скачивания (GET) "/download_file/{id}" файлов. 
В ответ на удачную загрузку файла должен приходить id для скачивания. 
b.	Добавить архивирование к post запросу, то есть файл должен сжиматься и сохраняться в ZIP формате.
с*.Добавить аннотации типов.
"""
@router.post("/upload_file", description="Задание_5. API для хранения файлов")
async def upload_file(file: UploadFile) -> int:
    """
    Принимает загружаемый файл, который архивируется и сохраняется в директории.\n
    Возвращает идентификатор для скачивания при удачной загрузке файла.
    """

    # Полное имя файла с форматом (прим. text.txt)
    full_file_name = file.filename
    
    # Имя файла без формата (прим. text)
    file_name = '.'.join(file.filename.split(".")[:-1])

    # Имя файла с разрешением архива (прим. text.zip)
    full_zip_file_name = file_name+".zip"

    # Если файл существует в директории, то к названию файла добавляется " — copy" (прим. text — copy.zip )
    while os.path.exists(SAVE_PATH + full_zip_file_name):
        full_zip_file_name = file_name + " — copy" + ".zip"
        full_file_name = file_name + " — copy." + full_file_name.split(".")[-1]
    
    # Путь сохранения файла
    file_zip_location = SAVE_PATH + full_zip_file_name

    #Сохранение ZIP-архива в директории
    with zipfile.ZipFile(file_zip_location, 'a') as zf:
        with zf.open(full_file_name, "w") as file_obj:
            file_obj.write(file.file.read())

    # Получение нового ID
    file_id = file_storage_db_get_last_id() + 1

    # Добавление файла в базу
    new_file_storage = FileStorage(id=file_id, filename=full_zip_file_name, path=file_zip_location)
    file_storage_db_add(new_file_storage)

    return file_id


@router.get("/download_file/{file_id}", description="Задание_5. API для хранения файлов")
async def download_file(file_id: int) -> FileResponse:
    """
    Принимает идентификатор файла для скачивания.\n
    Возвращает ссылку на скачивание файла, если файл нашелся по идентификатору.
    """
    
    file_storage = file_storage_db_get(file_id)

    if not file_storage:
        raise CustomException(detail="File not found!", status_code=404)

    file_path = file_storage.path
    file_name = file_storage.filename

    # проверка на нахождение файла в бд
    if not file_path:
        raise CustomException(detail="File not found!", status_code=404)
    
    # проверка на нахождение файла в бд
    if not os.path.exists(file_path):
        raise CustomException(detail="File not found!", status_code=404)    
    
    file = FileResponse(path=file_path, filename=file_name, media_type='multipart/form-data')
    return file
