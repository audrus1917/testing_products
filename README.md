# Задание
 
## Спроектировать схему БД. Модель данных реляционная.

### Сущности

+ [x] Номенклатура (наименование, кол-во, цена)
+ [x] Каталог номенклатуры/Дерево категорий.
+ [x] Клиенты (наименование, адрес)
+ [x] Заказы покупателей. Необходимо предусмотреть возможность делать заказ из разного набора товаров.

+ [x] Необходимо хранить данные о категориях товара, при этом сами категории могут иметь 
      неограниченный уровень вложенности
+ [x] Схема данных категорий номенклатуры должна безболезненно позволять добавлять 
      категории любого уровня вложенности. На этапе проектирования максимальный уровень 
      вложенности неизвестен.

* [x] Написать следующие SQL запросы:
  - [ ] Получение информации о сумме товаров заказанных под каждого клиента (Наименование клиента, сумма)
  - [ ] Найти количество дочерних элементов первого уровня вложенности для категорий номенклатуры.
  - [ ] Пункт 2.3.1. Написать текст запроса для отчета (view) «Топ-5 самых покупаемых товаров за последний месяц» 
        (по количеству штук в заказах). 
        В отчете должны быть: Наименование товара, Категория 1-го уровня, Общее количество проданных штук.

* [x] Проанализировать написанный в п. 2.3.1 запрос и структуру БД. Предложить варианты оптимизации 
      этого запроса и общей схемы данных для повышения производительности системы в 
      условиях роста данных (тысячи заказов в день).
* [x] Написать сервис «Добавление товара в заказ» который работает по REST-API. Метод должен принимать ID заказа, 
      ID номенклатуры и количество. Если товар уже есть в заказе, его количество должно увеличиваться, а не 
      создаваться новая позиция. Если товара нет в наличии то должна возвращаться соответствующая ошибка. 
      Стек -  любой фреймворк в пределах Python. Git репозиторий, контейнеризация, документация, и прочее — приветствуется.

Результатом выполнения задания должна быть даталогическая схема данных, SQL запросы по пункту 2 и сервис по пункту 3.

# Выполнение

