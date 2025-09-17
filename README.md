# Remnawave Telegram Bot (Aiogram 3)

## Задача

Небольшой асинхронный Telegram-бот, интегрированный с Remnawave API для управления пользовательскими ключами. Реализованы базовые сценарии и сохранение данных в PostgreSQL.
**Documentation:** `https://remna.st/api/`

## Фунĸционал

[ x ] Реализованы три кнопки: «Создать пользователя», «Получить ключ», «Продлить ключ».

[ ] Создание новых пользователей (ключи с определённой датой) через Remnawave API: выставление даты отключения и добавление данных в таблицу БД.
Сделано частично:
- Реализованы таблицы User и Subscription, объединены связью «один к одному».
- Реализован слой репозиториев для User, Subscription.
- Частично реализована валидация данных.
- Настроены миграции (Alembic).
- Пользователь сохраняется в БД через DatabaseMiddleware при /start и обновляется при дальнейших действиях.
- При создании пользователя на сервисе Remnawave возвращается 401 Unauthorized (причина не выяснена).

[ x ] осле создания нового ключа — отправка ссылки на подписку в ответном сообщении пользователю. (Реализовано, но не протестировано из-за 401 Unauthorized.)

[ ] ККнопка «Получить ключ» — запрос в БД и отправка пользователю ссылки на подписку и даты окончания.

[ x ] Запись данных в PostgreSQL (через asyncpg):
- таблица users (данные пользователя)
- таблица subscriptions (данные по ключу/подписке).

[ x ] Логировать важные события в терминал

Стуктура

```
app/
    handlers/ # хэндлеры aiogram
    keyboards/ # инлайн/реплай клавиатуры
    middlwares/ # middleware 
    service/
        remnawave/ # клиент Remnawave и обработка ошибок
config/ # конфиги (logging)
infra/
    models/ # SQLAlchemy модели
    repository/ # репозитории (UserRepo, SubscriptionRepo)
    storage/
        database/ # sessionmaker, Base, настройки БД
logs/
migration/
    versions/ # Alembic миграции
main.py
bot.py
settings.py
Docker
docker-compose.yml
alembic.ini
requirements.txt
```
