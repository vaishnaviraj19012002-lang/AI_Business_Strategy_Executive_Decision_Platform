import streamlit as st
import csv
import io
import os
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Business Strategy & Executive Decision Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------------
# NORMAL WHITE THEME
# ---------------------------------------------------------
st.markdown("""
<style>

.stApp {
    background-color: #ffffff;
    color: #222222;
}

.main {
    background-color: #ffffff;
}

section[data-testid="stSidebar"] {
    background-color: #f5f7fa;
    border-right: 1px solid #dddddd;
}

section[data-testid="stSidebar"] * {
    color: #222222 !important;
}

h1 {
    color: #1f2937 !important;
    font-weight: 700;
}

h2, h3 {
    color: #1f2937 !important;
}

p {
    color: #444444;
}

div[data-testid="stMetric"] {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 15px;
    border-radius: 10px;
}

.stButton > button {
    border-radius: 8px;
    border: 1px solid #d1d5db;
    background-color: #ffffff;
    color: #222222;
    padding: 8px 18px;
}

.stButton > button:hover {
    border-color: #2563eb;
    color: #2563eb;
}

[data-testid="stFileUploader"] {
    background-color: #ffffff;
    border: 1px dashed #bfc5cc;
    border-radius: 10px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.title("📊 AI Business Strategy & Executive Decision Intelligence Platform")

st.write(
    "Transform business data into executive insights, trends, risks, "
    "opportunities and strategic recommendations."
)

st.divider()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.title("📊 Business Intelligence")

uploaded_file = st.sidebar.file_uploader(
    "Upload Business Dataset",
    type=["csv"]
)

st.sidebar.divider()

menu = st.sidebar.radio(
    "Select Analysis",
    [
        "Executive Dashboard",
        "Business Performance",
        "KPI & Metrics",
        "Trends & Anomalies",
        "Customer Feedback",
        "Period Comparison",
        "Significant Business Changes",
        "Reasons Behind Changes",
        "Risks & Opportunities",
        "Executive Summary",
        "AI Recommendations",
        "Scenario Analysis",
        "AI Assistant"
    ]
)


# ---------------------------------------------------------
# WELCOME SCREEN
# ---------------------------------------------------------
if uploaded_file is None:

    st.subheader("👋 Welcome")

    st.write(
        "Upload a business CSV file from the left sidebar."
    )

    st.info(
        "The platform will analyze business performance, KPIs, "
        "trends, anomalies, customer feedback, risks, opportunities "
        "and strategic recommendations."
    )

    st.markdown("### Expected Business Data")

    st.write(
        "The dataset can contain business information such as "
        "Sales, Revenue, Profit, Expenses, Customers, Ratings, "
        "Region, Product and Date."
    )

    st.stop()


# ---------------------------------------------------------
# READ CSV
# ---------------------------------------------------------
try:

    content = uploaded_file.getvalue().decode("utf-8")

    reader = csv.DictReader(io.StringIO(content))

    rows = list(reader)

    columns = reader.fieldnames or []

except Exception as e:

    st.error(f"Unable to read CSV file: {e}")
    st.stop()


# ---------------------------------------------------------
# BASIC HELPERS
# ---------------------------------------------------------
def clean_number(value):

    if value is None:
        return None

    value = str(value).strip()

    if value == "":
        return None

    value = value.replace(",", "")
    value = value.replace("$", "")
    value = value.replace("₹", "")

    try:
        return float(value)
    except:
        return None


def find_column(keywords):

    for col in columns:

        name = col.lower()

        for keyword in keywords:

            if keyword in name:
                return col

    return None


sales_col = find_column(
    ["sales", "revenue", "turnover"]
)

profit_col = find_column(
    ["profit", "net_profit", "net profit"]
)

expense_col = find_column(
    ["expense", "expenses", "cost"]
)

customer_col = find_column(
    ["customer", "customers", "client"]
)

rating_col = find_column(
    ["rating", "score", "satisfaction"]
)

date_col = find_column(
    ["date", "month", "year"]
)

region_col = find_column(
    ["region", "location", "country", "city"]
)

product_col = find_column(
    ["product", "item", "service"]
)

feedback_col = find_column(
    ["feedback", "review", "comment"]
)


# ---------------------------------------------------------
# NUMERIC COLUMNS
# ---------------------------------------------------------
numeric_columns = []

for col in columns:

    values = [
        clean_number(row.get(col))
        for row in rows
    ]

    valid_values = [
        v for v in values
        if v is not None
    ]

    if valid_values:
        numeric_columns.append(col)


# ---------------------------------------------------------
# MISSING VALUES
# ---------------------------------------------------------
missing_total = 0

for row in rows:

    for col in columns:

        value = row.get(col)

        if value is None or str(value).strip() == "":
            missing_total += 1


# ---------------------------------------------------------
# GET NUMERIC VALUES
# ---------------------------------------------------------
def get_values(column):

    if column is None:
        return []

    result = []

    for row in rows:

        value = clean_number(row.get(column))

        if value is not None:
            result.append(value)

    return result


sales_values = get_values(sales_col)
profit_values = get_values(profit_col)
expense_values = get_values(expense_col)
customer_values = get_values(customer_col)
rating_values = get_values(rating_col)


# ---------------------------------------------------------
# EXECUTIVE DASHBOARD
# ---------------------------------------------------------
if menu == "Executive Dashboard":

    st.header("📊 Executive Dashboard")

    st.write(
        "High-level view of the uploaded business dataset."
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Records",
        len(rows)
    )

    c2.metric(
        "Columns",
        len(columns)
    )

    c3.metric(
        "Numeric Columns",
        len(numeric_columns)
    )

    c4.metric(
        "Missing Values",
        missing_total
    )

    st.divider()

    st.subheader("Business Overview")

    if sales_values:
        st.metric(
            "Total Sales / Revenue",
            f"{sum(sales_values):,.2f}"
        )

    if profit_values:
        st.metric(
            "Total Profit",
            f"{sum(profit_values):,.2f}"
        )

    if customer_values:
        st.metric(
            "Total Customers",
            f"{sum(customer_values):,.0f}"
        )

    if rating_values:
        st.metric(
            "Average Rating",
            f"{sum(rating_values) / len(rating_values):.2f}"
        )

    st.divider()

    st.subheader("Dataset Preview")

    for index, row in enumerate(rows[:5], start=1):

        with st.expander(f"Record {index}"):

            for col in columns:

                st.write(
                    f"**{col}:** {row.get(col, '')}"
                )


# ---------------------------------------------------------
# BUSINESS PERFORMANCE
# ---------------------------------------------------------
elif menu == "Business Performance":

    st.header("📈 Business Performance")

    st.write(
        "Analyze the major numerical business indicators."
    )

    if not numeric_columns:

        st.warning("No numerical business columns found.")

    else:

        for col in numeric_columns:

            values = get_values(col)

            if values:

                st.subheader(col)

                a, b, c, d = st.columns(4)

                a.metric(
                    "Total",
                    f"{sum(values):,.2f}"
                )

                b.metric(
                    "Average",
                    f"{sum(values) / len(values):,.2f}"
                )

                c.metric(
                    "Highest",
                    f"{max(values):,.2f}"
                )

                d.metric(
                    "Lowest",
                    f"{min(values):,.2f}"
                )


# ---------------------------------------------------------
# KPI & METRICS
# ---------------------------------------------------------
elif menu == "KPI & Metrics":

    st.header("🎯 KPI & Metrics")

    st.write(
        "Key performance indicators for executive decision-making."
    )

    if sales_values:

        st.metric(
            "Total Sales",
            f"{sum(sales_values):,.2f}"
        )

        st.metric(
            "Average Sales",
            f"{sum(sales_values) / len(sales_values):,.2f}"
        )

    if profit_values:

        st.metric(
            "Total Profit",
            f"{sum(profit_values):,.2f}"
        )

        st.metric(
            "Average Profit",
            f"{sum(profit_values) / len(profit_values):,.2f}"
        )

    if expense_values:

        st.metric(
            "Total Expenses",
            f"{sum(expense_values):,.2f}"
        )

    if customer_values:

        st.metric(
            "Customers",
            f"{sum(customer_values):,.0f}"
        )

    if rating_values:

        st.metric(
            "Average Rating",
            f"{sum(rating_values) / len(rating_values):.2f}"
        )


# ---------------------------------------------------------
# TRENDS & ANOMALIES
# ---------------------------------------------------------
elif menu == "Trends & Anomalies":

    st.header("📈 Trends & Anomalies")

    st.write(
        "Identify significant movements and unusual values."
    )

    for col in numeric_columns:

        values = get_values(col)

        if len(values) >= 2:

            first_value = values[0]
            last_value = values[-1]

            if first_value != 0:

                change = (
                    (last_value - first_value)
                    / abs(first_value)
                ) * 100

                st.subheader(col)

                st.write(
                    f"Change from first record to latest record: "
                    f"**{change:.2f}%**"
                )

                if change > 0:
                    st.success("Increasing trend detected.")

                elif change < 0:
                    st.warning("Decreasing trend detected.")

                else:
                    st.info("No significant change detected.")

                average = sum(values) / len(values)

                anomalies = [
                    v for v in values
                    if abs(v) > abs(average * 2)
                ]

                if anomalies:

                    st.warning(
                        f"{len(anomalies)} unusual value(s) detected."
                    )


# ---------------------------------------------------------
# CUSTOMER FEEDBACK
# ---------------------------------------------------------
elif menu == "Customer Feedback":

    st.header("💬 Customer Feedback")

    if feedback_col is None:

        st.info(
            "No feedback/review/comment column was detected."
        )

    else:

        positive_words = [
            "good",
            "great",
            "excellent",
            "happy",
            "satisfied",
            "love",
            "positive"
        ]

        negative_words = [
            "bad",
            "poor",
            "worst",
            "unhappy",
            "problem",
            "issue",
            "negative"
        ]

        positive = 0
        negative = 0
        neutral = 0

        for row in rows:

            text_value = str(
                row.get(feedback_col, "")
            ).lower()

            if any(
                word in text_value
                for word in positive_words
            ):

                positive += 1

            elif any(
                word in text_value
                for word in negative_words
            ):

                negative += 1

            else:

                neutral += 1

        a, b, c = st.columns(3)

        a.metric("Positive", positive)
        b.metric("Negative", negative)
        c.metric("Neutral", neutral)

        st.divider()

        for row in rows[:10]:

            feedback = row.get(feedback_col, "")

            if feedback:

                st.write(f"• {feedback}")


# ---------------------------------------------------------
# PERIOD COMPARISON
# ---------------------------------------------------------
elif menu == "Period Comparison":

    st.header("📅 Period Comparison")

    st.write(
        "Compare earlier business records with recent records."
    )

    if not rows:

        st.warning("No records available.")

    else:

        midpoint = len(rows) // 2

        earlier_rows = rows[:midpoint]
        recent_rows = rows[midpoint:]

        for col in numeric_columns:

            earlier_values = [
                clean_number(row.get(col))
                for row in earlier_rows
            ]

            recent_values = [
                clean_number(row.get(col))
                for row in recent_rows
            ]

            earlier_values = [
                v for v in earlier_values
                if v is not None
            ]

            recent_values = [
                v for v in recent_values
                if v is not None
            ]

            if earlier_values and recent_values:

                earlier_avg = (
                    sum(earlier_values)
                    / len(earlier_values)
                )

                recent_avg = (
                    sum(recent_values)
                    / len(recent_values)
                )

                st.subheader(col)

                a, b = st.columns(2)

                a.metric(
                    "Earlier Period",
                    f"{earlier_avg:,.2f}"
                )

                b.metric(
                    "Recent Period",
                    f"{recent_avg:,.2f}"
                )


# ---------------------------------------------------------
# SIGNIFICANT BUSINESS CHANGES
# ---------------------------------------------------------
elif menu == "Significant Business Changes":

    st.header("🔎 Significant Business Changes")

    for col in numeric_columns:

        values = get_values(col)

        if len(values) >= 2:

            first_value = values[0]
            latest_value = values[-1]

            if first_value != 0:

                change = (
                    (latest_value - first_value)
                    / abs(first_value)
                ) * 100

                if abs(change) >= 10:

                    st.warning(
                        f"**{col}** changed by "
                        f"**{change:.2f}%**."
                    )

                else:

                    st.info(
                        f"{col}: {change:.2f}% change."
                    )


# ---------------------------------------------------------
# REASONS BEHIND CHANGES
# ---------------------------------------------------------
elif menu == "Reasons Behind Changes":

    st.header("🧠 Reasons Behind Changes")

    st.write(
        "Potential business factors that may explain observed changes."
    )

    if sales_values and len(sales_values) >= 2:

        change = (
            (sales_values[-1] - sales_values[0])
            / abs(sales_values[0])
        ) * 100

        if change > 10:

            st.success(
                "Sales increased significantly."
            )

            st.write(
                "Possible factors include increased customer demand, "
                "successful products, regional growth, pricing changes "
                "or improved market performance."
            )

        elif change < -10:

            st.warning(
                "Sales decreased significantly."
            )

            st.write(
                "Possible factors include reduced demand, pricing pressure, "
                "customer loss, higher competition or operational issues."
            )

        else:

            st.info(
                "Sales remained relatively stable."
            )

    else:

        st.info(
            "Sales data is required for this analysis."
        )


# ---------------------------------------------------------
# RISKS & OPPORTUNITIES
# ---------------------------------------------------------
elif menu == "Risks & Opportunities":

    st.header("⚠️ Risks & Opportunities")

    st.subheader("Potential Risks")

    if missing_total > 0:

        st.warning(
            f"Dataset contains {missing_total} missing value(s)."
        )

    if profit_values:

        if sum(profit_values) < 0:

            st.error(
                "Overall profit is negative."
            )

    st.write(
        "Other possible risks include declining sales, "
        "customer reduction, increasing expenses and poor ratings."
    )

    st.divider()

    st.subheader("💡 Opportunities")

    if sales_values:

        st.success(
            "Analyze high-performing sales periods, products "
            "and regions to identify growth opportunities."
        )

    if rating_values:

        st.success(
            "Customer rating patterns can be used to improve "
            "customer experience and retention."
        )


# ---------------------------------------------------------
# EXECUTIVE SUMMARY
# ---------------------------------------------------------
elif menu == "Executive Summary":

    st.header("📋 Executive Summary")

    st.write(
        "A concise summary of the business dataset."
    )

    st.write(
        f"• Total records: **{len(rows)}**"
    )

    st.write(
        f"• Total columns: **{len(columns)}**"
    )

    st.write(
        f"• Missing values: **{missing_total}**"
    )

    if sales_values:

        st.write(
            f"• Total sales/revenue: "
            f"**{sum(sales_values):,.2f}**"
        )

    if profit_values:

        st.write(
            f"• Total profit: "
            f"**{sum(profit_values):,.2f}**"
        )

    if customer_values:

        st.write(
            f"• Total customers: "
            f"**{sum(customer_values):,.0f}**"
        )

    if rating_values:

        st.write(
            f"• Average rating: "
            f"**{sum(rating_values) / len(rating_values):.2f}**"
        )


# ---------------------------------------------------------
# AI RECOMMENDATIONS
# ---------------------------------------------------------
elif menu == "AI Recommendations":

    st.header("🤖 AI Recommendations")

    st.write(
        "Generate strategic recommendations using Gemini."
    )

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:

        st.warning(
            "GEMINI_API_KEY is not configured in the .env file."
        )

    else:

        try:

            from google import genai

            client = genai.Client(
                api_key=api_key
            )

            business_context = f"""
Business dataset contains {len(rows)} records
and {len(columns)} columns.

Columns:
{columns}

Total missing values:
{missing_total}

Total sales/revenue:
{sum(sales_values) if sales_values else "Not available"}

Total profit:
{sum(profit_values) if profit_values else "Not available"}

Total expenses:
{sum(expense_values) if expense_values else "Not available"}

Customers:
{sum(customer_values) if customer_values else "Not available"}

Average rating:
{(sum(rating_values) / len(rating_values)) if rating_values else "Not available"}
"""

            prompt = f"""
Act as an executive business strategy analyst.

Analyze the following business information:

{business_context}

Provide:

1. Key business observations
2. Important performance changes
3. Major risks
4. Growth opportunities
5. Strategic recommendations
6. Executive-level actions

Keep the answer practical and concise.
"""

            if st.button("Generate AI Recommendations"):

                response = client.models.generate_content(
                    model="gemini-3.5-flash",
                    contents=prompt
                )

                st.write(response.text)

        except Exception as e:

            st.error(
                f"AI analysis error: {e}"
            )


# ---------------------------------------------------------
# SCENARIO ANALYSIS
# ---------------------------------------------------------
elif menu == "Scenario Analysis":

    st.header("📊 Scenario Analysis")

    st.write(
        "Explore simple business scenarios based on sales changes."
    )

    if sales_values:

        current_sales = sum(sales_values)

        st.subheader("Current Sales")

        st.metric(
            "Current",
            f"{current_sales:,.2f}"
        )

        st.divider()

        scenarios = {
            "10% Growth": 1.10,
            "20% Growth": 1.20,
            "10% Decline": 0.90
        }

        for name, factor in scenarios.items():

            projected = current_sales * factor

            st.write(
                f"**{name}:** "
                f"{projected:,.2f}"
            )

    else:

        st.info(
            "Sales data is required for scenario analysis."
        )


# ---------------------------------------------------------
# AI ASSISTANT
# ---------------------------------------------------------
elif menu == "AI Assistant":

    st.header("💬 AI Assistant")

    st.write(
        "Ask questions about the uploaded business dataset."
    )

    question = st.text_input(
        "Enter your business question"
    )

    api_key = os.getenv("GEMINI_API_KEY")

    if question:

        if not api_key:

            st.warning(
                "GEMINI_API_KEY is not configured."
            )

        else:

            try:

                from google import genai

                client = genai.Client(
                    api_key=api_key
                )

                context = f"""
Dataset columns:
{columns}

Number of records:
{len(rows)}

Missing values:
{missing_total}

Total sales:
{sum(sales_values) if sales_values else "Not available"}

Total profit:
{sum(profit_values) if profit_values else "Not available"}

Total expenses:
{sum(expense_values) if expense_values else "Not available"}

Customers:
{sum(customer_values) if customer_values else "Not available"}

Average rating:
{(sum(rating_values) / len(rating_values)) if rating_values else "Not available"}
"""

                prompt = f"""
You are an executive business intelligence assistant.

Business context:

{context}

User question:

{question}

Give a clear, business-focused answer.
"""

                if st.button("Ask AI"):

                    response = client.models.generate_content(
                        model="gemini-3.5-flash",
                        contents=prompt
                    )

                    st.write(response.text)

            except Exception as e:

                st.error(
                    f"AI Assistant error: {e}"
                )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.divider()

st.caption(
    "AI Business Strategy & Executive Decision Intelligence Platform"
)