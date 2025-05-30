# Random User App

Приложение на FastAPI для загрузки, 
отображения и управления случайными 
пользователями с внешнего API
[randomuser.me](https://randomuser.me/).  
Поддерживает хранение данных в PostgreSQL, 
пагинацию, Jinja2-шаблоны и 
подробный просмотр каждого пользователя.

---

## Стек технологий

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker + Docker Compose
- Jinja2
- Pytest (+ aioresponses для mock)

---

## Почему FastAPI

**Выбор FastAPI обоснован следующими техническими характеристиками:**

- **Асинхронная обработка запросов.**
  - Поддержка async/await позволяет эффективно работать с внешними API и высоконагруженными базами данных.
- **Высокая скорость разработки.**
  - Декларативный стиль, автоматическая генерация OpenAPI-спецификаций и документации на основе схем Pydantic.
- **Совместимость с современным стеком.**
  - FastAPI хорошо интегрируется с SQLAlchemy, Jinja2, Pytest и Docker.
- FastAPI использует **Pydantic** для валидации и сериализации данных, что обеспечивает строгую типизацию и меньше шаблонного кода.

## Установка локальная

1. Клонируйте репозиторий:
    ```bash
    git clone <URL_вашего_репозитория>
    cd random_user_app
    ```

2. Создайте виртуальное окружение:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Для Linux/Mac
    venv\Scriptsctivate     # Для Windows
    ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4. Настройте переменные окружения:
    - Создайте файл `.env` в корне проекта.
    - Пример содержимого лежит в .env.example

5. Создание базы данных
   - Если не используется Docker, перед запуском нужно вручную создать базу
   ```bash
    psql -U postgres -h localhost -c "CREATE DATABASE randomuser_db;"
    ```
   
6. Запустите сервер разработки: 
    ```bash
    uvicorn app.main:app --reload
    ```

## Запуск через Docker

1. Запустите контейнеры с помощью Docker Compose:
   ```bash
   docker-compose up --build
   ```
2. Открой браузер:
http://localhost:8000

## Тестирование
1. Тесты включают:
API /users, /user/{id}, /random
Загрузку через fetch_users() с моками
Тестирование бизнес-логики без обращения к реальному API
    ```bash
   pytest
   ```
---

## Структура маршрутов (URL)

| URL                          | Метод | Тип        | Назначение                                                                 |
|-----------------------------|-------|------------|----------------------------------------------------------------------------|
| `/`                         | GET   | HTML       | Главная страница. Таблица с пользователями и кнопка загрузки              |
| `/load`                     | POST  | redirect   | Загружает указанное количество пользователей с API                        |
| `/users?skip=0&limit=10`    | GET   | JSON       | Список пользователей (REST API, пагинированный)                           |
| `/user/{user_id}`           | GET   | JSON       | Данные конкретного пользователя по ID (для API)                           |
| `/user/{user_id}`           | GET   | HTML       | HTML-страница с подробной информацией о пользователе                      |
| `/random`                   | GET   | JSON       | Возвращает случайного пользователя из БД                                  |

 `/user/{id}` возвращает **HTML**, если открыт в браузере, и **JSON**, если используется как API.

## Пример запросов
Получить 10 пользователей (API):
```http
GET /users?skip=0&limit=10