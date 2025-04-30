from flask import Flask, render_template
from app.schedule.routes import schedule_bp
from app.shop.routes import shop_bp

app = Flask(__name__)

# Регистрация микросервисов
app.register_blueprint(schedule_bp, url_prefix='/schedule')
app.register_blueprint(shop_bp, url_prefix='/shop')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)