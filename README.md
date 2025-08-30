# 🐱 Cat Charity Fund

Проект **Cat Charity Fund** — это благотворительный фонд с API-интерфейсом для сбора пожертвований и распределения средств по проектам. Реализован на **FastAPI** с использованием **SQLAlchemy**, **SQLite** и **Alembic**.

---

## 🚀 Возможности

- Добавление и редактирование благотворительных проектов
- Создание пожертвований пользователями
- Автоматическое распределение пожертвований по открытым проектам
- Логика автоматического закрытия проектов и донатов
- Валидация данных и защита бизнес-логики
- Асинхронный API с автогенерируемой документацией Swagger/OpenAPI

---

## ⚙️ Технологии

- **Python 3.9+**
- **FastAPI**
- **SQLAlchemy (async)**
- **Alembic**
- **PostgreSQL / SQLite (dev)**
- **Pydantic**
- **Uvicorn**
- **Docker** (опционально)

---

## 📦 Установка и запуск

### 🔧 Локально

1. **Клонируйте репозиторий:**

```bash
git clone https://github.com/your-username/cat_charity_fund.git
cd cat_charity_fund
```

2. **Создайте виртуальное окружение:**

```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
source venv\Scripts\activate  # для Windows
```

3. **Установите зависимости:**

```bash
pip install -r requirements.txt
```

4. **Настройте переменные окружения:**
```bash
Создайте .env файл в корне проекта.
Добавьте следующие константы в .env:
DATABASE_URI=sqlite+aiosqlite:///./fastapi.db # или ссылка на PostgreSQL
SECRET=<Ваш секретный ключ>
PERUSER_EMAIL=root@admin.ru # Email суперпользователя
FIRST_SUPERUSER_PASSWORD=root # Пароль суперпользователя
```

5. **Примените миграции:**

```bash
alembic upgrade head
```

6. **Запустите сервер:**

```bash
uvicorn app.main:app --reload
```

---

## 🔍 Документация

После запуска перейдите в браузере:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 📋 Примеры запросов к API
```bash
1. Создание благотворительного проекта  
POST /charity_projects/ # Только суперюзеры
Request:
{
  "name": "Помощь детям",
  "description": "Сбор средств на лечение детей",
  "full_amount": 100000
}

Response:
{
  "name": "Помощь детям",
  "description": "Сбор средств на лечение детей",
  "full_amount": 100000
}


2. Получение списка всех проектов  
GET /charity_projects/

Response:
[
  {
    "name": "Помощь хвостатым",
    "description": "Сбор средств на корм котам",
    "full_amount": 100000,
    "id": 1,
    "invested_amount": 35000,
    "fully_invested": true,
    "create_date": "2019-08-24T14:15:22Z",
    "close_date": "2019-08-24T14:15:22Z"
  },
  ...
]

3. Обновление проекта  
PATCH /charity_projects/{project_id} # Только суперюзеры

Request:
{
  "description": "Обновленное описание проекта",
  "full_amount": 120000
}

Response:
{
  "id": 1,
  "name": "Помощь детям",
  "description": "Обновленное описание проекта",
  "full_amount": 120000,
  "invested_amount": 25000,
  "fully_invested": false,
  "fully_invested": true,
  "create_date": "2019-08-24T14:15:22Z",
  "close_date": "2019-08-24T14:15:22Z"
}


4. Удаление проекта  
DELETE /charity_projects/{project_id}

Response:
{
  "id": 1,
  "name": "Помощь детям",
  "description": "Обновленное описание проекта",
  "full_amount": 120000,
  "invested_amount": 25000,
  "fully_invested": false,
  "fully_invested": true,
  "create_date": "2019-08-24T14:15:22Z",
  "close_date": "2019-08-24T14:15:22Z"
}
```

---

## 🗃️ Структура проекта

```bash
cat_charity_fund/
├── alembic/                # Миграции базы данных Alembic
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions/           # Скрипты миграций
├── alembic.ini             # Конфигурационный файл Alembic
├── app/                    # Основной код приложения
│   ├── api/                # Роуты (endpoints) FastAPI
│   │   ├── endpoints/      # Конкретные маршруты
│   │   ├── routers.py
│   │   └── validators.py
│   ├── core/               # Основная бизнес-логика и настройки приложения
│   │   ├── base.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── init_db.py
│   │   └── user.py
│   ├── crud/               # CRUD-операции (взаимодействие с БД)
│   │   ├── base.py
│   │   ├── charity_project.py
│   │   └── donation.py
│   ├── models/             # SQLAlchemy-модели (описание таблиц)
│   │   ├── base.py
│   │   ├── charity_project.py
│   │   ├── donation.py
│   │   └── user.py
│   ├── schemas/            # Pydantic-схемы (валидация и сериализация данных)
│   │   ├── base.py
│   │   ├── charity_project.py
│   │   ├── donation.py
│   │   └── user.py
│   ├── services/           # Дополнительная логика (например, инвестирование)
│   │   └── invested.py
│   └── main.py             # Точка входа приложения FastAPI
├── postman_collection/     # Коллекция Postman для тестирования API
│   ├── QRKot.postman_collection.json
│   └── README.md
├── tests/                  # Тесты (Pytest)
│   ├── conftest.py
│   ├── fixtures/
│   ├── test_auth.py
│   ├── test_charity_project.py
│   ├── test_db.py
│   ├── test_donations.py
│   └── test_investment.py
├── requirements.txt        # Зависимости Python
├── openapi.json            # Спецификация API в формате OpenAPI (Swagger)
├── pyproject.toml          # Конфигурация для сборщиков и линтеров (например, Poetry, Black)
├── pytest.ini              # Конфигурация Pytest
├── .env                    # Переменные окружения
├── README.md               # Инструкция по развёртыванию и использованию проекта
├── setup_for_postman.py    # Скрипт для настройки Postman коллекции (если нужен)
├── fastapi.db              # Основная база данных SQLite
├── test.db
```

---

## ✅ Тесты

Для запуска тестов перейдите в корневую директорию проекта и выполните команду:
```bash
pytest
```
Для запуска Postman-коллекции ознакомьтесь с README.md, расположенным в директории с коллекцией.
---

## 📌 Примечания

- Пожертвования автоматически распределяются по проектам согласно дате создания.
- Проекты и донаты автоматически **закрываются**, когда достигнуты нужные суммы.

---

## 🧑‍💻 Автор

- Дмитрий Радюк 
- GitHub: https://github.com/Dzmitry-Radziuk
- Email: mitia.radiuk@yandex.ru
---

## 📄 Лицензия

Проект распространяется под лицензией MIT.
