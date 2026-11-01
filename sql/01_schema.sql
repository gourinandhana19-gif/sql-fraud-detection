CREATE TABLE transactions (
    step INT,
    type VARCHAR(20),
    amount NUMERIC(15, 2),
    nameOrig VARCHAR(50),
    oldbalanceOrg NUMERIC(15, 2),
    newbalanceOrig NUMERIC(15, 2),
    nameDest VARCHAR(50),
    oldbalanceDest NUMERIC(15, 2),
    newbalanceDest NUMERIC(15, 2),
    isFraud INT,
    isFlaggedFraud INT
);

