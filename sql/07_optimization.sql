-- Day 10: Analyse fraud by transaction type

SELECT
    type,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (WHERE isFraud = 1) AS fraud_transactions,
    ROUND(
        COUNT(*) FILTER (WHERE isFraud = 1) * 100.0
        / COUNT(*),
        3
    ) AS fraud_percentage
FROM transactions
WHERE type IN ('TRANSFER', 'CASH_OUT')
GROUP BY type
ORDER BY fraud_percentage DESC;
-- Day 10: Focused TRANSFER fraud detection
-- 1. TRANSFER above 5 million

SELECT
    COUNT(*) AS total_flagged,
    COUNT(*) FILTER (WHERE isFraud = 1) AS fraud_detected,
    COUNT(*) FILTER (WHERE isFraud = 0) AS false_positives
FROM transactions
WHERE type = 'TRANSFER'
AND amount > 5000000;


-- 2. CASH_OUT above 1 million

SELECT
    COUNT(*) AS total_flagged,
    COUNT(*) FILTER (WHERE isFraud = 1) AS fraud_detected,
    COUNT(*) FILTER (WHERE isFraud = 0) AS false_positives
FROM transactions
WHERE type = 'CASH_OUT'
AND amount > 1000000;
SELECT
    COUNT(*) AS total_flagged,
    COUNT(*) FILTER (WHERE isFraud = 1) AS fraud_detected,
    COUNT(*) FILTER (WHERE isFraud = 0) AS false_positives
FROM transactions
WHERE type = 'CASH_OUT'
AND amount > 5000000;
SELECT
    COUNT(*) AS total_flagged,
    COUNT(*) FILTER (WHERE isFraud = 1) AS fraud_detected,
    COUNT(*) FILTER (WHERE isFraud = 0) AS false_positives
FROM transactions
WHERE
    (type = 'TRANSFER' AND amount > 1000000)
    OR
    (type = 'CASH_OUT' AND amount > 2000000);
    SELECT
    COUNT(*) AS total_flagged,
    COUNT(*) FILTER (WHERE isFraud = 1) AS fraud_detected,
    COUNT(*) FILTER (WHERE isFraud = 0) AS false_positives
FROM transactions
WHERE
    type = 'TRANSFER'
    AND amount > 1000000
    AND oldbalanceDest + amount <> newbalanceDest;
    SELECT
    COUNT(*) AS total_flagged,
    COUNT(*) FILTER (WHERE isFraud = 1) AS fraud_detected,
    COUNT(*) FILTER (WHERE isFraud = 0) AS false_positives
FROM transactions
WHERE
    type = 'TRANSFER'
    AND amount > 1000000
    AND oldbalanceOrg - amount <> newbalanceOrig
    AND oldbalanceDest + amount <> newbalanceDest;
    EXPLAIN ANALYZE
SELECT *
FROM transactions
WHERE type = 'TRANSFER';
CREATE INDEX idx_transactions_type
ON transactions(type);
EXPLAIN ANALYZE
SELECT *
FROM transactions
WHERE type = 'TRANSFER';
CREATE VIEW fraud_summary AS
SELECT
    type,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (WHERE isFraud = 1) AS fraud_transactions,
    COUNT(*) FILTER (WHERE isFraud = 0) AS genuine_transactions,
    ROUND(
        COUNT(*) FILTER (WHERE isFraud = 1) * 100.0
        / COUNT(*), 3
    ) AS fraud_percentage,
    ROUND(SUM(amount), 2) AS total_amount
FROM transactions
GROUP BY type;
SELECT * FROM fraud_summary;