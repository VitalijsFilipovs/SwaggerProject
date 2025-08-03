# SwaggerProject

🔐 Django REST Framework проект с JWT-аутентификацией, пользовательскими пермишенами и автогенерацией документации через Swagger (`drf-yasg`).

---

## 🚀 Функциональность

- Регистрация задач и подзадач, привязанных к текущему пользователю (`owner`)
- Только автор задачи может её изменить или удалить
- JWT (SimpleJWT) аутентификация
- Swagger и Redoc-документация API
- Представление для получения задач только текущего пользователя

---

## 🧱 Стек технологий

- Python 3.13
- Django 4+
- Django REST Framework
- SimpleJWT
- drf-yasg (Swagger)

---

## 📦 Установка и запуск

1. Клонировать репозиторий:

bash
git clone https://github.com/VitalijsFilipovs/SwaggerProject.git
cd SwaggerProject


2. Создать и активировать виртуальное окружение:
   
bash
python -m venv .venv
.venv\Scripts\activate  # Windows

3. Установить зависимости:

bash
pip install -r requirements.txt

4. Применить миграции и создать суперпользователя:

bash
python manage.py migrate
python manage.py createsuperuser

5. Запустить проект:

bash
python manage.py runserver

----------------------------------------------------------------------------------------

 JWT Аутентификация
Эндпоинты SimpleJWT:

api/token/ — получить токен

api/token/refresh/ — обновить токен

Пример заголовка:

http
Authorization: Bearer <ваш токен>
📘 Swagger-документация
Swagger UI: http://127.0.0.1:8000/swagger/

Redoc: http://127.0.0.1:8000/redoc/

🧪 Тестирование
✅ Создание задачи — owner проставляется автоматически

❌ Попытка изменить или удалить чужую задачу — 403 Forbidden

🔒 /api/tasks/my_tasks/ — возвращает задачи только текущего пользователя

📘 Swagger отображает все доступные эндпоинты