* [cсылка на репозиторий с тестовым заданием](https://github.com/audrus1917/testing_products)
* [ссылка на схему БД](https://github.com/audrus1917/testing_products/blob/dev/data/database_schema.psql)
* [ссылка на дамп с простым случайным набором данных](https://github.com/audrus1917/testing_products/blob/dev/data/database.psql)
* [ссылка на скрипт для заполнения этими данными](https://github.com/audrus1917/testing_products/blob/dev/commands/data_loader.py)

## Приложения

* `users` - аутентифкация (`OAuth2 Password Flow with JWT`) и авторизация;
* `categories` - каталог категорий. Вложенность неограничена, при редактировании проводится проверка 
  на недопустимость цикличности
* `manufacturers` - производители товаров
* `products` - товары
* `clients` - клиенты
* `orders` - заказы и заказанные товары

## Примеры запросов

### Получение информации о сумме товаров заказанных под каждого клиента (Наименование клиента, сумма)

```sql
-- Получение информации о сумме товаров заказанных под каждого клиента (Наименование клиента, сумма)
SELECT 
    c.id AS client_id,
    CONCAT(c.last_name, ' ', c.first_name) AS full_name,
    SUM(i.amount * i.price)::money AS client_amount
FROM clients AS c
JOIN orders AS o ON c.id = o.client_id
JOIN order_items AS i ON i.order_id = o.id
GROUP BY c.id
```


## Макет фронтенда (Vue 3)

В репозитории добавлен фронтенд-макет в папке `frontend`.

### Запуск

```bash
cd frontend
npm install
npm run dev
```

Фронтенд запускается на `http://localhost:5173` и проксирует API-запросы (`/api/*`) на backend по адресу `http://localhost:8080`.

## Запуск через Docker Compose

```bash
docker compose up --build
```

Что поднимается:

- `api` (FastAPI) — `http://localhost:8080`
- `frontend` (Vite + Vue) — `http://localhost:5173`
- `db` (PostgreSQL) — внутренний сервис `db:5432` в сети compose
- `redis` — внутренний сервис `redis:6379` для кэша API

При старте контейнера `api` автоматически выполняются:

1. `alembic upgrade head`
2. `python commands/data_loader.py`

Скрипт загрузки данных идемпотентен: если данные уже есть, повторно они не создаются.

### Локальный dev-режим (override)

Файл `docker-compose.override.yml` применяется автоматически и добавляет:

- доступ к PostgreSQL с хоста: `localhost:55432`
- доступ к Redis с хоста: `localhost:56379`
- монтирование исходников в контейнеры `api` и `frontend`

Если нужен только базовый compose без override:

```bash
docker compose -f docker-compose.yml up --build
```

### Полный сброс и «чистый первый запуск»

```bash
docker compose down -v --remove-orphans
docker compose up --build -d
```

После удаления volume у PostgreSQL миграции и `data_loader.py` выполнятся заново как при первом запуске.

### Что реализовано

- Вход по `OAuth2 Password Flow` через `POST /api/v1/auth/token/`
- Разделы: товары, клиенты, заказы
- Для заказов есть форма добавления товара через `POST /api/v1/orders/{order_id}/items/add`
- JWT-токен сохраняется в `localStorage` и автоматически подставляется в `Authorization: Bearer ...`

### Найти количество дочерних элементов первого уровня вложенности для категорий номенклатуры.

```sql
-- Найти количество дочерних элементов первого уровня вложенности для категорий номенклатуры.

SELECT
    c.name,
    COUNT(*) AS children_total
FROM categories AS c
JOIN categories AS cc ON cc.parent_id = c.id
GROUP BY 1
ORDER BY 1
```

### Написать текст запроса для отчета (view) «Топ-5 самых покупаемых товаров за последний месяц» 

По количеству штук в заказах. В отчете должны быть: Наименование товара, Категория 1-го уровня, Общее количество проданных штук.

```sql

-- Написать текст запроса для отчета (view) «Топ-5 самых покупаемых товаров за последний месяц»

WITH total_products AS (
    SELECT
        p.id,
        count(*) AS total
    FROM products AS p
    JOIN order_items AS i ON i.product_id = p.id
    JOIN orders AS o ON i.order_id = o.id
    WHERE o.payment_date BETWEEN CURRENT_DATE - INTERVAL '1 month' AND CURRENT_DATE
    GROUP BY p.id
)

SELECT  
    t.id AS product_id,
    p.name AS product_name,
    c.name AS category_name,
    t.total
FROM total_products AS t 
JOIN products AS p ON p.id = t.id
JOIN categories AS c ON c.id = p.category_id
ORDER BY t.total DESC LIMIT 5
```

### Примеры рекурсивных запросов для категорий

#### Поиск всех "предков"

Для категории с `ID = 8`

```sql
WITH RECURSIVE ancestor_path AS (
    SELECT id, name, parent_id, 0 AS level
    FROM categories
    WHERE id = 8
    UNION ALL
    SELECT c.id, c.name, c.parent_id, ap.level + 1
    FROM categories c
    JOIN ancestor_path ap ON c.id = ap.parent_id
)
SELECT * FROM ancestor_path ORDER BY level DESC
```

#### "Дерево"

```sql
WITH RECURSIVE subordinates AS (
    SELECT 
        c.id, 
        c.name, 
        c.parent_id,
        1 AS level,
        ARRAY[c.parent_id] AS path
    FROM 
        categories AS c
    WHERE 
        c.id = 1

    UNION ALL
    SELECT 
        c.id, 
        c.name, 
        c.parent_id,
        s.level + 1 AS level,
        s.path || c.parent_id
    FROM 
        categories AS c
    JOIN 
        subordinates AS s ON c.parent_id = s.id
)
SELECT 
    id,
    CONCAT(REPEAT('  ', level), name)
FROM subordinates ORDER BY COALESCE(parent_id, 0), path;
```


