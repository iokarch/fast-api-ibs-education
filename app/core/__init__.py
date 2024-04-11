import os
import json
import shutil
import pandas as pd

from fastapi import HTTPException
from abc import ABC, abstractmethod
from io import StringIO
from pandas.api.types import is_string_dtype, is_numeric_dtype

from app.models import FileStorage, file_storage_db_add, file_storage_db_get, file_storage_db_get_last_id


class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)

def convert_arabic_to_roman(number: int) -> str:
    """
    Переводит арабское число [1..3999] в римское.
    Возращает римское число в виде строки
    """
    # Словарь соотвествий арбаских и римских чисел
    map_arabic = {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC', 50: 'L', 40: 'XL', 10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'}
    
    # Проверка на диапазон [1..3999]
    if (number < 1 or number > 3999):
        return "не поддерживается"
    
    # Вычисление арабского числа в римское
    roman_numeral = ''
    for arabic_value, roman_symbol in map_arabic.items():
        while number >= arabic_value:
            roman_numeral += roman_symbol
            number -= arabic_value
    return roman_numeral

def check_correct_roman_number(number: str) -> bool:
    """
    Проверяет правильность написания римского числа.
    Возвращает булевое значение
    """
    # Словарь повторений разрядов в римском числе
    symbols_repeat = {"I": 0, "V": 0, "X": 0, "L": 0, "C": 0, "D": 0, "M": 0}
    # Словарь соотвествий римских и арабских чисел
    map_roman = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

    for count in range(len(number)):
        letter = number[count]
        # Проверка на наличие символа в базе разрядов
        if letter in symbols_repeat:
            if symbols_repeat[letter] == 0:
                letter_count = number.count(letter)
                # Ошибка, если один из разрядов (X, C, M) повторился больше 4-х раз 
                if (letter_count > 4) and letter in ["X", "C", "M"]:
                    return False
                # Ошибка, если разряд (I) повторился больше 3-х раз 
                if (letter_count > 3) and letter == "I":
                    return False
                # Ошибка, если разряды V, L, D повторились больше одного раза
                if (letter_count > 1 and letter in ["V", "L", "D"]):
                    return False
                symbols_repeat[letter] = letter_count
        else:
            return False
    
    for letter in symbols_repeat:
        # Разряды I должны быть друг за другом
        if symbols_repeat[letter] > 0 and not letter*symbols_repeat[letter] in number and letter == "I":
            return False
        # Если в числе 3 разряда X, C, M - 2 из них должны быть другом за другом
        if symbols_repeat[letter] == 3 and not letter*2 in number and letter in ["X", "C", "M"]:
            return False
        # Если в числе 4 разряда X, C, M - 3 из них должны быть другом за другом
        if symbols_repeat[letter] == 4 and not letter*3 in number and letter in ["X", "C", "M"]:
            return False
        # 4 разряда X, C, M не должны стоять друг за другом
        if symbols_repeat[letter] == 4 and letter*4 in number and letter in ["X", "C", "M"]:
            return False
    
    # Проверка построения римского числа
    for index, letter in enumerate(number):
        if index > 0:
            prev_letter = number[index - 1]
            if map_roman[letter] > map_roman[prev_letter]:
                # V, L, D никогда не вычитают
                if prev_letter in ["V", "L", "D"]:
                    return False
                # Если вычитаемый разряд I, то он должен находится в предпоследней позиции в римском числе
                if prev_letter == "I" and prev_letter != number[-2]:
                    return False
                # Ошибка при вычитании, если один разряд больше другого в 10 раз
                if map_roman[letter] / map_roman[prev_letter] > 10:
                    return False
                if index - 2 >= 0:
                    prev_prev_letter = number[index - 2]
                    # За один раз можно вычесть только один разряд
                    if map_roman[prev_prev_letter] <= map_roman[prev_letter]:
                        return False
    return True

def convert_roman_to_arabic(number: str) -> int:
    """
    Переводит риское число в арабское.
    Возращает арабское целочисленное число
    """
    # Словарь соотвествий римских и арабских чисел
    map_roman = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

    # Проверка римского числа на корректность
    if not check_correct_roman_number(number):
        return 0
    
    # Вычисление римского числа в арабское
    arabic_numeral = 0
    for index in range(len(number)):
        if index > 0 and map_roman[number[index]] > map_roman[number[index - 1]]:
            arabic_numeral += map_roman[number[index]] - 2 * map_roman[number[index - 1]]
        else:
            arabic_numeral += map_roman[number[index]]
    return arabic_numeral

def check_correct_csv_file(data: pd.DataFrame) -> bool:
    """
    Проверяет csv-файл на валидность
    """

    # Проверка на соответсвие названий колонок
    keys = data.columns.tolist()
    if (keys != ['Имя', 'Возраст', 'Должность']):
        return False
    
    # Проверка аннотаций типов столбцов
    if not is_string_dtype(data['Имя']) \
        or not is_numeric_dtype(data['Возраст']) \
        or not is_string_dtype(data['Должность']):
        return False

    return True

