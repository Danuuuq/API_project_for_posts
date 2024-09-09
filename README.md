# API для YaTube v1 домашнее задание на Я.Практикум.

Домашнее задание по созданию API для обработка запросов от клиентов.

## Функционал и особенности работы API:

1. Обращение к API YaTube для CRUD операций.
2. Просмотр, создание, редактирование и удаление постов, комментариев к постам, создание подписок на других пользователей.
3. Пользователь должен быть зарегистрирован и получить личный токен. Используется djoser
4. На уровне проекта установлено разрешение IsAuthenticated.

## Порядок запуска API-сервиса:

Клонируйте репозиторий себе на компьютер/сервер:

```bash
git clone git@github.com:user_name/api_final_yatube.git
```

Создайте виртуальное окружение:

```bash
python3 -m venv venv
```

Активируйте виртуальное окружение:

*Windows:*
```bash
source venv/Scripts/activate
```
*Linux & MacOS:*
```bash
source venv/Bin/activate
```

Установите зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

## Примеры запросов к API:

1. **Путь к эндпоинтам API.** 
[Link](http://127.0.0.1:8000/api/v1/) - стандартный путь к API
[Link](http://127.0.0.1:8000/api/v1/groups/) - GET получение всех групп
[Link](http://127.0.0.1:8000/api/v1/posts/) - GET получение всех постов, POST создание групп
[Link](http://127.0.0.1:8000/api/v1/posts/{post_id}/comment) - GET получение всех комментариев к посту, POST создание комментария
Ко всем эндпоинтам можно обратиться за детальной информацией, указав в конце id.
[Link](http://127.0.0.1:8000/api/v1/follow/) - GET получение всех своих подписок, POST подписаться на пользователя
2. **Получение/обновление/проверка токена.**
Убедитесь, что пользователь создан для выполнения запроса.
POST - Получить JWT-токен
[Link](http://127.0.0.1:8000/api/v1/jwt/create/) -
```json
{
    "username": "string",
    "password": "string"
}
```
POST - Обновить JWT-токен
[Link](http://127.0.0.1:8000/api/v1/jwt/refresh/) -
```json
{
    "refresh": "string"
}
```
POST - Проверить  JWT-токен
[Link](http://127.0.0.1:8000/api/v1/jwt/verify/) -
```json
{
    "token": "string"
}
```
Полученный токен необходимо использовать при любых запросах к API.
3. **CRUD операции.**
Эндпоинты: */api/v1/posts/* и */api/v1/posts/{post_id}/comment* принимает запросы GET, POST, PATCH, PUT и DELETE при указании id поста или комментария.
Пример запроса к */api/v1/posts/* ("group" и "image" не являются обязательным полем):
```json
{
    "text(required)": "string (текст публикации)",
    "image": "string or null <binary>",
    "group": "integer or null (id сообщества)"
}
```
Для фильтрации выдачи постов можно применить limit и offset, пример запроса:
[Link](http://127.0.0.1:8000/api/v1/posts/?limit=1&offset=1)
Пример запроса к */api/v1/posts/{post_id}/comment*:
```json
{
    "text(required)": "string (текст комментария)"
}
```
Эндпоинт: */api/v1/follow/* принимает GET (возвращает список ваших подписок) и POST (создание подписки) запросы, пример запроса POST:
```json
{
    "following(required)": "string (username)"
}
```
Для поиска среди своих подписок можно применить search, пример запроса:
[Link](http://127.0.0.1:8000/api/v1/follow/?search=username)
Эндопинт: */api/v1/groups/* доступен только для чтения.
