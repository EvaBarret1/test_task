from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    balance = db.Column(db.Float)

    def __init__(self, username, balance):
        self.username = username
        self.balance = balance

    def update_balance(self, amount):
        self.balance += amount
        db.session.commit()

def fetch_weather(city):
    url = f"https://api.gismeteo.net/v2/weather/current/{city}/"
    headers = {
        "X-Gismeteo-Token": "YOUR_API_TOKEN",
        "Accept-Encoding": "gzip, deflate"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()

        kind = data.get("kind")
        if kind == "Obs":
            temperature = data.get("temperature").get("air").get("C")
            return temperature
        else:
            return None
    else:
        return None

@app.route('/update_balance/<int:user_id>/<city>')
def update_balance(user_id, city):
    temperature = fetch_weather(city)

    if temperature is not None:
        user = User.query.get(user_id)

        if user is not None:
            new_balance = user.balance + temperature
            if new_balance >= 0:
                user.update_balance(temperature)
                return 'Баланс обновлен'
            else:
                return 'Ошибка: баланс не может быть отрицательным'
        else:
            return 'Ошибка: пользователь не найден'
    else:
        return 'Ошибка: не удалось получить данные о погоде'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        users = [
            User('user1', 5000),
            User('user2', 7500),
            User('user3', 10000),
            User('user4', 12500),
            User('user5', 15000)
        ]
        db.session.bulk_save_objects(users)
        db.session.commit()

    app.run()