def average_age_by_position(file):
    """
    Принимает csv-файл с сотрудниками компании с колонками "Имя", "Возраст", "Должность". 
    Возвращает словарь с ключами уникальных должностей и значениями среднего возраста сотрудников по каждой должности
    """

    # Попытка парсинга файла
    try:
        data = pd.read_csv(file.file)
    except Exception:
        raise CustomException(detail="Невалидный файл", status_code=400)

    # Проверка на валидность
    if not check_correct_csv_file(data):
        raise CustomException(detail="Невалидный файл", status_code=400)
    
    # Словарь уникальных должностей
    dict_of_post = dict.fromkeys(data["Должность"].tolist(), None)

    # Рассчет среднего возраста сотрудников по должностям
    for post in dict_of_post:
        mean = data[data['Должность'] == post][['Возраст']].mean().tolist()[0]
        # Проверка на пустое значение
        if (pd.isna(mean)):
            continue
        dict_of_post[post] = mean
    
    return dict_of_post


"""
Задание_6.
Дан класс DataGenerator, который имеет два метода: generate(), to_file()
Метод generate генерирует данные формата list[list[int, str, float]] и записывает результат в
переменную класса data
Метод to_file сохраняет значение переменной generated_data по пути path c помощью метода
write, классов JSONWritter, CSVWritter, YAMLWritter.

Допишите реализацию методов и классов.
"""
class BaseWriter(ABC):
    """Абстрактный класс с методом write для генерации файла"""

    @abstractmethod
    def write(self, data: list[list[int, str, float]]) -> StringIO:
        """
        Записывает данные в строковый объект файла StringIO
        :param data: полученные данные
        :return: Объект StringIO с данными из data
        """
        pass


class JSONWriter(BaseWriter):
    """Потомок BaseWriter с переопределением метода write для генерации файла в json формате"""

    def write(self, data: list[list[int, str, float]]) -> StringIO:
        json_data : dict = {"matrix": []}
        for row in range(len(data)):
            row_data = {"row": row + 1, 'content': data[row]}
            json_data["matrix"].append(row_data)

        file = StringIO()
        json.dump(json_data, file)
        return file


class CSVWriter:
    """Потомок BaseWriter с переопределением метода write для генерации файла в csv формате"""

    def write(self, data: list[list[int, str, float]]) -> StringIO:
        csv_data : str = ""
        csv_data += ",".join(["column_" + str(i + 1) for i in range(len(data))]) + "\n"
    
        for row in range(len(data)):
            csv_data += ",".join([str(item) for item in data[row]])
            if row < len(data) - 1:
                csv_data += "\n"

        file = StringIO()
        file.write(csv_data)
        return file


class YAMLWriter:
    """Потомок BaseWriter с переопределением метода write для генерации файла в yaml формате"""

    def write(self, data: list[list[int]]) -> StringIO:
        yaml_data = "matrix:\n"

        for row in range(len(data)):
            yaml_data += f" row_{row + 1}: {data[row]}"
            if row < len(data) - 1:
                yaml_data += "\n"

        file = StringIO()
        file.write(yaml_data)
        return file


class DataGenerator:
    def __init__(self, data: list[list[int, str, float]] = None):
        self.data: list[list[int, str, float]] = data
        self.file_id = None

    def generate(self, matrix_size) -> None:
        """Генерирует матрицу данных заданного размера."""

        data: list[list[int, str, float]] = []
        
        ''' Пример матрицы 5x5:
            [[0, 1, 2, 3, 4], 
            [1, 2, 3, 4, 5], 
            [2, 3, 4, 5, 6], 
            [3, 4, 5, 6, 7], 
            [4, 5, 6, 7, 8]]
        '''

        # Генерация матрицы
        for index_1 in range(matrix_size):
            dot_data = []
            for index_2 in range(matrix_size):
                dot_data.append(index_1 + index_2)
            data.append(dot_data)

        self.data = data

    def to_file(self, path: str, writer) -> None:
        """
        Метод для записи в файл данных полученных после генерации.
        Если данных нет, то вызывается кастомный Exception.
        :param path: Путь куда требуется сохранить файл
        :param writer: Одна из реализаций классов потомков от BaseWriter
        """

        if self.data == None:
            raise CustomException(detail="Matrix missing error", status_code=404)

        file = None

        # Запись матрицы в заданном формате
        if writer == 'json':
            file = JSONWriter().write(self.data)
        elif writer == 'csv':
            file = CSVWriter().write(self.data)
        elif writer == 'yaml':
            file = YAMLWriter().write(self.data)
        else:
            raise CustomException(detail="The file format is set incorrectly", status_code=400)
        
        if file == None:
            raise CustomException(detail="File missing error", status_code=400)
        
        file_name = 'file with matrix'
        file_format = '.' + writer

        while os.path.exists(path + file_name + file_format):
            file_name = file_name + " — copy"

        file_location = path + file_name + file_format

        with open(file_location, mode='w') as file_obj:
            file.seek(0)
            shutil.copyfileobj(file, file_obj)

        self.file_id: int = file_storage_db_get_last_id() + 1

        new_file_storage = FileStorage(id=self.file_id, filename=file_name+file_format, path=file_location)
        file_storage_db_add(new_file_storage)
