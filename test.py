import time
import random
import requests
import threading

# Список городов для тестирования
cities = ['Moscow', 'London', 'New York', 'Tokyo', 'Sydney']

# Функция для отправки запросов на обновление баланса
def make_request(user_id, city):
    url = f"http://localhost:5000/update_balance/{user_id}/{city}"
    response = requests.get(url)
    print(response.text)

# Функция для запуска тестирования
def test_update_balance():
    users = ['user1', 'user2', 'user3', 'user4', 'user5']

    start_time = time.time()
    end_time = start_time + 60 * 20
    
    while time.time() < end_time:
        user_id = random.choice(users)
        city = random.choice(cities)
        
        # Запуск нового потока для отправки запроса на обновление баланса пользователя
        threading.Thread(target=make_request, args=(user_id, city)).start()
        
        # Пауза для случайного времени (от 0 до 1 секунды)
        time.sleep(random.uniform(0, 1))

    user_id = random.choice(users)
    city = random.choice(cities)
    
    # Отправка 1000 запросов в секунду в случайный момент
    for _ in range(1000):
        threading.Thread(target=make_request, args=(user_id, city)).start()


if __name__ == "__main__":
    # Запуск тестирования
    test_update_balance()
