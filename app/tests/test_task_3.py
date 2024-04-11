from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_1():
    '''
    Ожидаемый выход: возвращение тело запроса c рассчитанным adult = true
    '''
    response = client.post(
        '/check_json',
        json =  {
            "user": {
                "name": "Ivan",
                "age": 23,
                "adult": None,
                "message": None
            },
            "meta": {
                "last_modfication": "20/05/2023",
                "list_of_skills": ["быстрый", "смелый"],
                "mapping": {
                    "list_of_ids": ["один", 2],
                    "tags": ["Стажировка"]
                }
            }
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "user": {
            "name": "Ivan",
            "age": 23,
            "adult": True,
            "message": None
        },
        "meta": {
            "last_modfication": "20/05/2023",
            "list_of_skills": ["быстрый", "смелый"],
            "mapping": {
                "list_of_ids": ["один", 2],
                "tags": ["Стажировка"]
            }
        }
    }

def test_2():
    '''
    Ожидаемый выход: возвращение тело запроса c полями adult = false и message = None
    '''
    response = client.post(
        '/check_json',
        json =  {
            "user": {
                "name": "Egor",
                "age": 17,
                "message": "Hello, World!"
            },
            "meta": {
                "last_modfication": "15/10/2015",
                "mapping": {
                    "list_of_ids": ["один", 2],
                    "tags": ["Стажировка"]
                }
            }
        }
    )
    assert response.status_code == 200
    assert response.json() == {
        "user": {
            "name": "Egor",
            "age": 17,
            "adult": False,
            "message": "Hello, World!"
        },
        "meta": {
            "last_modfication": "15/10/2015",
            "list_of_skills": None,
            "mapping": {
                "list_of_ids": ["один", 2],
                "tags": ["Стажировка"]
            }
        }
    }

def test_3():
    '''
    Ожидаемый выход: обрабатываемая ошибка 422
    '''
    response = client.post(
        '/check_json',
        json =  {
            "user": {
                "name": "Mihail",
                "age": -12
            }
        }
    )
    assert response.status_code == 422
