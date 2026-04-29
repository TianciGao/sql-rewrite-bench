SELECT COUNT(CASE WHEN currency = 'CZK' THEN 1 END) - COUNT(CASE WHEN currency = 'EUR' THEN 1 END) FROM customers WHERE segment = 'SME'
