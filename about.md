## Использованные паттерны

1. **Factory Method** (для создания приложения):
```python
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    # ... инициализация
    return app
