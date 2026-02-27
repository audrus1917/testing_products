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
