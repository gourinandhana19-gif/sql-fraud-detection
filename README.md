# ⚡ FRAUD//X — Financial Transaction Intelligence System

**A SQL-powered financial fraud detection and analytics project using PostgreSQL, Python and Streamlit.**

FRAUD//X explores millions of financial transactions to identify suspicious patterns, analyse fraud behaviour, evaluate detection rules and present insights through an interactive dashboard.

---

## 📌 Project Overview

Financial fraud is a major challenge in digital payment systems. Identifying suspicious transactions among millions of legitimate transactions requires effective data analysis and detection strategies.

This project uses the **PaySim synthetic financial transaction dataset** to explore transaction behaviour, investigate fraudulent activities and evaluate rule-based fraud detection techniques.

The project combines SQL-based analysis with an interactive Python dashboard to transform raw transaction data into meaningful insights.

## 🎯 Project Objectives

- Analyse large-scale financial transaction data using SQL.
- Identify patterns associated with fraudulent transactions.
- Develop rule-based fraud detection techniques.
- Calculate and evaluate fraud detection metrics.
- Explore transaction patterns across different payment types.
- Build an interactive dashboard for visual analysis.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| PostgreSQL | Database management and SQL analysis |
| SQL | Data exploration, fraud rules and risk scoring |
| Python | Dashboard development and data processing |
| Pandas | Data manipulation |
| Streamlit | Interactive dashboard |
| Plotly | Data visualisation |
| Git & GitHub | Version control and project management |
| VS Code | Development environment |

## 📂 Dataset

**Dataset:** PaySim – Financial Mobile Money Transactions

**Source:** [PaySim Dataset on Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1)

The dataset contains approximately **6.36 million financial transactions** with information such as:

- Transaction type
- Transaction amount
- Sender and receiver accounts
- Previous and updated account balances
- Fraud indicator
- Flagged fraud indicator

**Dataset size:** 6,362,620 transactions  
**Fraudulent transactions:** 8,213  
**Genuine transactions:** 6,354,407

*Note: PaySim is a synthetic dataset created for financial transaction research and simulation.*

## 🔍 Project Workflow

1. **Database Setup:** Created a PostgreSQL database and transaction table.
2. **Data Import:** Imported the PaySim dataset into PostgreSQL.
3. **Exploratory Data Analysis:** Investigated transaction types, amounts, fraud distribution and transaction patterns.
4. **Fraud Detection Rules:** Developed SQL-based rules using transaction amounts and account balance inconsistencies.
5. **Risk Scoring:** Created an experimental risk scoring system using multiple transaction indicators.
6. **Evaluation:** Evaluated detection performance using precision, recall, F1-score and a confusion matrix.
7. **Optimization:** Compared different transaction amount thresholds and detection rule combinations.
8. **Dashboard Development:** Built an interactive Streamlit dashboard using Python and Plotly.

## 📊 Key Findings

Analysis of the PaySim dataset revealed several interesting patterns:

- Only **8,213 transactions** out of 6.36 million were labelled as fraudulent.
- Fraudulent transactions occurred in only two transaction types: `TRANSFER` and `CASH_OUT`.
- CASH_OUT recorded 4,116 fraudulent transactions.
- TRANSFER recorded 4,097 fraudulent transactions.
- Fraudulent transactions had a higher average transaction amount than genuine transactions.
- High transaction amounts and balance inconsistencies were useful indicators to investigate, but individual rules produced many false positives.

### Fraud Distribution

| Category | Transactions |
|---|---:|
| Total transactions | 6,362,620 |
| Fraudulent | 8,213 |
| Genuine | 6,354,407 |

### Rule Optimization

Different transaction amount thresholds were tested.

One notable experiment was:

**CASH_OUT transactions above 2,000,000**

- Transactions flagged: 858
- Fraudulent transactions identified: 834
- Precision: 97.20%
- Recall: 10.15%

