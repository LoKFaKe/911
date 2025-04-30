import pytest
from app import app

@pytest.fixture
def client():
    """Фикстура для тестового клиента"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    """Тест главной страницы"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Учебное расписание' in response.data

def test_schedule_route_post(client):
    """Тест POST запроса к /schedule"""
    response = client.post('/schedule', data={'group_name': 'Группа 201'})
    assert response.status_code == 200

def test_faq_route(client):
    """Тест страницы FAQ"""
    response = client.get('/faq')
    assert response.status_code == 200
    assert b'Частые вопросы' in response.data

def test_schedule_route_get(client):
    """Тест недопустимого GET запроса к /schedule"""
    response = client.get('/schedule')
    assert response.status_code == 405  # Method Not Allowed