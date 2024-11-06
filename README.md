# Django CRUD Task

## Описание технического задания
Тестовый проект на Django, демонстрирующий реализацию CRUD операций с различными типами связей между моделями, WebSocket интеграцию и REST API.

### Основные функциональности
- CRUD операции для различных сущностей
- Демонстрация связей между моделями:
  1) One-to-One (Product -> Manufacturer)
  2) One-to-Many (Category -> Products)
  3) Many-to-One (Products -> Category)
  4) Many-to-Many (Customer <-> Products)
- WebSocket уведомления при CRUD операциях
- REST API с документацией
- Веб-интерфейс для тестирования функциональности
- Docker контейнеризация
- Тестовая страница для WebSocket подключений

## Технологический стек
### Backend
- Python 3.11
- Django 5.1.3
- Django REST Framework
- Django Channels (WebSocket)
- drf-yasg (Swagger/OpenAPI)

### База данных
- PostgreSQL 13
- Redis 6 (для WebSocket)

### Дополнительные инструменты
- Docker & Docker Compose
- WhiteNoise (для статических файлов)
- Daphne (ASGI сервер)

## Структура проекта
```
Django_CRUD_Task/
├── docker/                     # Docker конфигурации
│   └── backend/
│       ├── Dockerfile
│       └── entrypoint.sh
├── scripts/                    # Вспомогательные скрипты
│   └── wait-for-it.sh
├── src/                       # Исходный код Django
│   ├── crud_website/         # Основной проект
│   ├── shop/                 # Приложение магазина
│   ├── static/               # Статические файлы
│   ├── templates/            # HTML шаблоны
│   └── manage.py
├── .env                      # Переменные окружения
├── .env.example              # Пример переменных окружения
├── docker-compose.yml        # Docker Compose конфигурация
└── requirements.txt          # Python зависимости
```

## Установка и запуск
### Предварительные требования
- Docker Desktop
- Git

### Шаги по установке
1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd Django_CRUD_Task
```

2. Создайте и настройте .env файл:
```bash
cp .env.example .env
# Отредактируйте .env файл
```

3. Запустите проект:
```bash
docker-compose build
docker-compose up -d
```

## Доступ к приложению
После запуска доступны следующие URL:
- Главная страница (редирект на API): http://localhost:8000/
- Admin панель: http://localhost:8000/admin/
- API документация: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- WebSocket тест: http://localhost:8000/ws-test/

## API Endpoints

### Categories
- Основные операции:
  - GET /api/v1/categories/ - Список всех категорий
  - POST /api/v1/categories/ - Создать категорию
  - GET /api/v1/categories/{id}/ - Получить категорию
  - PUT /api/v1/categories/{id}/ - Обновить категорию
  - DELETE /api/v1/categories/{id}/ - Удалить категорию
- Дополнительные endpoints:
  - GET /api/v1/categories/with-products/ - Категории с продуктами
  - GET /api/v1/categories/{id}/products/ - Продукты в категории

### Products
- Основные операции:
  - GET /api/v1/products/ - Список всех продуктов
  - POST /api/v1/products/ - Создать продукт
  - GET /api/v1/products/{id}/ - Получить продукт
  - PUT /api/v1/products/{id}/ - Обновить продукт
  - DELETE /api/v1/products/{id}/ - Удалить продукт
- Дополнительные endpoints:
  - GET /api/v1/products/in-stock/ - Продукты в наличии
  - GET /api/v1/products/{id}/fans/ - Покупатели, добавившие в избранное
  - PATCH /api/v1/products/{id}/update-stock/ - Обновить количество

### Customers
- Основные операции:
  - GET /api/v1/customers/ - Список всех покупателей
  - POST /api/v1/customers/ - Создать покупателя
  - GET /api/v1/customers/{id}/ - Получить покупателя
  - PUT /api/v1/customers/{id}/ - Обновить покупателя
  - DELETE /api/v1/customers/{id}/ - Удалить покупателя
- Дополнительные endpoints:
  - GET /api/v1/customers/active/ - Активные покупатели
  - POST /api/v1/customers/{id}/toggle-favorite/ - Добавить/удалить из избранного
  - GET /api/v1/customers/{id}/favorites/ - Список избранных продуктов

### Manufacturers
- Основные операции:
  - GET /api/v1/manufacturers/ - Список всех производителей
  - POST /api/v1/manufacturers/ - Создать производителя
  - GET /api/v1/manufacturers/{id}/ - Получить производителя
  - PUT /api/v1/manufacturers/{id}/ - Обновить производителя
  - DELETE /api/v1/manufacturers/{id}/ - Удалить производителя
- Дополнительные endpoints:
  - GET /api/v1/manufacturers/by-country/ - Фильтр по странам
  - PATCH /api/v1/manufacturers/{id}/update-contacts/ - Обновить контакты

## WebSocket Events
Проект поддерживает следующие WebSocket события:
- Создание объекта
- Обновление объекта
- Удаление объекта
- Уведомления о действиях с избранным

## Автор
Аскарбек Алмазбек уулу