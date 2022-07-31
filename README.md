### Проект Yamdb:
Baсkend и api для сбора произведений и отзывов. API позволяет получить всю основную информацию социальной сети. Часть frontend-а отсутствует.

![workflow](https://github.com/turpanov/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

### Ссылка на развернутый проект Yamdb:

`http://yatube-turpanov.hopto.org/redoc`

### Как запустить проект:

Требуется наличие docker и docker-compose.

Процедура запуска:

1. Склонировать проект на локальный компьютер.
2. В папке "infra" проекта создать файл .env с описанием переменных:

DB_ENGINE=django.db.backends.postgresql
DB_NAME=<имя базы данных>
POSTGRES_USER=<пользователь базы данных>
POSTGRES_PASSWORD=<пароль пользователя>
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<ключ шифрования данных Django>

3. Запустить консоль и перейти в директорию "infra" проекта.
4. Выполнить команду `docker-compose up`
5. После запуска docker-compose открыть новое окно консоли и выполнить следующие команды:
`docker-compose exec web python manage.py migrate` - выполняет миграции
`docker-compose exec web python manage.py createsuperuser` - создает суперпользователя
`docker-compose exec web python manage.py collectstatic --no-input` - подключает статику

## Как остановить проект:

1. Команда для остановки - `docker-compose stop`
2. Команда для остановки и удаления контейнеров - `docker-compose down -v`

### Основные ендпойнты (urls):
```
http://{url}/api/v1/auth/signup/ - предназначен для самморегистрации пользователей, получения кода подтверждения
http://{url}/api/v1/auth/token/ - предназначен для получения токена, после получения кода подтверждения
http://{url}/api/v1/users/ - предназначен для самостоятельного изменения данных пользователей - на эндпойнте me, или же для работы с пользовотелями администратором - эндпойнты имена пользователей
http://{url}/api/v1/categories/ - предназначен для просмотра категорий пользователями, создания \ изменения категорий произведений - администратором
http://{url}/api/v1/genres/ - предназначен для просмотра жанров пользователями, создания \ изменения жанров произведений - администратором
http://{url}/api/v1/titles/ - предназначен для просмотра произведений пользователями, создания \ изменения произведений - администратором
http://{url}/api/v1/titles/{title_id}/reviews/ - предназначен для просмотра \ создания отзывов пользователями, изменения \ удаления - администратором, модератором, автором
http://{url}/api/v1/titles/{title_id}/reviews/{review_id}/comments/ - предназначен для просмотра \ создания комментариев на отзывы пользователями, изменения \ удаления - администратором, модератором, автором
```
### Примеры обращений к API:


#### Самостоятельно зарегистрироваться и получить код подтвердения для получения токена:

Обратиться по методу Post на - ``` http://{url}/api/v1/auth/signup/ ```
В теле запроса передать параметры username и email и их значения. После этого, если пользователь новый произойдет его регистрация, если пользователь уже существует, то регистрация не произойдет, на указанную почту будет выслан код подтверждения:
Пример тела запроса:
```
{
    "username": "test1",
    "email": "test12@yamdb.ru"
}
```
#### Получить токен для авторизации пользователя:

Обратиться по методу Post на - ``` http://{url}/api/v1/auth/token/ ```
В теле запроса передать параметры username и confirmation_code и их значения.
Полученный токен использовать для авторизации в сервисе api по методу bearer.
Пример тела запроса:
```
{
    "username": "test1",
    "confirmation_code": "123456"
}
```
Пример ответа:
```
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUzOTI3ODgxL"
}
```
#### Получить список произведений:

Метод Get - ``` http://{url}/api/v1/titles/ ```

Ответ
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]

```
#### Добавить произведение (доступно только администратору):

Обратиться по методу Post на эндпойнт - ``` http://{url}/api/v1/titles/ ```
В теле запроса передать название произведения, год создания, описание, список жанров, категорию
Тело запроса:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": ["string",],
  "category": "string"
}
```
Ответ:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}

```
#### Просмотреть детали по произведению:

Обратиться по методу Get на эндпойнт - ``` http://{url}/api/v1/titles/{titles_id}/ ```
Ответ:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}

```
Администратору на эндпойнте ``` http://{url}/api/v1/titles/{titles_id}/ ``` также доступны методы Patch и Delete

#### Получить список отзывов:

Метод Get - ``` http://{url}/api/v1/titles/{title_id}/reviews/ ```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]

```
#### Получить отзыв по id:

Метод Get - ``` http://{url}/api/v1/titles/{title_id}/reviews/{review_id}/ ```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}

```
#### Добавить отзыв:

Отправить запрос по методу Post - ``` http://{url}/api/v1/titles/{title_id}/reviews/ ```

Тело запроса:
```
{
  "text": "string",
  "score": 1
}
Ответ:
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
Администратору, модератору и автору на эндпойнте ``` http://{url}/api/v1/titles/{title_id}/reviews/{review_id}/ ``` также доступны методы Patch и Delete
