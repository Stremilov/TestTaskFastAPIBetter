# Проект: Веб-приложение для управления списком книг
## Описание проекта

Это веб-приложение для управления списком книг, разработанное с использованием FastAPI, базы данных PostgreSQL, и интеграции с gRPC-сервисом и RabbitMQ для обмена сообщениями. Приложение предоставляет REST API для выполнения операций CRUD (создание, получение, обновление, удаление) над книгами. Также реализована аутентификация через JWT, поддерживаются миграции базы данных с помощью Alembic, а для взаимодействия между сервисами используется RabbitMQ.
## Основные функции:

    CRUD операции для книг через REST API:
        Создание книги.
        Получение списка всех книг.
        Получение информации о книге по её ID.
        Обновление информации о книге.
        Удаление книги.

    Аутентификация пользователей с помощью JWT. Только аутентифицированные пользователи могут выполнять CRUD операции.

    gRPC-сервис для получения списка книг и информации по конкретной книге:
        gRPC-сервис взаимодействует с той же базой данных.
        Реализована прослушка RabbitMQ для обработки сообщений при изменении данных книг через REST API.

    Брокер сообщений:
        Используется RabbitMQ для передачи событий создания, обновления и удаления книги от веб-приложения к gRPC-сервису.
        gRPC-сервис выводит логи сообщений в консоль при получении.

    Тестирование:
        Написаны unit-тесты для проверки работы основных функций веб-приложения и gRPC-сервиса с использованием pytest.

    Документация:
        Автоматическая документация API с помощью Swagger.
        Предоставлены .proto файлы для gRPC-сервиса.

## Технологии

    FastAPI — фреймворк для построения веб-приложений.
    PostgreSQL — база данных для хранения данных о книгах.
    gRPC — сервис для получения данных о книгах.
    RabbitMQ — брокер сообщений для взаимодействия между сервисами.
    Alembic — инструмент для миграций базы данных.
    Docker — контейнеризация приложений.
    Pytest — тестирование.

## Архитектура

### Приложение состоит из двух основных компонентов:

    Веб-приложение на FastAPI, которое предоставляет REST API для взаимодействия с книгами.
    gRPC-сервис, который предоставляет доступ к данным книг и обрабатывает сообщения от веб-приложения через RabbitMQ.

Взаимодействие между этими сервисами происходит через RabbitMQ, который отправляет сообщения о создании, обновлении или удалении книг. gRPC-сервис прослушивает эти сообщения и выводит информацию в консоль.
#### Схема взаимодействия компонентов:

`PostgreSQL(Хранение данных) <-> FastAPI(REST API + JWT) <-> RabbitMQ(Message Broker) <-> gRPC-сервис(Получение книг) <-> PostgreSQL(Общая база с API)`


## Установка и запуск проекта
### 1. Клонирование репозитория

`git clone https://github.com/your-repository/book-management-app.git`
`cd book-management-app`

### 2. Настройка окружения

Создайте виртуальное окружение и установите зависимости:

- `python3 -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`

### 3. Настройка переменных окружения

Создайте файл .env и добавьте следующие переменные:

- `DATABASE_URL=postgresql://user:password@db:5432/books_db`
- `RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/`
- `JWT_SECRET=your_jwt_secret`
- `JWT_ALGORITHM=HS256`

### 4. Запуск проекта с использованием Docker

Проект поддерживает контейнеризацию, поэтому вы можете запустить его с помощью Docker Compose:


`docker-compose up --build`

#### Docker Compose запустит:

    - Веб-приложение на FastAPI.
    - gRPC-сервис.
    - PostgreSQL.
    - RabbitMQ.

### 5. Миграции базы данных

После первого запуска выполните миграции базы данных с помощью Alembic:

`docker-compose exec web alembic upgrade head`

### 6. Документация API

Документация REST API доступна по адресу:

`http://localhost:8000/docs`

### 7. gRPC

Файлы протокола для gRPC-сервиса находятся в директории grpc/protos/. Вы можете использовать их для взаимодействия с gRPC-сервисом.

### 8. Тестирование

Для запуска тестов используйте команду:

`pytest`

## Особенности:
- Реализован репозиторный подход к базе данных
- Декоратор @retry — реализован для повторного выполнения функций при возникновении ошибок, связанных с внешними сервисами
- Реализована панель для админов по адресу http://localhost:8000/admin
    

## Как использовать gRPC

    Протокол: .proto файлы находятся в папке grpc/protos/.
    Методы:
        GetBookById — получение информации о книге по ID.
        GetAllBooks — получение списка всех книг.

Заключение

Проект обеспечивает полноценное решение для управления библиотекой книг с использованием современных технологий, таких как FastAPI, PostgreSQL, gRPC и RabbitMQ. Реализованы необходимые операции CRUD, поддерживается аутентификация пользователей через JWT, а также обработка сообщений и кэширование для улучшения производительности.
