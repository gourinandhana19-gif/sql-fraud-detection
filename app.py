
import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="FRAUD//X | Intelligence System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# CYBERPUNK CSS
# --------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(circle at 10% 10%, #17234a 0%, transparent 35%),
        radial-gradient(circle at 90% 80%, #35152d 0%, transparent 30%),
        #070B16;
    color: #EAF1FF;
    font-family: 'Inter', sans-serif;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    letter-spacing: 1px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #10182B, #090E1B);
    border-right: 1px solid #243654;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #151F35, #0D1527);
    border: 1px solid #263C5E;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 0 18px rgba(0, 210, 255, 0.06);
}

[data-testid="stMetricLabel"] {
    color: #9AAEC9 !important;
    font-size: 13px;
}

[data-testid="stMetricValue"] {
    color: #F1F6FF !important;
    font-family: 'Orbitron', sans-serif;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #263C5E;
    border-radius: 14px;
    background: rgba(17, 27, 48, 0.72);
}

.stButton > button {
    background: linear-gradient(90deg, #00D9FF, #755CFF);
    color: #06101D;
    border: none;
    border-radius: 8px;
    font-weight: 800;
    transition: 0.3s;
}

.stButton > button:hover {
    box-shadow: 0 0 20px #00D9FF;
    transform: translateY(-2px);
}

div[data-baseweb="select"] > div {
    background-color: #111C30;
    border-color: #314765;
}

hr {
    border-color: #263C5E;
}

.hero {
    padding: 28px;
    border: 1px solid #26476B;
    border-radius: 18px;
    background: linear-gradient(115deg, #111D35, #21132F 70%, #35152B);
    box-shadow: 0 0 35px rgba(0, 217, 255, 0.08);
    margin-bottom: 25px;
}

.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: 3px;
    color: #FFFFFF;
}

.hero-sub {
    color: #A6BBD7;
    font-size: 14px;
    margin-top: 8px;
}

.status {
    display: inline-block;
    color: #53F5B2;
    border: 1px solid #238D6B;
    background: #102D2A;
    padding: 7px 13px;
    border-radius: 30px;
    font-size: 11px;
    letter-spacing: 1px;
    font-weight: 700;
}

.section-title {
    font-family: 'Orbitron', sans-serif;
    color: #00D9FF;
    font-size: 15px;
    letter-spacing: 2px;
    margin-top: 20px;
    margin-bottom: 12px;
}

.alert-box {
    background: linear-gradient(90deg, #351721, #211A30);
    border: 1px solid #A93D5A;
    border-left: 4px solid #FF5277;
    padding: 17px;
    border-radius: 10px;
    color: #FFDDE5;
    margin-bottom: 15px;
}

.small-note {
    color: #8295B1;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=st.secrets["postgres"]["host"],
        port=st.secrets["postgres"]["port"],
        dbname=st.secrets["postgres"]["dbname"],
        user=st.secrets["postgres"]["user"],
        password=st.secrets["postgres"]["password"]
    )


# --------------------------------------------------
# DATA FUNCTIONS
# --------------------------------------------------

@st.cache_data(ttl=300)
def get_kpis():
    conn = get_connection()

    query = """
    SELECT
        COUNT(*) AS total,
        COUNT(*) FILTER (WHERE isFraud = 1) AS fraud,
        COUNT(*) FILTER (WHERE isFraud = 0) AS genuine,
        ROUND(
            COUNT(*) FILTER (WHERE isFraud = 1) * 100.0
            / NULLIF(COUNT(*), 0), 3
        ) AS fraud_rate,
        COALESCE(
            SUM(amount) FILTER (WHERE isFraud = 1), 0
        ) AS fraud_amount
    FROM transactions;
    """

    return pd.read_sql_query(query, conn)


@st.cache_data(ttl=300)
def get_type_data():
    conn = get_connection()

    query = """
    SELECT
        type,
        COUNT(*) AS total_transactions,
        COUNT(*) FILTER (WHERE isFraud = 1) AS fraud_transactions,
        COUNT(*) FILTER (WHERE isFraud = 0) AS genuine_transactions,
        ROUND(
            COUNT(*) FILTER (WHERE isFraud = 1) * 100.0
            / NULLIF(COUNT(*), 0), 3
        ) AS fraud_percentage
    FROM transactions
    GROUP BY type
    ORDER BY fraud_transactions DESC;
    """

    return pd.read_sql_query(query, conn)


@st.cache_data(ttl=300)
def get_timeline():
    conn = get_connection()

    query = """
    SELECT
        step,
        COUNT(*) FILTER (WHERE isFraud = 1) AS fraud_count,
        COUNT(*) AS total_transactions
    FROM transactions
    GROUP BY step
    ORDER BY step;
    """

    return pd.read_sql_query(query, conn)


@st.cache_data(ttl=300)
def get_risk_data():
    conn = get_connection()

    query = """
    SELECT
        CASE
            WHEN type = 'CASH_OUT' AND amount > 2000000
                THEN 'Critical'
            WHEN type = 'CASH_OUT' AND amount > 1000000
                THEN 'High'
            WHEN type = 'TRANSFER' AND amount > 1000000
                THEN 'Medium'
            ELSE 'Other'
        END AS alert_level,
        COUNT(*) AS transactions,
        COUNT(*) FILTER (WHERE isFraud = 1) AS actual_fraud
    FROM transactions
    GROUP BY alert_level
    ORDER BY actual_fraud DESC;
    """

    return pd.read_sql_query(query, conn)


@st.cache_data(ttl=180)
def get_transactions(transaction_type, status, min_amount, max_amount):
    conn = get_connection()

    query = """
    SELECT
        step,
        type,
        amount,
        nameOrig,
        nameDest,
        oldbalanceOrg,
        newbalanceOrig,
        oldbalanceDest,
        newbalanceDest,
        isFraud
    FROM transactions
    WHERE
        (%s = 'All' OR type = %s)
        AND
        (%s = 'All' OR
            (%s = 'Fraud' AND isFraud = 1) OR
            (%s = 'Genuine' AND isFraud = 0))
        AND amount BETWEEN %s AND %s
    ORDER BY amount DESC
    LIMIT 500;
    """

    return pd.read_sql_query(
        query,
        conn,
        params=(
            transaction_type, transaction_type,
            status, status, status,
            min_amount, max_amount
        )
    )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.markdown(
        "<h2 style='color:#00D9FF;font-family:Orbitron'>⚡ FRAUD//X</h2>",
        unsafe_allow_html=True
    )

    st.caption("FINANCIAL INTELLIGENCE SYSTEM")
    st.divider()

    page = st.radio(
        "SYSTEM NAVIGATION",
        ["◈ Command Center", "◈ Transaction Explorer", "◈ Threat Analysis"]
    )

    st.divider()

    st.markdown("**SYSTEM STATUS**")
    st.markdown(
        "<span style='color:#53F5B2'>● DATABASE CONNECTED</span>",
        unsafe_allow_html=True
    )

    st.caption("DATA SOURCE: PaySim")
    st.caption("ENGINE: PostgreSQL")
    st.caption("ANALYTICS: Python + Streamlit")

    st.divider()
    st.caption("FRAUD//X  |  VERSION 2.0")


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:
    kpi = get_kpis().iloc[0]
    type_data = get_type_data()
    timeline = get_timeline()
    risk_data = get_risk_data()

except Exception as error:
    st.error("DATABASE CONNECTION FAILED")
    st.write("Check your PostgreSQL connection and .streamlit/secrets.toml file.")
    st.code(str(error))
    st.stop()


# --------------------------------------------------
# COMMAND CENTER
# --------------------------------------------------

if page == "◈ Command Center":

    st.markdown("""
    <div class="hero">
        <div class="status">● SYSTEM ONLINE</div>
        <div class="hero-title">FRAUD//X</div>
        <div class="hero-sub">
            FINANCIAL TRANSACTION INTELLIGENCE
            <br>
            Detect. Investigate. Understand.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">01 / GLOBAL THREAT OVERVIEW</div>',
                unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "TOTAL TRANSACTIONS",
        f"{int(kpi['total']):,}"
    )

    col2.metric(
        "FRAUD DETECTED",
        f"{int(kpi['fraud']):,}"
    )

    col3.metric(
        "GENUINE TRANSACTIONS",
        f"{int(kpi['genuine']):,}"
    )

    col4.metric(
        "FRAUD RATE",
        f"{float(kpi['fraud_rate']):.3f}%"
    )

    st.markdown("---")

    st.markdown('<div class="section-title">02 / FRAUD INTELLIGENCE</div>',
                unsafe_allow_html=True)

    left, right = st.columns([1, 1.5])

    with left:
        st.markdown("#### Transaction Distribution")

        donut = go.Figure(
            data=[go.Pie(
                labels=["Genuine", "Fraud"],
                values=[int(kpi["genuine"]), int(kpi["fraud"])],
                hole=0.72,
                marker=dict(
                    colors=["#00D9FF", "#FF426D"],
                    line=dict(color="#0B1220", width=3)
                ),
                textinfo="percent",
                hovertemplate="%{label}: %{value:,}<extra></extra>"
            )]
        )

        donut.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=330,
            showlegend=True,
            legend=dict(orientation="h", y=-0.08),
            margin=dict(t=15, b=30, l=10, r=10)
        )

        st.plotly_chart(donut, use_container_width=True)

    with right:
        st.markdown("#### Fraud by Transaction Type")

        fig = px.bar(
            type_data,
            x="type",
            y="fraud_transactions",
            color="fraud_transactions",
            color_continuous_scale=["#263B72", "#00D9FF", "#FF426D"],
            text="fraud_transactions"
        )

        fig.update_traces(
            textposition="outside",
            hovertemplate="%{x}<br>Fraud: %{y:,}<extra></extra>"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=330,
            coloraxis_showscale=False,
            xaxis_title="Transaction Type",
            yaxis_title="Fraud Count",
            margin=dict(t=20, b=20, l=10, r=10)
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.markdown('<div class="section-title">03 / THREAT ACTIVITY TIMELINE</div>',
                unsafe_allow_html=True)

    timeline_fig = go.Figure()

    timeline_fig.add_trace(go.Scatter(
        x=timeline["step"],
        y=timeline["fraud_count"],
        mode="lines",
        name="Fraud activity",
        line=dict(color="#FF426D", width=2),
        fill="tozeroy",
        fillcolor="rgba(255,66,109,0.12)",
        hovertemplate="Step %{x}<br>Fraud: %{y:,}<extra></extra>"
    ))

    timeline_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=350,
        xaxis_title="Simulation Step",
        yaxis_title="Fraud Transactions",
        margin=dict(t=20, b=20)
    )

    st.plotly_chart(timeline_fig, use_container_width=True)

    st.markdown("---")

    st.markdown('<div class="section-title">04 / TRANSACTION INTELLIGENCE</div>',
                unsafe_allow_html=True)

    st.dataframe(
        type_data.rename(columns={
            "type": "Transaction Type",
            "total_transactions": "Total",
            "fraud_transactions": "Fraud",
            "genuine_transactions": "Genuine",
            "fraud_percentage": "Fraud Rate (%)"
        }),
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# TRANSACTION EXPLORER
# --------------------------------------------------

elif page == "◈ Transaction Explorer":

    st.markdown("""
    <div class="hero">
        <div class="status">● INVESTIGATION MODE</div>
        <div class="hero-title">TRANSACTION SCANNER</div>
        <div class="hero-sub">
            Search, filter and investigate transaction records.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">01 / SEARCH FILTERS</div>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        transaction_type = st.selectbox(
            "Transaction Type",
            ["All", "TRANSFER", "CASH_OUT", "CASH_IN", "PAYMENT", "DEBIT"]
        )

    with c2:
        status = st.selectbox(
            "Transaction Status",
            ["All", "Fraud", "Genuine"]
        )

    with c3:
        max_amount = st.number_input(
            "Maximum Amount",
            min_value=0.0,
            value=10000000.0,
            step=100000.0
        )

    min_amount = st.number_input(
        "Minimum Amount",
        min_value=0.0,
        value=0.0,
        step=100000.0
    )

    if min_amount > max_amount:
        st.error("Minimum amount cannot be greater than maximum amount.")
        st.stop()

    if st.button("⚡ SCAN TRANSACTIONS", use_container_width=True):

        with st.spinner("Scanning transaction database..."):
            try:
                results = get_transactions(
                    transaction_type,
                    status,
                    min_amount,
                    max_amount
                )

                st.session_state["search_results"] = results

            except Exception as error:
                st.error(f"Search failed: {error}")

    if "search_results" in st.session_state:

        results = st.session_state["search_results"]

        st.markdown("---")
        st.metric("RECORDS FOUND (MAX 500)", f"{len(results):,}")

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇ DOWNLOAD RESULTS AS CSV",
            data=results.to_csv(index=False).encode("utf-8"),
            file_name="fraud_transaction_results.csv",
            mime="text/csv",
            use_container_width=True
        )

        if not results.empty:
            fraud_found = int((results["isfraud"] == 1).sum())

            if fraud_found > 0:
                st.warning(
                    f"Investigation alert: {fraud_found} fraud-labelled "
                    "transactions found in these results."
                )
            else:
                st.success("No fraud-labelled transactions in these results.")


# --------------------------------------------------
# THREAT ANALYSIS
# --------------------------------------------------

elif page == "◈ Threat Analysis":

    st.markdown("""
    <div class="hero">
        <div class="status">● ANALYTICS MODE</div>
        <div class="hero-title">THREAT ANALYSIS</div>
        <div class="hero-sub">
            Explore transaction patterns and fraud indicators.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">01 / AMOUNT ANALYSIS</div>',
                unsafe_allow_html=True)

    st.metric(
        "TOTAL AMOUNT ASSOCIATED WITH FRAUD",
        f"{float(kpi['fraud_amount']):,.2f}"
    )

    st.markdown("---")

    st.markdown('<div class="section-title">02 / TRANSACTION RISK BREAKDOWN</div>',
                unsafe_allow_html=True)

    risk_fig = px.bar(
        risk_data,
        x="alert_level",
        y="transactions",
        color="alert_level",
        color_discrete_map={
            "Critical": "#FF426D",
            "High": "#FF9B54",
            "Medium": "#00D9FF",
            "Other": "#7585A6"
        },
        text="transactions"
    )

    risk_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=350,
        xaxis_title="Experimental Alert Category",
        yaxis_title="Number of Transactions",
        showlegend=False
    )

    st.plotly_chart(risk_fig, use_container_width=True)

    st.dataframe(
        risk_data.rename(columns={
            "alert_level": "Alert Category",
            "transactions": "Transactions",
            "actual_fraud": "Actual Fraud"
        }),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("""
    <div class="alert-box">
        <b>IMPORTANT ANALYTICS NOTE</b><br>
        These alert categories are experimental amount-based rules,
        not a validated fraud prediction model. Actual fraud labels
        are shown for analysis and comparison.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-title">03 / FRAUD RATE BY TRANSACTION TYPE</div>',
                unsafe_allow_html=True)

    rate_fig = px.bar(
        type_data,
        x="type",
        y="fraud_percentage",
        color="fraud_percentage",
        color_continuous_scale=["#263B72", "#00D9FF", "#FF426D"],
        text="fraud_percentage"
    )

    rate_fig.update_traces(
        texttemplate="%{text:.3f}%",
        textposition="outside"
    )

    rate_fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=350,
        coloraxis_showscale=False,
        xaxis_title="Transaction Type",
        yaxis_title="Fraud Rate (%)"
    )

    st.plotly_chart(rate_fig, use_container_width=True)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.markdown("""
<div style="text-align:center;color:#7185A5;font-size:12px;padding:15px">
    ⚡ FRAUD//X FINANCIAL INTELLIGENCE SYSTEM
    <br>
    Built with PostgreSQL · Python · Streamlit · Plotly
    <br>
    PAYSim Financial Transaction Dataset
</div>
""", unsafe_allow_html=True)
