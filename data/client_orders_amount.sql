-- Получение информации о сумме товаров заказанных под каждого клиента (Наименование клиента, сумма)

SELECT 
    c.id AS client_id,
    CONCAT(c.last_name, ' ', c.first_name) AS full_name,
    SUM(i.amount * i.price)::money AS client_amount
FROM clients AS c
JOIN orders AS o ON c.id = o.client_id
JOIN order_items AS i ON i.order_id = o.id
GROUP BY c.id
