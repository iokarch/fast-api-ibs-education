from typing import Union
from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo
from datetime import datetime

# Путь для хранения файлов. Задание 5,6
SAVE_PATH = "app/files/save/"

class ConverterRequest(BaseModel):
    number: Union[int, str]


class ConverterResponse(BaseModel):
    arabic: int
    roman: str


class User(BaseModel):
    """
    Информация о пользователе

    :param name: - Имя пользователя
    :param age: - Возраст пользователя [0..100]
    :param adult: - Статус совершеннолетия [age > 18 == true]
    :param message: - Сообщение пользователя (необязательное)
    """
    model_config = {"validate_default": True}

    name: str
    age: int
    adult: bool | None = None
    message: str | None = None

    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if value > 100 or value < 0:
            raise ValueError("Age value must be in [0..100]")
        return value
    
    @field_validator("adult")
    def validate_autofill_adult(cls, v, info: ValidationInfo):
        if "age" not in info.data:
                raise ValueError("User adulthood does not correspond to age!")
        if v != None:
            if v != (info.data["age"] >= 18):
                raise ValueError("User adulthood does not correspond to age!")
            else:
                return v
        return info.data["age"] >= 18


class MetaMapping(BaseModel):
    """
    Мета-отображение

    :param list_of_ids: - Список идентификаторов
    :param tags: - Тэги
    """

    list_of_ids: list[str | int]
    tags: set[str]


class UserMeta(BaseModel):
    """
    Мета пользователя

    :param list_of_ids: - Дата последнего изменения (DD/MM/YYYY)
    :param list_of_ids: - Список качеств
    :param mapping: - Мета-отображение
    """

    last_modfication: str
    list_of_skills: list[str] | None = None
    mapping: MetaMapping

    @field_validator("last_modfication")
    def validate_date_format(cls, value):
        try:
            if value != datetime.strptime(value, "%d/%m/%Y").strftime('%d/%m/%Y'):
                raise ValueError
            return value
        except ValueError:
            raise ValueError("Date must have the format: DD/MM/YYYY")
        

class BigJson(BaseModel):
    """Использует модель User и UserMeta"""
    user: User
    meta: UserMeta


class FileMatrixGeneration(BaseModel):
    """
    Модель файла с записанной матрицей

    :param file_type: - Формат файла (json, csv, yaml)
    :param matrix_size: - Размер матрицы [4..15]
    """
    file_type: str
    matrix_size: int

    @field_validator("matrix_size")
    @classmethod
    def validate_matrix_size(cls, value):
        if value > 15 or value < 4:
            raise ValueError("Matrix size must be in [4..15]")
        return value
    

class FileStorage(BaseModel):
    """
    Хранилище файла

    :param id: - Идентификатор файла
    :param filename: - Имя файла с форматом
    :param path: - Директория файла
    """
    id: int
    filename: str
    path: str


# Фейковая база данных сохраненных файлов
fake_file_storage_db : list[FileStorage] = []


def file_storage_db_add(file: FileStorage) -> None:
    '''Добавляет в бд новую запись FileStorage'''
    if file:
        fake_file_storage_db.append(file)

def file_storage_db_get(request_id: int) -> FileStorage:
    '''Берет запись из базы данных FileStorage'''
    for file in fake_file_storage_db:
        if (request_id == file.id):
            return file
    return None

def file_storage_db_get_last_id() -> int:
    '''Возвращает последний ID из базы данных FileStorage'''
    file_id: int = 0
    for i in fake_file_storage_db:
        print(i.id)
        if i.id > file_id:
            print(i.id)
            file_id = i.id
    return file_id


# class UserRequest(BaseModel):
#     name: str
#     message: str
#
#
# class User(BaseModel):
#     name: str
#     age: str
#     is_adult: bool
#     message: str = None
#
#
# class UserResponse(BaseModel):
#     pass
