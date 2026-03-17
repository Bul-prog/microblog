# Описание проекта

Проект представляет собой корпоративный сервис микроблогов, 
реализованное с использованием FastAPI, PostgreSQL, Docker и Nginx (backend + frontend приложение с REST API).
Frontend — одностраничное приложение (SPA), backend — асинхронный API-сервер.

## 📌 Стек технологий

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy (Async)
- PostgreSQL
- Pydantic
- Uvicorn

### Frontend
- HTML / CSS / JavaScript (готовая сборка)
- Nginx

### Инфраструктура
- Docker
- Docker Compose

---

## 📁 Структура проекта

```text
microblog/
│
├── alembic/                        # миграции БД
│   └── env.py
│
├── app/
│   │
│   ├── endpoints/                  # HTTP-роуты (FastAPI)
│   │   ├── medias_endpoints.py
│   │   ├── tweets_endpoints.py
│   │   └── users_endpoints.py
│   │
│   ├── media/                      # загруженные файлы
│   │
│   ├── deps.py                     # зависимости (DB, auth и т.п.)
│   ├── main.py                     # точка входа FastAPI
│   ├── models.py                   # SQLAlchemy модели
│   ├── schemas.py                  # Pydantic-схемы
│   ├── services.py                 # бизнес-логика
│   └── test_key.py                 # тестовый api-key
│
├── frontend/
│   └── dist/                       # файлы frontend
│
├── nginx/
│   └── default.conf                # конфигурация nginx
├── tests/                          # тесты
│
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── README.md
└── requirements.txt
```

### 🚀 Запуск проекта

- Клонировать репозиторий
```bash
git clone https://github.com/Bul-prog/microblog.git
cd python_advanced_diploma
```

- Запуск через Docker Compose  
```bash
docker-compose up --build
```
    

### 📌 Основные эндпоинты

| Раздел       | HTTP метод | URL                    | Описание                               |
| ------------ | ---------- | ---------------------- | -------------------------------------- |
| Пользователи | GET        | /api/users/me          | Получение данных текущего пользователя |
| Пользователи | POST       | /api/users/follow/{id} | Подписка на пользователя               |
| Пользователи | DELETE     | /api/users/follow/{id} | Отписка от пользователя                |
| Твиты        | POST       | /api/tweets            | Создание нового твита                  |
| Твиты        | GET        | /api/tweets            | Получение ленты твитов                 |
| Твиты        | DELETE     | /api/tweets/{id}       | Удаление твита                         |
| Медиа        | POST       | /api/medias            | Загрузка медиафайла                    |


