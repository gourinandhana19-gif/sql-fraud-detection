```sql
-- 1. Total, fraud and genuine transactions

SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE isfraud = 1) AS fraud_transactions,
    COUNT(*) FILTER (WHERE isfraud = 0) AS genuine_transactions
FROM transactions;


-- 2. Transaction counts by type

SELECT
    type,
    COUNT(*) AS total_transactions
FROM transactions
GROUP BY type
ORDER BY total_transactions DESC;


-- 3. Fraud transactions by type

SELECT
    type,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (WHERE isfraud = 1) AS fraud_transactions,
    ROUND(
        COUNT(*) FILTER (WHERE isfraud = 1) * 100.0 / COUNT(*),
        3
    ) AS fraud_percentage
FROM transactions
GROUP BY type
ORDER BY fraud_transactions DESC;
-- 4. Average transaction amount: Fraud vs Genuine

SELECT
    CASE
        WHEN isfraud = 1 THEN 'Fraud'
        ELSE 'Genuine'
    END AS transaction_category,
    COUNT(*) AS total_transactions,
    ROUND(AVG(amount), 2) AS average_amount,
    ROUND(MAX(amount), 2) AS maximum_amount
FROM transactions
GROUP BY isfraud
ORDER BY isfraud DESC;
-- 5. Fraud transactions by step

SELECT
    step,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (WHERE isfraud = 1) AS fraud_transactions
FROM transactions
WHERE isfraud = 1
GROUP BY step
ORDER BY fraud_transactions DESC
LIMIT 10;
-- 6. Total fraud amount by transaction type

SELECT
    type,
    COUNT(*) AS fraud_count,
    ROUND(SUM(amount), 2) AS total_fraud_amount
FROM transactions
WHERE isfraud = 1
GROUP BY type
ORDER BY total_fraud_amount DESC;