# 🌦️ WeatherPulse

**WeatherPulse** — это Django-приложение, собирающее погодные данные, отображающее статистику и поддерживающее фоновую обработку с помощью Celery.

---

## 🚀 Стек технологий

- Python 3.11
- Django
- Celery + Redis
- Docker + Docker Compose
- PostgreSQL / SQLite (зависит от настройки)
- Chart.js (если используется график)
- Bootstrap (если используется на фронте)

---

## 📁 Установка через Docker

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/yourusername/WeatherPulse.git
cd WeatherPulse

2. Создайте .env файл

Пример:

SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=*
CELERY_BROKER_URL=redis://redis:6379/0

3. Соберите и запустите контейнеры

docker-compose up --build

    Приложение будет доступно по адресу: http://localhost:8000

⚙️ Компоненты Docker
Сервис	Назначение
web	Django-приложение
redis	Брокер для Celery
celery	Воркер для фоновых задач
celery-beat	Планировщик периодических задач
📌 Полезные команды
Миграции:

docker-compose exec web python manage.py migrate

Создание суперпользователя:

docker-compose exec web python manage.py createsuperuser

📊 Возможности

    Регистрация пользователей

    Сбор и хранение погодных данных

    Отображение графиков и метрик

    Фоновые задачи (например, обновление погоды)

    Подписки на параметры погоды (если настроено)

🛠️ TODO / Возможные улучшения

    Поддержка PostgreSQL

    Email-уведомления на основе Celery

    Фронтенд на React (если планируется)

    Документация API (DRF Swagger или ReDoc)

🧑‍💻 Автор

Разработано как pet-проект для портфолио.
Автор: yourusername
📄 License

MIT License


---

📦 Если хочешь — могу сохранить этот `README.md` прямо в проект или отправить отдельным файлом.  
Хочешь? ​:contentReference[oaicite:0]{index=0}​
