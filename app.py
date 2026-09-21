import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Supermarket Sales Analysis",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Supermarket Sales Analysis Dashboard")
st.write("Upload your supermarket sales CSV file to analyze sales performance.")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # Data preprocessing
    if "Postal Code" in df.columns:
        df["Postal Code"] = df["Postal Code"].fillna(0)

    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(
            df["Order Date"], format="mixed"
        )

    if "Ship Date" in df.columns:
        df["Ship Date"] = pd.to_datetime(
            df["Ship Date"], format="mixed"
        )

    st.success("CSV file loaded successfully!")

    # ---------------- KPIs ----------------
    total_sales = df["Sales"].sum()
    average_sales = df["Sales"].mean()
    total_orders = df["Order ID"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Total Sales", f"${total_sales:,.2f}")
    col2.metric("📊 Average Sales", f"${average_sales:,.2f}")
    col3.metric("🧾 Total Orders", f"{total_orders:,}")

    st.divider()

    # ---------------- Data Preview ----------------
    st.subheader("📋 Data Preview")
    st.dataframe(df.head(10), use_container_width=True)

    # ---------------- Category Analysis ----------------
    if "Category" in df.columns:

        st.subheader("📦 Category-wise Sales")

        category_sales = (
            df.groupby("Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots()
        category_sales.plot(kind="bar", ax=ax)
        ax.set_xlabel("Category")
        ax.set_ylabel("Sales")
        ax.set_title("Sales by Category")
        st.pyplot(fig)

    # ---------------- Region Analysis ----------------
    if "Region" in df.columns:

        st.subheader("🌎 Region-wise Sales")

        region_sales = (
            df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots()
        region_sales.plot(kind="bar", ax=ax)
        ax.set_xlabel("Region")
        ax.set_ylabel("Sales")
        ax.set_title("Sales by Region")
        st.pyplot(fig)

    # ---------------- Sub-category ----------------
    if "Sub-Category" in df.columns:

        st.subheader("📊 Sub-Category Sales")

        subcategory_sales = (
            df.groupby("Sub-Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots()
        subcategory_sales.plot(kind="bar", ax=ax)
        ax.set_xlabel("Sub-Category")
        ax.set_ylabel("Sales")
        ax.set_title("Sales by Sub-Category")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # ---------------- Top Products ----------------
    if "Product Name" in df.columns:

        st.subheader("🏆 Top 10 Products")

        top_products = (
            df.groupby("Product Name")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        fig, ax = plt.subplots()
        top_products.sort_values().plot(kind="barh", ax=ax)
        ax.set_xlabel("Sales")
        ax.set_title("Top 10 Products by Sales")
        st.pyplot(fig)

    # ---------------- Top States ----------------
    if "State" in df.columns:

        st.subheader("📍 Top 10 States")

        state_sales = (
            df.groupby("State")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        fig, ax = plt.subplots()
        state_sales.plot(kind="bar", ax=ax)
        ax.set_xlabel("State")
        ax.set_ylabel("Sales")
        ax.set_title("Top 10 States by Sales")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # ---------------- Top Cities ----------------
    if "City" in df.columns:

        st.subheader("🏙️ Top 10 Cities")

        city_sales = (
            df.groupby("City")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
        )

        fig, ax = plt.subplots()
        city_sales.plot(kind="bar", ax=ax)
        ax.set_xlabel("City")
        ax.set_ylabel("Sales")
        ax.set_title("Top 10 Cities by Sales")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # ---------------- Segment ----------------
    if "Segment" in df.columns:

        st.subheader("👥 Customer Segment Sales")

        segment_sales = (
            df.groupby("Segment")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots()
        segment_sales.plot(kind="bar", ax=ax)
        ax.set_xlabel("Segment")
        ax.set_ylabel("Sales")
        ax.set_title("Sales by Customer Segment")
        st.pyplot(fig)

    # ---------------- Ship Mode ----------------
    if "Ship Mode" in df.columns:

        st.subheader("🚚 Ship Mode Sales")

        ship_mode_sales = (
            df.groupby("Ship Mode")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        fig, ax = plt.subplots()
        ship_mode_sales.plot(kind="bar", ax=ax)
        ax.set_xlabel("Ship Mode")
        ax.set_ylabel("Sales")
        ax.set_title("Sales by Ship Mode")
        plt.xticks(rotation=20)
        st.pyplot(fig)

    # ---------------- Monthly Trend ----------------
    if "Order Date" in df.columns:

        st.subheader("📈 Monthly Sales Trend")

        monthly_sales = (
            df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
            .sum()
        )

        monthly_sales.index = monthly_sales.index.astype(str)

        fig, ax = plt.subplots()
        monthly_sales.plot(kind="line", marker="o", ax=ax)
        ax.set_xlabel("Month")
        ax.set_ylabel("Sales")
        ax.set_title("Monthly Sales Trend")
        plt.xticks(rotation=45)
        st.pyplot(fig)

    # ---------------- Yearly Trend ----------------
    if "Order Date" in df.columns:

        st.subheader("📅 Yearly Sales")

        yearly_sales = (
            df.groupby(df["Order Date"].dt.year)["Sales"]
            .sum()
        )

        fig, ax = plt.subplots()
        yearly_sales.plot(kind="bar", ax=ax)
        ax.set_xlabel("Year")
        ax.set_ylabel("Sales")
        ax.set_title("Yearly Sales")
        st.pyplot(fig)

    # ---------------- Key Insights ----------------
    st.divider()
    st.subheader("💡 Key Insights")

    if "Category" in df.columns:
        top_category = category_sales.index[0]
        st.write(f"• Highest-selling category: **{top_category}**")

    if "Region" in df.columns:
        top_region = region_sales.index[0]
        st.write(f"• Highest-selling region: **{top_region}**")

    if "Sub-Category" in df.columns:
        top_subcategory = subcategory_sales.index[0]
        st.write(f"• Highest-selling sub-category: **{top_subcategory}**")

    if "State" in df.columns:
        top_state = state_sales.index[0]
        st.write(f"• Highest-selling state: **{top_state}**")

    if "Segment" in df.columns:
        top_segment = segment_sales.index[0]
        st.write(f"• Highest-selling customer segment: **{top_segment}**")

    st.success("Analysis completed successfully! 🎉")
