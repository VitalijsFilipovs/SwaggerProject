# SwaggerProject — Housing Rental Backend

## 📌 Описание проекта
Backend-сервис для системы аренды жилья.  
Реализован на **Django + Django REST Framework**, с поддержкой **JWT-аутентификации**, Swagger/Redoc документации, Docker и MySQL.

### Основные функции:
- **Управление объявлениями (listings)**  
  - Создание, редактирование, удаление объявлений арендодателями (landlords).  
  - Просмотр и фильтрация объявлений арендаторами (renters).  
  - Поиск по городу, району, описанию.  
  - Сортировка по цене, дате, рейтингу.  

- **Бронирования (bookings)**  
  - Арендатор может бронировать жильё.  
  - Владелец объявления подтверждает (`approve`) или отклоняет (`reject`) бронь.  
  - Арендатор может отменить (`cancel`).  
  - Проверка пересечений дат и статусов.  

- **Отзывы и рейтинги (reviews)**  
  - Арендатор с подтверждённой бронью может оставить отзыв и рейтинг.  
  - У каждого объявления считается средний рейтинг и количество отзывов.  

- **Аутентификация и авторизация**  
  - Регистрация, логин/логаут, JWT-токены.  
  - Разграничение ролей: `landlord` и `renter`.  
  - Swagger UI с поддержкой JWT авторизации.  

---

## ⚙️ Технологии
- Python 3.12  
- Django 5 + DRF  
- MySQL (Docker container)  
- Docker + docker-compose  
- JWT (SimpleJWT)  
- drf-yasg (Swagger/Redoc)  
- django-filter (поиск/фильтрация)  

---

## 🚀 Запуск проекта

### 1. Клонировать репозиторий

git clone https://github.com/VitalijsFilipovs/SwaggerProject.git
cd SwaggerProject ```


### 2. Создать .env файл

Пример содержимого (.env в корне):

DJANGO_SECRET_KEY=dev-secret-key
DJANGO_DEBUG=true
DJANGO_ALLOWED_HOSTS=*

MYSQL_DATABASE=pagination_db
MYSQL_USER=pagination_user
MYSQL_PASSWORD=password
DB_HOST=db
DB_PORT=3306


### 3. Запуск через Docker

docker-compose up -d --build


### 4. Применить миграции и создать суперпользователя

docker-compose run --rm web python manage.py makemigrations
docker-compose run --rm web python manage.py migrate
docker-compose run --rm web python manage.py createsuperuser


### 5. Открыть в браузере

Главная: http://localhost:8000/

Swagger UI: http://localhost:8000/swagger/

Redoc: http://localhost:8000/redoc/

Admin: http://localhost:8000/admin/

###########################################################



📚 Примеры API

Создать объявление (landlord)

POST /api/listings/listings/
{
  "title": "Студия у метро",
  "description": "5 мин пешком",
  "city": "Riga",
  "district": "Center",
  "address": "Brivibas 12",
  "price": "450.00",
  "rooms": 1,
  "property_type": "studio",
  "status": "active"
}

--------

Забронировать (renter)

POST /api/bookings/bookings/
{
  "listing": 1,
  "start_date": "2025-09-01",
  "end_date": "2025-09-05"
}

--------

Подтвердить бронь (landlord)

POST /api/bookings/bookings/1/approve/

--------

Оставить отзыв (renter с подтверждённой бронью)

POST /api/reviews/reviews/
{
  "listing": 1,
  "rating": 5,
  "comment": "Очень уютная студия!"
}

################################################################



🔑 JWT-аутентификация
Получить токен

POST /api/token/
{
  "username": "user@example.com",
  "password": "mypassword"
}

---------

Обновить токен

POST /api/token/refresh/
{
  "refresh": "<refresh_token>"
}

----------

Использовать токен в запросах

В заголовке:

Authorization: Bearer <access_token>

#################################################################



🔎 Поиск, фильтры и сортировка
Поиск (full-text по полям)

Эндпоинт:
GET /api/listings/listings/?search=<строка>

Ищет по: title, description, city, district.

Примеры:

/api/listings/listings/?search=Riga

/api/listings/listings/?search=студия

-------------------------------------------------------------

Фильтры

Эндпоинт:
GET /api/listings/listings/?<filters>

Поддерживаются (из ListingFilter):

price_min — минимальная цена

price_max — максимальная цена

rooms — кол-во комнат

city — город (icontains)

property_type — тип жилья (apartment|house|room|studio)

status — active|inactive

Примеры:

/api/listings/listings/?city=Riga&price_max=700

/api/listings/listings/?rooms=2&property_type=apartment

--------------------------------------------------------

Сортировка (ordering)

Эндпоинт:
GET /api/listings/listings/?ordering=<поле>

Используй поля:

price, -price

created_at, -created_at

avg_rating, -avg_rating ← средняя оценка (аннотация)

reviews_count, -reviews_count← кол-во отзывов (аннотация)

Примеры:

/api/listings/listings/?ordering=-price — от дорогих к дешёвым

/api/listings/listings/?search=Riga&ordering=-avg_rating — в Риге, сначала самые высоко оценённые

/api/listings/listings/?ordering=-reviews_count — самые обсуждаемые

Поля avg_rating и reviews_count автоматически добавляются к каждому объявлению в ответе.

--------------------------------------------------------------------

👨‍💻 Автор

Vitalijs Filipovs
📧 filipovvitalij@gmail.com


