from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests

# Создаем приложение Flask
app = Flask(__name__)

# Конфигурируем базу данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

# Определяем модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float)

with app.app_context():
    # Создаем таблицу в базе данных (если ее нет)
    db.create_all()

# Функция для получения данных о погоде
def fetch_weather(city):
    url = f"https://api.weather.com/v1/current/temperature?city={city}&apiKey=YOUR_API_KEY"
    response = requests.get(url)
    if response.status_code == 200:
        temperature = response.json()['temperature']
        return temperature
    else:
        return None

# Route для обновления баланса пользователя
@app.route('/update_balance/<user_id>/<city>')
def update_balance(user_id, city):
    temperature = fetch_weather(city)

    if temperature is not None:
        user = User.query.get(user_id)

        if user is not None:
            new_balance = user.balance + temperature
            if new_balance >= 0:
                user.balance = new_balance
                db.session.commit()
                return 'Баланс обновлен'
            else:
                return 'Ошибка: баланс не может быть отрицательным'
        else:
            return 'Ошибка: пользователь не найден'
    else:
        return 'Ошибка: не удалось получить данные о погоде'

if __name__ == "__main__":
    # Запускаем веб-приложение Flask
    app.run()
