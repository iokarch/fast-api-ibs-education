from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_1():
    ''' 4 -> IV '''
    response = client.post(
        '/converter',
        json=4
    )
    assert response.status_code == 200
    assert response.json() == {"arabic": 4, "roman": "IV"}

def test_2():
    ''' 19 -> XIX '''
    response = client.post(
        '/converter',
        json=19
    )
    assert response.status_code == 200
    assert response.json() == {"arabic": 19, "roman": "XIX"}

def test_3():
    ''' 2867 -> MMDCCCLXVII '''
    response = client.post(
        '/converter',
        json=2867
    )
    assert response.status_code == 200
    assert response.json() == {"arabic": 2867, "roman": "MMDCCCLXVII"}

def test_4():
    ''' 0 -> не поддерживается (проверка на неверное арабское число) '''
    response = client.post(
        '/converter',
        json=0
    )
    assert response.status_code == 200
    assert response.json() == {"arabic": 0, "roman": "не поддерживается"}

def test_5():
    ''' 4500 -> не поддерживается (проверка на неверное арабское число) '''
    response = client.post(
        '/converter',
        json=4500
    )
    assert response.status_code == 200
    assert response.json() == {"arabic": 4500, "roman": "не поддерживается"}

def test_6():
    ''' IV -> 4 '''
    response = client.post(
        '/converter',
        json="IV"
    )
    assert response.status_code == 200
    assert response.json() == {"arabic": 4, "roman": "IV"}

def test_7():
    ''' CMX -> 910 '''
    response = client.post(
        '/converter',
        json="CMX"
    )
    assert response.status_code == 200
    assert response.json() == {"arabic": 910, "roman": "CMX"}

def test_8():
    ''' CCCXXXVIII -> 338 '''
    response = client.post(
        '/converter',
        json="CCCXXXVIII"
    )
    assert response.status_code == 200
    assert response.json() == {"arabic": 338, "roman": "CCCXXXVIII"}

def test_9():
    ''' IIV -> 0 (проверка на неверное римское число) '''
    response = client.post(
        '/converter',
        json="IIV"
    )
    assert response.status_code == 200
    assert response.json() == {"arabic": 0, "roman": "IIV"}

def test_10():
    ''' IIIIIXIXCM -> 0 (проверка на неверное римское число) '''
    response = client.post(
        '/converter',
        json="IIIIIXIXCM"
    )
    assert response.status_code == 200
    assert response.json() == {"arabic": 0, "roman": "IIIIIXIXCM"}

def test_11():
    ''' VXI#%$ -> 0 (проверка на неверное римское число) '''
    response = client.post(
        '/converter',
        json="VXI#%$"
    )
    assert response.status_code == 200
    assert response.json() == {"arabic": 0, "roman": "VXI#%$"}