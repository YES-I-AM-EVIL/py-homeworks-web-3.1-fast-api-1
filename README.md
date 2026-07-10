# Ads API — FastAPI Advertisement Service

![Python](https://img.shields.io/badge/Python-3.9-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?logo=sqlalchemy&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-4169E1?logo=postgresql&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.0-E92063?logo=pydantic&logoColor=white)
![Docker](https://img.shields.io/badge/Docker_Compose-3.8-2496ED?logo=docker&logoColor=white)
![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-499CD6?logo=uvicorn&logoColor=white)

REST API-сервис объявлений купли/продажи на **FastAPI** с PostgreSQL в качестве базы данных. Поддерживает полный CRUD-цикл и поиск по полям. Полностью докеризован.

Домашнее задание к лекции «Создание REST API на FastApi» часть 1 (курс Python-разработчика, Нетология). Авторизация и аутентификация в этой части не реализуются — согласно требованиям задания.

---

## Содержание

- [Возможности](#возможности)
- [Стек технологий](#стек-технологий)
- [Модель данных](#модель-данных)
- [API Endpoints](#api-endpoints)
- [Быстрый старт](#быстрый-старт)
- [Запуск через Docker Compose](#запуск-через-docker-compose)
- [Примеры запросов](#примеры-запросов)
- [Структура проекта](#структура-проекта)
- [Технические решения](#технические-решения)

---

## Возможности

- Создание объявлений с валидацией полей через Pydantic
- Получение объявления по ID
- Частичное обновление объявления (PATCH)
- Удаление объявления
- Поиск объявлений по полям `title` и `author` (case-insensitive)
- Автоматическая генерация даты создания
- Автодокументация API: Swagger UI (`/docs`) и ReDoc (`/redoc`)
- Полная докеризация: FastAPI + PostgreSQL в одной команде

---

## Стек технологий

| Компонент | Технология | Назначение |
|-----------|-----------|------------|
| Web-фреймворк | FastAPI | Асинхронный REST API с автоматической документацией |
| ASGI-сервер | Uvicorn | Запуск FastAPI приложения |
| ORM | SQLAlchemy 2.0 | Работа с PostgreSQL |
| База данных | PostgreSQL 13 | Хранение объявлений |
| Валидация данных | Pydantic | Сериализация и валидация request/response |
| Контейнеризация | Docker Compose 3.8 | Оркестрация web + db |

---

## Модель данных

### Advertisement

| Поле | Тип | Описание |
|------|-----|---------|
| `id` | Integer (PK) | Уникальный идентификатор |
| `title` | String(100) | Заголовок объявления (индексируется) |
| `description` | String(500) | Описание |
| `price` | Float | Цена |
| `author` | String(50) | Автор объявления |
| `created_at` | DateTime | Дата создания (автогенерация, UTC) |

---

## API Endpoints

| Метод | Endpoint | Описание | Тело запроса |
|-------|----------|----------|--------------|
| POST | `/advertisement/` | Создание объявления | `AdvertisementCreate` |
| GET | `/advertisement/{ad_id}` | Получение по ID | — |
| PATCH | `/advertisement/{ad_id}` | Обновление | `AdvertisementCreate` |
| DELETE | `/advertisement/{ad_id}` | Удаление | — |
| GET | `/advertisement/` | Поиск по полям (`title`, `author`) | — |
| GET | `/docs` | Swagger UI | — |
| GET | `/redoc` | ReDoc документация | — |

### Схемы данных

**AdvertisementCreate** (для POST/PATCH):
```json
{
  "title": "iPhone 13 Pro",
  "description": "Отличное состояние",
  "price": 65000.0,
  "author": "Иван"
}
```

**AdvertisementResponse** (ответ):
```json
{
  "id": 1,
  "title": "iPhone 13 Pro",
  "description": "Отличное состояние",
  "price": 65000.0,
  "author": "Иван",
  "created_at": "2025-01-15T12:30:00"
}
```

---

## Быстрый старт

### Предварительные требования

- Python 3.9+
- PostgreSQL 13+ (или Docker)

### Локальная установка

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/YES-I-AM-EVIL/py-homeworks-web-3.1-fast-api-1.git
cd py-homeworks-web-3.1-fast-api-1

# 2. Создайте и активируйте виртуальное окружение
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .\.venv\Scripts\activate  # Windows

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Запустите PostgreSQL (если нет локального)
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:13

# 5. Запустите приложение
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Сервис будет доступен на `http://127.0.0.1:8000/`.

Документация API:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

## Запуск через Docker Compose

Полное окружение с FastAPI и PostgreSQL в одной команде:

```bash
# Сборка и запуск всех сервисов
docker-compose up -d --build

# Проверка статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f web

# Остановка
docker-compose down
```

### Состав сервисов в `docker-compose.yml`

| Сервис | Образ | Назначение | Порт |
|--------|-------|------------|------|
| `web` | Python 3.9-slim + Uvicorn | FastAPI приложение | 8000 |
| `db` | postgres:13 | База данных PostgreSQL | 5432 |

База данных использует volume `postgres_data` для сохранения данных между перезапусками контейнеров.

---

## Примеры запросов

### Создание объявления

```bash
curl -X POST http://localhost:8000/advertisement/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "iPhone 13 Pro",
    "description": "Отличное состояние,全套 комплект",
    "price": 65000.0,
    "author": "Иван"
  }'
```

Ответ:
```json
{
  "id": 1,
  "title": "iPhone 13 Pro",
  "description": "Отличное состояние,全套 комплект",
  "price": 65000.0,
  "author": "Иван",
  "created_at": "2025-01-15T12:30:00"
}
```

### Получение по ID

```bash
curl http://localhost:8000/advertisement/1
```

### Обновление объявления

```bash
curl -X PATCH http://localhost:8000/advertisement/1 \
  -H "Content-Type: application/json" \
  -d '{
    "title": "iPhone 13 Pro Max",
    "description": "Снижена цена!",
    "price": 70000.0,
    "author": "Иван"
  }'
```

### Удаление объявления

```bash
curl -X DELETE http://localhost:8000/advertisement/1
# Ответ: {"message": "Advertisement deleted"}
```

### Поиск объявлений

```bash
# По названию (case-insensitive)
curl "http://localhost:8000/advertisement/?title=iphone"

# По автору
curl "http://localhost:8000/advertisement/?author=иван"

# Комбинированный
curl "http://localhost:8000/advertisement/?title=iphone&author=иван"
```

---

## Структура проекта

```
py-homeworks-web-3.1-fast-api-1/
├── app/                          # Основное приложение
│   ├── __init__.py
│   ├── main.py                  # FastAPI app + роуты (CRUD + поиск)
│   ├── database.py              # SQLAlchemy engine + SessionLocal + Base
│   ├── models.py                # Модель БД: Advertisement
│   ├── schemas.py               # Pydantic-схемы (Create, Response)
│   └── crud.py                  # CRUD-операции + search_advertisements
├── Dockerfile                    # Образ для web-сервиса (Python 3.9-slim)
├── docker-compose.yml           # Оркестрация web + db
├── requirements.txt             # Зависимости Python
└── README.md                     # Документация проекта
```

---

## Технические решения

### 1. Многоуровневая архитектура

Проект разделён на слои для лучшей читаемости и тестируемости:

- **`main.py`** — роуты FastAPI, валидация входных данных
- **`crud.py`** — операции с БД (Create, Read, Update, Delete, Search)
- **`models.py`** — SQLAlchemy-модели (схема БД)
- **`schemas.py`** — Pydantic-схемы (сериализация/валидация API)
- **`database.py`** — конфигурация подключения к PostgreSQL

### 2. Зависимость `get_db` для управления сессиями

Сессия БД автоматически открывается перед запросом и закрывается после:

```python
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/advertisement/")
def create_ad(ad: schemas.AdvertisementCreate, db: Session = Depends(get_db)):
    return crud.create_advertisement(db, ad)
```

### 3. Автогенерация даты создания

Поле `created_at` заполняется автоматически при создании записи:

```python
class Advertisement(Base):
    __tablename__ = "advertisements"
    created_at = Column(DateTime, default=datetime.utcnow)
```

### 4. Case-insensitive поиск через `ilike`

Поиск по `title` и `author` нечувствителен к регистру — удобно для русскоязычных и англоязычных запросов:

```python
def search_advertisements(db, title=None, author=None):
    query = db.query(models.Advertisement)
    if title:
        query = query.filter(models.Advertisement.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(models.Advertisement.author.ilike(f"%{author}%"))
    return query.all()
```

### 5. Автоматическое создание таблиц

При старте приложения таблицы создаются автоматически, если их ещё нет:

```python
# app/main.py
models.Base.metadata.create_all(bind=engine)
```

### 6. Pydantic-схемы с наследованием

Схемы спроектированы по принципу DRY — базовая схема содержит общие поля, остальные её расширяют:

```python
class AdvertisementBase(BaseModel):
    title: str
    description: str
    price: float
    author: str

class AdvertisementCreate(AdvertisementBase):
    pass

class AdvertisementResponse(AdvertisementBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
```

### 7. Докеризация

`Dockerfile` использует лёгкий образ `python:3.9-slim`, а `docker-compose.yml` связывает web-сервис с PostgreSQL через volume для персистентности данных:

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
  db:
    image: postgres:13
    volumes:
      - postgres_data:/var/lib/postgresql/data
