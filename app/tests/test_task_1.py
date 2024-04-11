from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_1():
    ''' 
    Вход: ["Мама", "МАМА", "Мама", "папа", "ПАПА", "Мама", "ДЯдя", "брАт", "Дядя", "Дядя", "Дядя"]
    Ожидаемый вывод:  ["папа","брат"] 
    '''
    
    response = client.post(
        '/find_in_different_registers',
        json=["Мама", "МАМА", "Мама", "папа", "ПАПА", "Мама", "ДЯдя", "брАт", "Дядя", "Дядя", "Дядя"]
    )
    assert response.status_code == 200
    assert response.json() == ["папа","брат"]

def test_2():
    ''' 
    Вход: ["Ivan", "Slava", "Oleg", "OLEG", "SlavA", "OlEG", "IVAN", "oleG", "IvAn", "Ivan"]
    Ожидаемый вывод:  ["slava","oleg"] 
    '''
    
    response = client.post(
        '/find_in_different_registers',
        json=["Ivan", "Slava", "Oleg", "OLEG", "SlavA", "OlEG", "IVAN", "oleG", "IvAn", "Ivan"]
    )
    assert response.status_code == 200
    assert response.json() == ["slava","oleg"]

def test_3():
    ''' 
    Вход: [] (пустой список)
    Ожидаемый вывод:  []
    '''
    
    response = client.post(
        '/find_in_different_registers',
        json=[]
    )
    assert response.status_code == 200
    assert response.json() == []

def test_4():
    '''
    Вход: ["ivan", "lera", "nastya", "lera", "ivan", "nastya", "MISHA", "MISHA"]
    Ожидаемый вывод:  []
    '''
    
    response = client.post(
        '/find_in_different_registers',
        json=["ivan", "lera", "nastya", "lera", "ivan", "nastya", "MISHA", "MISHA"]
    )
    assert response.status_code == 200
    assert response.json() == []