-- Найти количество дочерних элементов первого уровня вложенности для категорий номенклатуры.

SELECT
    c.name,
    COUNT(*) AS children_total
FROM categories AS c
JOIN categories AS cc ON cc.parent_id = c.id
GROUP BY 1
ORDER BY 1
