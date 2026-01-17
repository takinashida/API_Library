# 📚 Library API

REST API для управления библиотекой: авторы, книги, прокаты и пользователи.  
Документация доступна через Swagger (OpenAPI 3).

---

## 🚀 Стек

- Python / Django
- Django REST Framework
- JWT (SimpleJWT)
- Swagger / OpenAPI 3

---

## 📖 Swagger-документация

Доступна по адресу:

```

GET /api/schema/

```

Форматы:
- JSON — `application/vnd.oai.openapi+json`
- YAML — `application/vnd.oai.openapi`

---

## 🔐 Аутентификация

Используется **JWT**.

### Получение токенов
```

POST /users/token/

````

**Request**
```json
{
  "email": "user@example.com",
  "password": "string"
}
````

**Response**

```json
{
  "access": "string",
  "refresh": "string"
}
```

### Обновление access-токена

```
POST /users/token/refresh/
```

```json
{
  "refresh": "string"
}
```

---

## 👤 Пользователи

### Регистрация

```
POST /users/registration/
```

```json
{
  "email": "user@example.com",
  "password": "string",
  "telegram_chat_id": "string"
}
```

### Подтверждение email

```
GET /users/email-confirm/{token}/
```

### Список пользователей

```
GET /users/
```

---

## ✍️ Авторы (`Author`)

### Список авторов

```
GET /author/
```

### Создание автора

```
POST /author/
```

```json
{
  "name": "string",
  "surname": "string",
  "second_name": "string"
}
```

### Получение автора

```
GET /author/{id}/
```

### Обновление автора

```
PUT /author/{id}/
PATCH /author/{id}/
```

### Удаление автора

```
DELETE /author/{id}/
```

---

## 📚 Книги (`Book`)

### Список книг

```
GET /book/
```

#### Фильтры:

- `author` — ID автора
    
- `genre` — жанр
    
- `search` — поиск
    
- `page` — пагинация
    

### Создание книги

```
POST /book/
```

```json
{
  "title": "string",
  "author": 0,
  "genre": "string",
  "count_available": 10,
  "all_count": 10
}
```

### Получение книги

```
GET /book/{id}/
```

### Обновление книги

```
PUT /book/{id}/
PATCH /book/{id}/
```

### Удаление книги

```
DELETE /book/{id}/
```

---

## 🔄 Прокат книг (`Loan`)

### Список прокатов

```
GET /loan/
```

### Создание проката

```
POST /loan/
```

```json
{
  "user": 0,
  "book": 0,
  "return_at": "2026-01-07T02:09:49.971Z",
  "is_active": true
}
```

### Получение проката

```
GET /loan/{id}/
```

### Обновление проката

```
PUT /loan/{id}/
PATCH /loan/{id}/
```

### Удаление проката

```
DELETE /loan/{id}/
```

---

## 📦 Ответы со списками

Все списки возвращаются в формате пагинации:

```json
{
  "count": 123,
  "next": "http://api.example.org/?page=2",
  "previous": null,
  "results": []
}
```

---

## 🧪 Тестирование

Запуск тестов:

```bash
python manage.py test
```

Покрытие тестами:

```bash
coverage run manage.py test
coverage report
coverage html
```

