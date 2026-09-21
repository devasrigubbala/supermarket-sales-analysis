import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="SuperMart Analytics",
    page_icon="🛒",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fb;
    }

    .hero {
        background: linear-gradient(135deg, #172554, #2563eb);
        padding: 35px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .hero p {
        font-size: 17px;
        opacity: 0.9;
    }

    .card {
        background: white;
        padding: 22px;
        border-radius: 15px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        text-align: center;
    }

    .card-title {
        color: #64748b;
        font-size: 15px;
    }

    .card-value {
        color: #172554;
        font-size: 27px;
        font-weight: bold;
    }

    .section-title {
        color: #172554;
        font-size: 25px;
        font-weight: bold;
        margin-top: 25px;
    }

    .insight {
        background: white;
        padding: 15px 20px;
        border-radius: 12px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }

    footer {
        text-align: center;
        padding: 25px;
        color: #64748b;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## 🛒 SuperMart")
    st.write("Sales Analytics Platform")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "📊 Sales Analysis",
            "📋 Data Preview"
        ]
    )

    st.divider()
    st.caption("Data Detectives")
    st.caption("Supermarket Sales Analysis")


# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>🛒 SuperMart Analytics</h1>
    <p>Smart sales insights from your supermarket data</p>
</div>
""", unsafe_allow_html=True)


# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader(
    "📤 Upload your supermarket CSV file",
    type=["csv"]
)

if uploaded_file is None:

    st.info(
        "👆 Upload your CSV file to start analysing supermarket sales."
    )

    st.markdown("""
    ### What this dashboard provides

    📈 Sales trends  
    📦 Category performance  
    🌎 Regional analysis  
    🏆 Top products  
    📍 Top states and cities  
    👥 Customer segment analysis  
    🚚 Shipping mode analysis  
    💡 Automatic business insights
    """)

else:

    # ---------------- LOAD DATA ----------------
    df = pd.read_csv(uploaded_file)

    # ---------------- PREPROCESSING ----------------
    if "Postal Code" in df.columns:
        df["Postal Code"] = df["Postal Code"].fillna(0)

    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(
            df["Order Date"],
            format="mixed",
            errors="coerce"
        )

    if "Ship Date" in df.columns:
        df["Ship Date"] = pd.to_datetime(
            df["Ship Date"],
            format="mixed",
            errors="coerce"
        )

    st.success("✅ CSV file loaded successfully!")

    # ---------------- KPI CALCULATIONS ----------------
       total_sales = filtered_df["Sales"].sum()

    average_sales = filtered_df["Sales"].mean()

    total_orders = (
        filtered_df["Order ID"].nunique()
        if "Order ID" in filtered_df.columns
        else len(filtered_df)
    )

    total_products = (
        filtered_df["Product Name"].nunique()
        if "Product Name" in filtered_df.columns
        else 0
    )

    # ---------------- DASHBOARD ----------------
    if page == "🏠 Dashboard":

        st.markdown(
            '<div class="section-title">📊 Business Overview</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">💰 Total Sales</div>
                <div class="card-value">${total_sales:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">📈 Average Sale</div>
                <div class="card-value">${average_sales:,.2f}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">🧾 Total Orders</div>
                <div class="card-value">{total_orders:,}</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="card">
                <div class="card-title">📦 Products</div>
                <div class="card-value">{total_products:,}</div>
            </div>
            """, unsafe_allow_html=True)

        # -------- QUICK ANALYSIS --------
                # -------- SEARCH & FILTER --------

        st.markdown(
            '<div class="section-title">🔎 Search & Filter</div>',
            unsafe_allow_html=True
        )

        filter_col1, filter_col2, filter_col3 = st.columns(3)

        with filter_col1:
            search_product = st.text_input(
                "🔍 Search Product",
                placeholder="Type product name..."
            )

        with filter_col2:
            if "Category" in df.columns:
                selected_category = st.selectbox(
                    "📦 Category",
                    ["All"] + sorted(df["Category"].dropna().unique().tolist())
                )
            else:
                selected_category = "All"

        with filter_col3:
            if "Region" in df.columns:
                selected_region = st.selectbox(
                    "🌎 Region",
                    ["All"] + sorted(df["Region"].dropna().unique().tolist())
                )
            else:
                selected_region = "All"
        # -------- DATE FILTER --------

        if "Order Date" in df.columns:

            date_col1, date_col2 = st.columns(2)

            with date_col1:
                start_date = st.date_input(
                    "📅 Start Date",
                    value=df["Order Date"].min().date()
                )

            with date_col2:
                end_date = st.date_input(
                    "📅 End Date",
                    value=df["Order Date"].max().date()
                )
            filtered_df = df.copy()

        # Apply Date Filter
        if "Order Date" in filtered_df.columns:
            filtered_df = filtered_df[
                (filtered_df["Order Date"].dt.date >= start_date) &
                (filtered_df["Order Date"].dt.date <= end_date)
            ]   
        if search_product:
            filtered_df = filtered_df[
                filtered_df["Product Name"]
                .astype(str)
                .str.contains(search_product, case=False, na=False)
            ]

        if selected_category != "All":
            filtered_df = filtered_df[
                filtered_df["Category"] == selected_category
            ]

        if selected_region != "All":
            filtered_df = filtered_df[
                filtered_df["Region"] == selected_region
            ]

        st.info(
            f"🔎 Showing {len(filtered_df):,} records"
        )

        col1, col2 = st.columns(2)

        if "Category" in df.columns:

            category_sales = (
                df.groupby("Category")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            with col1:

                st.markdown(
                    '<div class="section-title">📦 Category Sales</div>',
                    unsafe_allow_html=True
                )

                fig, ax = plt.subplots(figsize=(7, 4))

                category_sales.plot(
                    kind="bar",
                    ax=ax
                )

                ax.set_ylabel("Sales")
                ax.set_xlabel("Category")
                ax.set_title("Sales by Category")

                plt.xticks(rotation=0)

                st.pyplot(fig)

        if "Region" in df.columns:

            region_sales = (
                df.groupby("Region")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            with col2:

                st.markdown(
                    '<div class="section-title">🌎 Regional Sales</div>',
                    unsafe_allow_html=True
                )

                fig, ax = plt.subplots(figsize=(7, 4))

                region_sales.plot(
                    kind="bar",
                    ax=ax
                )

                ax.set_ylabel("Sales")
                ax.set_xlabel("Region")
                ax.set_title("Sales by Region")

                plt.xticks(rotation=0)

                st.pyplot(fig)

        # -------- MONTHLY TREND --------

        if "Order Date" in df.columns:

            monthly_sales = (
                df.groupby(
                    df["Order Date"].dt.to_period("M")
                )["Sales"]
                .sum()
            )

            monthly_sales.index = monthly_sales.index.astype(str)

            st.markdown(
                '<div class="section-title">📈 Monthly Sales Trend</div>',
                unsafe_allow_html=True
            )

            fig, ax = plt.subplots(figsize=(14, 5))

            monthly_sales.plot(
                kind="line",
                marker="o",
                ax=ax
            )

            ax.set_xlabel("Month")
            ax.set_ylabel("Sales")
            ax.set_title("Monthly Sales Performance")

            plt.xticks(rotation=45)

            st.pyplot(fig)

        # -------- INSIGHTS --------

        st.markdown(
            '<div class="section-title">💡 Key Business Insights</div>',
            unsafe_allow_html=True
        )

        if "Category" in df.columns:

            top_category = category_sales.index[0]

            st.markdown(
                f'<div class="insight">📦 Highest-selling category: <b>{top_category}</b></div>',
                unsafe_allow_html=True
            )

        if "Region" in df.columns:

            top_region = region_sales.index[0]

            st.markdown(
                f'<div class="insight">🌎 Highest-selling region: <b>{top_region}</b></div>',
                unsafe_allow_html=True
            )

        if "Product Name" in df.columns:

            product_sales = (
                df.groupby("Product Name")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            top_product = product_sales.index[0]

            st.markdown(
                f'<div class="insight">🏆 Top-selling product: <b>{top_product}</b></div>',
                unsafe_allow_html=True
            )

        if "State" in df.columns:

            state_sales = (
                df.groupby("State")["Sales"]
                .sum()
                .sort_values(ascending=False)
            )

            top_state = state_sales.index[0]

            st.markdown(
                f'<div class="insight">📍 Highest-sales state: <b>{top_state}</b></div>',
                unsafe_allow_html=True
            )

    # ---------------- SALES ANALYSIS ----------------
    elif page == "📊 Sales Analysis":

        st.markdown(
            '<div class="section-title">📊 Detailed Sales Analysis</div>',
            unsafe_allow_html=True
        )

        tab1, tab2, tab3, tab4 = st.tabs([
            "🏆 Products",
            "📍 Location",
            "👥 Customers",
            "🚚 Shipping"
        ])

        # PRODUCTS
        with tab1:

            if "Sub-Category" in df.columns:

                subcategory_sales = (
                    df.groupby("Sub-Category")["Sales"]
                    .sum()
                    .sort_values(ascending=False)
                )

                st.subheader("📦 Sub-Category Sales")

                fig, ax = plt.subplots(figsize=(12, 5))

                subcategory_sales.plot(
                    kind="bar",
                    ax=ax
                )

                ax.set_ylabel("Sales")
                ax.set_xlabel("Sub-Category")

                plt.xticks(rotation=45)

                st.pyplot(fig)

            if "Product Name" in df.columns:

                product_sales = (
                    df.groupby("Product Name")["Sales"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(10)
                )

                st.subheader("🏆 Top 10 Products")

                fig, ax = plt.subplots(figsize=(12, 5))

                product_sales.sort_values().plot(
                    kind="barh",
                    ax=ax
                )

                ax.set_xlabel("Sales")

                st.pyplot(fig)

        # LOCATION
        with tab2:

            if "State" in df.columns:

                state_sales = (
                    df.groupby("State")["Sales"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(10)
                )

                st.subheader("📍 Top 10 States")

                fig, ax = plt.subplots(figsize=(12, 5))

                state_sales.plot(
                    kind="bar",
                    ax=ax
                )

                ax.set_ylabel("Sales")

                plt.xticks(rotation=45)

                st.pyplot(fig)

            if "City" in df.columns:

                city_sales = (
                    df.groupby("City")["Sales"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(10)
                )

                st.subheader("🏙️ Top 10 Cities")

                fig, ax = plt.subplots(figsize=(12, 5))

                city_sales.plot(
                    kind="bar",
                    ax=ax
                )

                ax.set_ylabel("Sales")

                plt.xticks(rotation=45)

                st.pyplot(fig)

        # CUSTOMERS
        with tab3:

            if "Segment" in df.columns:

                segment_sales = (
                    df.groupby("Segment")["Sales"]
                    .sum()
                    .sort_values(ascending=False)
                )

                st.subheader("👥 Customer Segment Sales")

                fig, ax = plt.subplots(figsize=(10, 5))

                segment_sales.plot(
                    kind="bar",
                    ax=ax
                )

                ax.set_ylabel("Sales")

                plt.xticks(rotation=0)

                st.pyplot(fig)

        # SHIPPING
        with tab4:

            if "Ship Mode" in df.columns:

                ship_mode_sales = (
                    df.groupby("Ship Mode")["Sales"]
                    .sum()
                    .sort_values(ascending=False)
                )

                st.subheader("🚚 Ship Mode Sales")

                fig, ax = plt.subplots(figsize=(10, 5))

                ship_mode_sales.plot(
                    kind="bar",
                    ax=ax
                )

                ax.set_ylabel("Sales")

                plt.xticks(rotation=20)

                st.pyplot(fig)

    # ---------------- DATA PREVIEW ----------------
    elif page == "📋 Data Preview":

        st.markdown(
            '<div class="section-title">📋 Dataset Preview</div>',
            unsafe_allow_html=True
        )

        st.write(
            f"**Rows:** {df.shape[0]:,}  |  **Columns:** {df.shape[1]}"
        )

        st.dataframe(
            df.head(20),
            use_container_width=True
        )

        st.markdown(
            '<div class="section-title">🔍 Dataset Information</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Column Names**")
            st.write(list(df.columns))

        with col2:
            st.write("**Missing Values**")
            st.dataframe(
                df.isnull().sum().to_frame("Missing Values"),
                use_container_width=True
            )


# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<footer>
🛒 <b>SuperMart Analytics</b><br>
Supermarket Sales Analysis | Data Detectives
</footer>
""", unsafe_allow_html=True)
