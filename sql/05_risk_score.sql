-- Day 8: Fraud Risk Scoring

SELECT
    step,
    type,
    amount,
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
LIMIT 20;
-- Risk Score Classification

WITH risk_data AS (
    SELECT
        type,
        amount,
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
    CASE
        WHEN risk_score >= 5 THEN 'High Risk'
        WHEN risk_score >= 2 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS risk_level,
    COUNT(*) AS total_transactions,
    COUNT(*) FILTER (WHERE isFraud = 1) AS fraud_transactions
FROM risk_data
GROUP BY risk_level
ORDER BY risk_level;