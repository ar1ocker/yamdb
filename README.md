# API_YAMDB

Проект YaMDb собирает отзывы пользователей на произведения (Фильмы, книги, музыка и т.д.)

## Запуск

- Скачайте репозиторий

- Создайте и активируйте окружение

```bash
python3 -m venv venv
```

```bash
. venv/bin/activate
```

- Установите зависимости

```bash
pip3 install -r requirements.txt
```

- Выполните миграции

```
python3 manage.py migrate
```

- Запустите проект

```
python3 manage.py runserver
```

По умолчанию проект слушает локальный IP и порт 8000 - 127.0.0.1:8000

## API

#### Далее будут описаны основные запросы для получения того или иного объекта из API Yamdb. С полной документацией можно ознакомиться по ссылке /redoc/ при запущенном API Yamdb, либо же отправив файл redoc.yaml (api_yamdb/static/redoc.yaml) на сайт для чтения OpenAPI документации (например [redocly.github.io/redoc/](redocly.github.io/redoc/))

### Регистрация нового пользователя
- Авторизация - нет
- Url - api/v1/auth/signup/
- Тип запроса - POST
- Заголовки
```
Content-type: application/json
```
- Payload
```json
{
    "email": "user@example.com",
    "username": "string"
}
```

После запроса на указанную почту будет отправлено сообщение с кодом подтверждения

### Получение JWT-токена
- Авторизация - нет
- Url - /api/v1/auth/token/
- Тип запроса - POST
- Заголовки
```
Content-type: application/json
```
- Payload
```json
{
    "username": "string",
    "confirmation_code": "string"
}
```

В ответ на запрос будет отправлен JWT токен
```json
{
    "token": "string"
}
```

### Получение списка всех категорий
- Авторизация - нет
- Url - /api/v1/categories/
- Тип запроса - GET
- Дополнительные параметры
search - поиск по названию категории
- Ответ
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

### Получение списка всех жанров
- Авторизация - нет
- Url - /api/v1/genres/
- Тип запроса - GET
- Дополнительные параметры
search - поиск по названию жарна
- Ответ
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

### Получение списка всех произведений
- Авторизация - нет
- Url - /api/v1/titles/
- Тип запроса - GET
- Дополнительные параметры
category - фильтрует по полю slug категории
genre - фильтрует по полю slug жанра
name - фильтрует по названию произведения
year - фильтрует по году
- Ответ
```json
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
```

### Получение списка всех отзывов
- Авторизация - нет
- Url - api/v1/titles/{title_id}/reviews/
- Тип запроса - GET
- Ответ
```json
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
```

### Получение списка всех комментариев к отзыву
- Авторизация - нет
- Url - api/v1/titles/{title_id}/reviews/{review_id}/comments/
- Тип запроса - GET
- Ответ
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```

### Получение списка всех пользователей
- Авторизация - jwt-token (Admin)
- Url - api/v1/users/
- Тип запроса - GET
- Заголовки
```
Authorization: Bearer <jwt-token>
```
- Дополнительные параметры
search - Поиск по имени пользователя (username)
- Ответ
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "username": "string",
      "email": "user@example.com",
      "first_name": "string",
      "last_name": "string",
      "bio": "string",
      "role": "user"
    }
  ]
}
```

### Получение данных своей учетной записи
- Авторизация - jwt-token (любой авторизаванный пользователь)
- Url - api/v1/users/me/
- Тип запроса - GET
- Заголовки
```
Authorization: Bearer <jwt-token>
```
- Ответ
```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

## Команда разработки

### Ahriman - Auth/Users
Часть касающаяся управлением пользователями: 
- систему регистрации и аутентификации,
- права доступа,
- работу с токеном,
- систему подтверждения через e-mail.

### hun53 - Categories/Genres/Titles
Модели, view и эндпойнты для
- произведений,
- категорий,
- жанров;
- реализует импорта данных из csv файлов.

### ar1ocker - Review/Comments
Работа над
- отзывами,
- комментариями,
- рейтингом произведений.

### Яндекс Практикум - тесты

### Отдельная благодарность наставнику от ЯП - Александру Хмелевскому
