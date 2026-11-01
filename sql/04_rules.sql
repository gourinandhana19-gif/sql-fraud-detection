-- Rule 1: Identify high-value transactions

SELECT
    step,
    type,
    amount,
    nameOrig,
    nameDest,
    isFraud
FROM transactions
WHERE amount > 1000000
ORDER BY amount DESC
LIMIT 20;
-- Rule 2: Check fraud among high-value transactions

SELECT
    COUNT(*) AS total_high_value,
    COUNT(*) FILTER (WHERE isFraud = 1) AS fraud_count,
    COUNT(*) FILTER (WHERE isFraud = 0) AS genuine_count
FROM transactions
WHERE amount > 1000000;
-- Rule 3: Detect sender balance inconsistencies

SELECT
    step,
    type,
    amount,
    oldbalanceOrg,
    newbalanceOrig,
    isFraud
FROM transactions
WHERE oldbalanceOrg - amount <> newbalanceOrig
LIMIT 20;
-- Rule 3: Analyse sender balance inconsistencies

SELECT
    COUNT(*) AS total_mismatched,
    COUNT(*) FILTER (WHERE isFraud = 1) AS fraud_count,
    COUNT(*) FILTER (WHERE isFraud = 0) AS genuine_count
FROM transactions
WHERE oldbalanceOrg - amount <> newbalanceOrig;
-- Rule 4: Analyse destination balance inconsistencies

SELECT
    COUNT(*) AS total_mismatched,
    COUNT(*) FILTER (WHERE isFraud = 1) AS fraud_count,
    COUNT(*) FILTER (WHERE isFraud = 0) AS genuine_count
FROM transactions
WHERE oldbalanceDest + amount <> newbalanceDest;
-- Rule 5: Combine fraud indicators

SELECT
    COUNT(*) AS suspicious_transactions,
    COUNT(*) FILTER (WHERE isFraud = 1) AS fraud_count,
    COUNT(*) FILTER (WHERE isFraud = 0) AS genuine_count
FROM transactions
WHERE
    amount > 1000000
    OR oldbalanceDest + amount <> newbalanceDest;
    -- Rule 6: Calculate precision

SELECT
    ROUND(
        COUNT(*) FILTER (WHERE isFraud = 1) * 100.0
        / COUNT(*),
        2
    ) AS precision_percentage
FROM transactions
WHERE
    amount > 1000000
    OR oldbalanceDest + amount <> newbalanceDest;
-- Rule 7: Calculate recall

SELECT
    ROUND(
        COUNT(*) FILTER (WHERE isFraud = 1) * 100.0
        / (SELECT COUNT(*) FROM transactions WHERE isFraud = 1),
        2
    ) AS recall_percentage
FROM transactions
WHERE
    amount > 1000000
    OR oldbalanceDest + amount <> newbalanceDest;
    -- Rule 8: Calculate F1-score

WITH metrics AS (
    SELECT
        COUNT(*) FILTER (WHERE isFraud = 1) AS tp,
        COUNT(*) FILTER (WHERE isFraud = 0) AS fp,
        (SELECT COUNT(*) FROM transactions WHERE isFraud = 1) AS actual_fraud
    FROM transactions
    WHERE
        amount > 1000000
        OR oldbalanceDest + amount <> newbalanceDest
)
SELECT
    ROUND(
        2.0 * tp / (2 * tp + fp + actual_fraud - tp) * 100,
        2
    ) AS f1_score
FROM metrics;