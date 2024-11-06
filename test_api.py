import requests
import json
from requests.auth import HTTPBasicAuth

BASE_URL = 'http://localhost:8000/api/v1'
# Учетные данные для аутентификации
USERNAME = 'admin'  # Замените на свой логин
PASSWORD = 'Uzgen13054$'  # Замените на свой пароль

def test_api():
    # Создаем сессию для сохранения аутентификации
    session = requests.Session()
    session.auth = HTTPBasicAuth(USERNAME, PASSWORD)

    try:
        # 1. Создание категории
        category_data = {
            "name": "Mobile",
            "description": "Electronic devices and gadgets"
        }
        category_response = session.post(
            f'{BASE_URL}/categories/',
            json=category_data
        )
        category_response.raise_for_status()  # Проверяем статус ответа
        print("Category created:", category_response.json())
        category_id = category_response.json()['id']  # Убрали ['data']

        # 2. Создание производителя
        manufacturer_data = {
            "name": "Samsung",
            "country": "Korea",
            "website": "http://samsung.com",
            "contact_email": "contact@samsung.com",
            "contact_phone": "3424324"
        }
        manufacturer_response = session.post(
            f'{BASE_URL}/manufacturers/',
            json=manufacturer_data
        )
        manufacturer_response.raise_for_status()
        print("Manufacturer created:", manufacturer_response.json())
        manufacturer_id = manufacturer_response.json()['id']  # Убрали ['data']

        # 3. Создание продукта
        product_data = {
            "name": "Smartphone2",
            "description": "Latest model smartphone3",
            "price": "999.99",
            "stock": 100,
            "category": category_id,
            "manufacturer": manufacturer_id,
            "sku": "PHONE0021",
            "is_active": True
        }
        product_response = session.post(
            f'{BASE_URL}/products/',
            json=product_data
        )
        product_response.raise_for_status()
        print("Product created:", product_response.json())
        product_id = product_response.json()['id']  # Убрали ['data']

        # 4. Создание покупателя
        customer_data = {
            "name": "John Doe2",
            "email": "john2@example.com",
            "phone": "98765432210",
            "address": "123 Main St2"
        }
        customer_response = session.post(
            f'{BASE_URL}/customers/',
            json=customer_data
        )
        customer_response.raise_for_status()
        print("Customer created:", customer_response.json())
        customer_id = customer_response.json()['id']  # Убрали ['data']

        # 5. Добавление продукта в избранное покупателя
        favorite_response = session.post(
            f'{BASE_URL}/customers/{customer_id}/toggle-favorite/',
            json={"product_id": product_id}
        )
        favorite_response.raise_for_status()
        print("Added to favorites:", favorite_response.json())

    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        if hasattr(e.response, 'json'):
            print("Response:", e.response.json())

if __name__ == "__main__":
    test_api()