
from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

from src.data_cleaning import clean_data
from src.analysis import (
    calculate_total_sales,
    calculate_average_sales,
    calculate_total_quantity,
    product_sales,
    daily_sales,
    generate_summary,
)

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_DATA = PROJECT_ROOT / "data" / "raw" / "sales_dataset.csv"

st.set_page_config(
    page_title="Sales EDA Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Sales Data Analysis Dashboard")
st.write(
    "Explore revenue trends, product performance, "
    "sales statistics, and business insights."
)

@st.cache_data
def load_sales_data(file_bytes):
    from io import BytesIO
    raw = pd.read_csv(BytesIO(file_bytes))
    return clean_data(raw)

uploaded_file = st.sidebar.file_uploader(
    "Upload a sales CSV (optional)",
    type=["csv"],
)

try:
    if uploaded_file is not None:
        original_df = pd.read_csv(uploaded_file)
        df = clean_data(original_df)
    else:
        if not DEFAULT_DATA.exists():
            st.error("Default sales dataset was not found.")
            st.stop()

        original_df = pd.read_csv(DEFAULT_DATA)
        df = clean_data(original_df)

except Exception as error:
    st.error(f"Could not load the dataset: {error}")
    st.stop()

required = {"Date", "Product", "Quantity", "Revenue"}
missing_columns = required - set(df.columns)

if missing_columns:
    st.error(
        "The dataset is missing required columns: "
        + ", ".join(sorted(missing_columns))
    )
    st.stop()

if df.empty:
    st.warning("No valid records remain after cleaning.")
    st.stop()

st.sidebar.success(f"{len(df):,} valid records loaded")
st.sidebar.caption("Dates and numeric values are validated during cleaning.")

st.subheader("Sales Overview")

total_revenue = calculate_total_sales(df)
average_revenue = calculate_average_sales(df)
total_quantity = calculate_total_quantity(df)
product_count = df["Product"].nunique()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Revenue", f"{total_revenue:,.2f}")
c2.metric("Average Revenue / Record", f"{average_revenue:,.2f}")
c3.metric("Quantity Sold", f"{total_quantity:,.0f}")
c4.metric("Products", f"{product_count:,}")

st.divider()

st.subheader("Explore the Data")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.date_input(
    "Filter by date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

filtered = df.copy()

if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        (filtered["Date"].dt.date >= start_date)
        & (filtered["Date"].dt.date <= end_date)
    ]

if filtered.empty:
    st.warning("No sales records match this date range.")
    st.stop()

left, right = st.columns(2)

with left:
    st.markdown("#### Revenue by Product")
    revenue_by_product = product_sales(filtered)
    fig, ax = plt.subplots(figsize=(8, 4))
    revenue_by_product.plot(kind="bar", ax=ax)
    ax.set_xlabel("Product")
    ax.set_ylabel("Revenue")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.markdown("#### Revenue Trend Over Time")
    trend = daily_sales(filtered).sort_index()
    fig, ax = plt.subplots(figsize=(8, 4))
    trend.plot(kind="line", marker="o", ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue")
    fig.autofmt_xdate()
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

left, right = st.columns(2)

with left:
    st.markdown("#### Revenue Share by Product")
    share = product_sales(filtered)
    fig, ax = plt.subplots(figsize=(7, 5))
    share.plot(kind="pie", autopct="%1.1f%%", ax=ax, ylabel="")
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with right:
    st.markdown("#### Quantity Sold by Product")
    quantity_by_product = (
        filtered.groupby("Product")["Quantity"]
        .sum()
        .sort_values(ascending=False)
    )
    fig, ax = plt.subplots(figsize=(8, 4))
    quantity_by_product.plot(kind="bar", ax=ax)
    ax.set_xlabel("Product")
    ax.set_ylabel("Quantity")
    ax.tick_params(axis="x", rotation=35)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()
st.subheader("🧹 Cleaned Dataset")
st.caption(
    "Cleaning removes duplicate records, invalid dates, missing required "
    "values, and negative quantities or revenue."
)
st.dataframe(filtered, use_container_width=True, hide_index=True)

st.download_button(
    "Download cleaned sales data (CSV)",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="cleaned_sales_data.csv",
    mime="text/csv",
)

st.divider()
st.subheader("💡 Business Insights")

summary = generate_summary(filtered)

st.write(
    f"**Total revenue:** {summary['Total Revenue']:,.2f} "
    f"across the selected records."
)
st.write(
    f"**Average revenue per record:** "
    f"{summary['Average Revenue']:,.2f}."
)
st.write(
    f"**Total quantity sold:** "
    f"{summary['Total Quantity Sold']:,.0f}."
)

revenue_by_product = product_sales(filtered)
best_product = revenue_by_product.idxmax()
lowest_product = revenue_by_product.idxmin()

st.write(
    f"**Top revenue product:** {best_product} "
    f"({revenue_by_product.max():,.2f})."
)
st.write(
    f"**Lowest revenue product:** {lowest_product} "
    f"({revenue_by_product.min():,.2f})."
)

daily = daily_sales(filtered)
best_date = daily.idxmax()

st.write(
    f"**Highest revenue date:** {best_date:%Y-%m-%d} "
    f"({daily.max():,.2f})."
)

st.caption(
    "Insights describe the selected dataset and date range. "
    "They are descriptive, not forecasts or proof of causation."
)
