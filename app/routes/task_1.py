from fastapi import APIRouter


router = APIRouter(tags=["Стажировка"])


"""
Задание_1. Удаление дублей
    Реализуйте функцию соответствующую следующему описанию:
    На вход подаётся массив слов зависимых от регистра, для которых необходимо произвести
    фильтрацию на основании дублей слов, если в списке найден дубль по регистру, то все
    подобные слова вне зависимости от регистра исключаются.
    На выходе должны получить уникальный список слов в нижнем регистре.

    Список слов для примера: ['Мама', 'МАМА', 'Мама', 'папа', 'ПАПА', 'Мама', 'ДЯдя', 'брАт', 'Дядя', 'Дядя', 'Дядя']
    Ожидаемый результат: ['папа','брат']
"""
@router.post("/find_in_different_registers", description="Задание_1. Удаление дублей")
async def find_in_different_registers(words: list[str]) -> list[str]:
    """
    Принимает массив слов, зависимых от регистра
    Фильтрует дубли по регистру, исключая все остальные подобные слова, независящих от регистра
    Возвращает уникальных список слов в нижнем регистре, которые прошли фильтрацию
    """

    result = []

    # Список уникальных слов в нижнем регистре
    result = list(dict.fromkeys([item.lower() for item in words]))

    # Список исключенный слов
    ban_words = []

    for index_1, word_1 in enumerate(words):
        if word_1.lower() in ban_words:
            continue
        for index_2, word_2 in enumerate(words):
            if (index_1 == index_2):
                continue
            if (word_1 == word_2):
                if (word_1.lower() in result):
                    result.pop(result.index(word_1.lower()))
                ban_words.append(word_1.lower())
                break

    return result
