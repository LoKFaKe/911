import sqlite3
import pytest
from app import get_schedule, get_faq

@pytest.fixture
def setup_db():
    """Фикстура для настройки тестовой БД"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Создаем тестовые таблицы
    cursor.execute("""
        CREATE TABLE schedule (
            id INTEGER PRIMARY KEY,
            group_name TEXT NOT NULL,
            subject TEXT NOT NULL,
            day TEXT NOT NULL,
            time TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE faq (
            id INTEGER PRIMARY KEY,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)
    
    # Добавляем тестовые данные
    cursor.execute("""
        INSERT INTO schedule (group_name, subject, day, time)
        VALUES ('Группа 201', 'Иностранный язык в профессиональной деятельности', 'Понедельник', '09:00')
    """)
    
    cursor.execute("""
        INSERT INTO faq (question, answer)
        VALUES ('Как найти расписание?', 'Используйте поиск по группе')
    """)
    
    conn.commit()
    yield conn
    conn.close()

def test_get_schedule(setup_db):
    """Тест получения расписания"""
    # Подменяем соединение с БД на тестовое
    original_connect = sqlite3.connect
    sqlite3.connect = lambda _: setup_db
    
    try:
        result = get_schedule('Группа 201')
        assert len(result) == 1
        assert result[0][0] == 'Иностранный язык в профессиональной деятельности'  # subject
        assert result[0][1] == 'Понедельник' # day
        assert result[0][2] == '09:00'       # time
        
        # Проверка для несуществующей группы
        empty_result = get_schedule('Несуществующая группа')
        assert len(empty_result) == 0
    finally:
        sqlite3.connect = original_connect

def test_get_faq(setup_db):
    """Тест получения FAQ"""
    original_connect = sqlite3.connect
    sqlite3.connect = lambda _: setup_db
    
    try:
        result = get_faq()
        assert len(result) == 1
        assert result[0][0] == 'Как найти расписание?'  # question
        assert 'поиск по группе' in result[0][1]       # answer
    finally:
        sqlite3.connect = original_connect