This experiment demonstrated a trade-off between precision and recall. Although the rule identified a high proportion of fraudulent transactions among those flagged, it missed many other fraudulent transactions.

## 📈 Fraud Detection Evaluation

The experimental risk scoring system was evaluated using a threshold of 5.

| Metric | Result |
|---|---:|
| True Positives (TP) | 1,611 |
| False Positives (FP) | 3,429,420 |
| True Negatives (TN) | 2,924,987 |
| False Negatives (FN) | 6,602 |
| Precision | 0.047% |
| Recall | 19.615% |
| F1-score | 0.094% |
| Accuracy | 46.00% |

These results demonstrate the limitations of the initial risk scoring approach and the challenges of detecting fraud in a highly imbalanced dataset.

## 🖥️ Interactive Dashboard — FRAUD//X

The project includes a dark-themed financial transaction intelligence dashboard developed using Streamlit and Plotly.

### Dashboard Features

**1. Command Center**
- Total transaction overview
- Fraud and genuine transaction KPIs
- Fraud distribution donut chart
- Fraud count by transaction type
- Fraud activity timeline

**2. Transaction Explorer**
- Filter by transaction type
- Filter by fraud or genuine status
- Filter by transaction amount
- Explore transaction records
- Download filtered results as CSV

**3. Threat Analysis**
- Fraud amount analysis
- Experimental transaction alert categories
- Fraud rate comparison across transaction types

## 📁 Project Structure

```text
sql-fraud-detection/
│
├── sql/
│   ├── 01_schema.sql
│   ├── 02_load_clean.sql
│   ├── 03_eda.sql
│   ├── 04_rules.sql
│   ├── 05_risk_score.sql
│   ├── 06_evaluation.sql
│   └── 07_optimization.sql
│
├── images/
│
├── app.py
├── README.md
└── .gitignore
```

The original dataset and database credentials are excluded from the Git repository.

## ⚙️ How to Run the Project

### Prerequisites

- Python
- PostgreSQL
- Git
- VS Code (recommended)

### 1. Clone the repository

```bash
git clone https://github.com/gourinandhana19-gif/sql-fraud-detection.git
```

```bash
cd sql-fraud-detection
```

### 2. Install dependencies

```bash
pip install streamlit pandas plotly psycopg2-binary
```

### 3. Set up PostgreSQL

- Create or select a PostgreSQL database.
- Import the PaySim transaction dataset.
- Execute the SQL scripts in the `sql/` folder in the appropriate order.

### 4. Configure database credentials

Create a folder named `.streamlit` in the project root.

Inside it, create `secrets.toml`:

```toml
[postgres]
host = "localhost"
port = 5432
dbname = "postgres"
user = "postgres"
password = "YOUR_PASSWORD"
```

Replace the placeholder with your local PostgreSQL password.

**Important:** Never upload `secrets.toml` or database credentials to GitHub.

### 5. Run the dashboard

```bash
streamlit run app.py
```

The dashboard will open in your browser.

## ⚠️ Limitations

- PaySim is a synthetic dataset and may not represent all real-world financial transaction behaviours.
- The detection rules are experimental and may produce false positives.
- The initial risk scoring system requires further improvement.
- The current dashboard displays historical dataset analysis, not live financial transaction monitoring.
- The experimental alert categories are rule-based and are not a validated machine learning prediction model.

## 🚀 Future Improvements

- Improve fraud detection rules to reduce false positives.
- Develop and evaluate machine learning-based fraud detection models.
- Explore transaction velocity and behavioural patterns.
- Improve risk scoring using more effective features.
- Deploy the dashboard with a securely hosted database.
- Add more advanced interactive visualisations.

## 👩‍💻 Author

**Gouri Nandhana K S**

BCA Student | Aspiring Data Analyst

[GitHub](https://github.com/gourinandhana19-gif)

---

*Built as a hands-on project to explore SQL, financial transaction analytics, fraud detection and interactive data visualisation.*
