import pytest
import os
import sys

# Добавляем путь к проекту в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == '__main__':
    # Запуск тестов с покрытием
    pytest_args = [
        'tests/',
        '-v',
        '--cov=app',  # Указываем имя вашего основного модуля (без .py)
        '--cov-report=term',
        '--cov-report=html',
        '--log-level=DEBUG'
    ]
    
    exit_code = pytest.main(pytest_args)
    
    # Сохраняем результаты
    with open('tests/test_results.log', 'w') as f:
        f.write(str(exit_code))
    
    os._exit(exit_code)