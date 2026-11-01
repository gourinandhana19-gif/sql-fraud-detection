-- Day 9: Confusion Matrix

WITH risk_data AS (
    SELECT
        isFraud,
        (
            CASE WHEN amount > 1000000 THEN 2 ELSE 0 END
            +
            CASE WHEN oldbalanceDest + amount <> newbalanceDest THEN 3 ELSE 0 END
            +
            CASE WHEN oldbalanceOrg - amount <> newbalanceOrig THEN 2 ELSE 0 END
            +
            CASE WHEN type IN ('TRANSFER', 'CASH_OUT') THEN 1 ELSE 0 END
        ) AS risk_score
    FROM transactions
)

SELECT
    COUNT(*) FILTER (WHERE isFraud = 1 AND risk_score >= 5) AS true_positives,
    COUNT(*) FILTER (WHERE isFraud = 0 AND risk_score >= 5) AS false_positives,
    COUNT(*) FILTER (WHERE isFraud = 0 AND risk_score < 5) AS true_negatives,
    COUNT(*) FILTER (WHERE isFraud = 1 AND risk_score < 5) AS false_negatives
FROM risk_data;
-- Day 9: Performance Metrics

WITH confusion AS (
    SELECT
        COUNT(*) FILTER (
            WHERE isFraud = 1 AND risk_score >= 5
        ) AS tp,
        COUNT(*) FILTER (
            WHERE isFraud = 0 AND risk_score >= 5
        ) AS fp,
        COUNT(*) FILTER (
            WHERE isFraud = 0 AND risk_score < 5
        ) AS tn,
        COUNT(*) FILTER (
            WHERE isFraud = 1 AND risk_score < 5
        ) AS fn
    FROM (
        SELECT
            isFraud,
            (
                CASE WHEN amount > 1000000 THEN 2 ELSE 0 END
                +
                CASE WHEN oldbalanceDest + amount <> newbalanceDest THEN 3 ELSE 0 END
                +
                CASE WHEN oldbalanceOrg - amount <> newbalanceOrig THEN 2 ELSE 0 END
                +
                CASE WHEN type IN ('TRANSFER', 'CASH_OUT') THEN 1 ELSE 0 END
            ) AS risk_score
        FROM transactions
    ) AS risk_data
)
SELECT
    ROUND(tp * 100.0 / NULLIF(tp + fp, 0), 3) AS precision,
    ROUND(tp * 100.0 / NULLIF(tp + fn, 0), 3) AS recall,
    ROUND(
        2.0 * tp * 100 / NULLIF(2 * tp + fp + fn, 0), 3
    ) AS f1_score,
    ROUND((tp + tn) * 100.0 / (tp + fp + tn + fn), 2) AS accuracy
FROM confusion;