# PaginationProject

## Описание

Проект Django API с поддержкой:
- JWT аутентификации (SimpleJWT)
- Пермишенов (`IsAuthenticated`)
- Глобальной пагинации (5 элементов на страницу)

## Установка

```bash
git clone https://github.com/VitalijsFilipovs/PaginationProject.git
cd PaginationProject
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

------------------------------------------------------------------------------------------
Миграции и запуск
bash
python manage.py migrate
python manage.py runserver

------------------------------------------------------------------------------------------
API
Получение токена:
POST /api/token/

json
{
  "username": "ваш_юзер",
  "password": "ваш_пароль"
}

------------------------------------------------------------------------------------------
Обновление токена:
POST /api/token/refresh/

Эндпоинты задач:
GET /api/tasks/ — получить список задач (с пагинацией)

POST /api/tasks/ — создать задачу (нужен JWT токен)

