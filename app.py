import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Coffee Estate Analytics",
    page_icon="☕",
    layout="wide"
)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv(
    "data/estate_data.csv",
    encoding="latin1"
)

category_mapping = {
    "Technology": "Arabica",
    "Furniture": "Robusta",
    "Office Supplies": "Liberica"
}

df["Category"] = df["Category"].replace(category_mapping)

# -----------------------------
# FORECAST MODEL
# -----------------------------
df["Order Date"] = pd.to_datetime(df["Order Date"])

daily_sales = (
    df.groupby("Order Date")["Sales"]
    .sum()
    .reset_index()
)

daily_sales["Days"] = (
    daily_sales["Order Date"]
    - daily_sales["Order Date"].min()
).dt.days

X = daily_sales[["Days"]]
y = daily_sales["Sales"]

model = LinearRegression()
model.fit(X, y)

future_days = pd.DataFrame({
    "Days": range(
        daily_sales["Days"].max() + 1,
        daily_sales["Days"].max() + 31
    )
})

predictions = model.predict(future_days)

forecast_df = pd.DataFrame({
    "Day": range(1, 31),
    "Forecast": predictions
})

# -----------------------------
# HEADER
# -----------------------------
st.title("☕ AI Coffee Estate Analytics System")

st.markdown("""
### Harvest Forecasting • Inventory Planning • Sales Intelligence

AI-powered decision support platform for estate operations,
yield forecasting, inventory visibility, and management reporting.
""")

# -----------------------------
# KPI SECTION
# -----------------------------
total_revenue = df["Sales"].sum()
total_profit = df["Profit"].sum()
total_inventory = df["Quantity"].sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "☕ Coffee Revenue",
        f"₹{total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "🌱 Estate Profitability",
        f"₹{total_profit:,.0f}"
    )

with col3:
    st.metric(
        "🏬 Warehouse Stock",
        f"{total_inventory:,.0f}"
    )

st.divider()
st.sidebar.header("Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    df["Order Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Order Date"].max()
)

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3 = st.tabs([
    "📊 Sales Intelligence",
    "📦 Inventory Analytics",
    "🌱 Harvest Forecasting"
])

# -----------------------------
# SALES TAB
# -----------------------------
with tab1:

    st.subheader("Coffee Revenue Analysis")

    sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        sales,
        x="Category",
        y="Sales",
        title="Revenue by Coffee Variety"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # Coffee Variety Comparison
    st.subheader("Coffee Variety Comparison")

    variety_sales = (
        df.groupby("Category")["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        variety_sales,
        values="Profit",
        names="Category",
        title="Profit Contribution by Coffee Variety"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.markdown("""
    **Business Insight:**  

    Arabica, Robusta, and Liberica varieties contribute differently to estate profitability.
    This visualization helps management identify the most profitable coffee variety and
    optimize cultivation and harvesting strategies.
    """)
# -----------------------------
# INVENTORY TAB
# -----------------------------
with tab2:

    st.subheader("Inventory Visibility")

    inventory = (
        df.groupby("Category")["Quantity"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        inventory,
        x="Category",
        y="Quantity",
        title="Warehouse Stock by Coffee Variety"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.markdown("""
    **Business Insight:**  
    Enables inventory monitoring and stock planning.
    """)


# -----------------------------
# FORECAST TAB
# -----------------------------
with tab3:

    st.subheader("🌱 AI Harvest Forecast")

    st.info(
        "Climate Simulation Engine: Adjust weather conditions to observe their impact on predicted coffee yield."
    )

    rainfall = st.slider(
        "Rainfall (mm)",
        0,
        100,
        50
    )

    temperature = st.slider(
        "Temperature (°C)",
        15,
        40,
        25
    )

    adjustment = (
        rainfall * 0.2
        - temperature * 0.1
    )

    adjusted_predictions = predictions + adjustment

    historical_avg = daily_sales["Sales"].mean()
    forecast_mean = adjusted_predictions.mean()

    if forecast_mean > historical_avg * 1.10:
        risk = "🟢 Low Risk"
    elif forecast_mean > historical_avg * 0.90:
        risk = "🟡 Medium Risk"
    else:
        risk = "🔴 High Risk"

    forecast_df["Forecast"] = adjusted_predictions
    forecast_df["Upper"] = forecast_df["Forecast"] * 1.05
    forecast_df["Lower"] = forecast_df["Forecast"] * 0.95

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Expected Next-Day Yield",
            f"{adjusted_predictions[0]:.0f}"
        )

    with col2:
        st.metric(
            "Expected 30-Day Yield",
            f"{adjusted_predictions.sum():,.0f}"
        )

    with col3:
        st.metric(
            "Harvest Risk Score",
            risk
        )

    st.subheader("Estate Health Index")

    health_index = min(
        100,
        max(
            0,
            int(
                (rainfall * 0.7)
                - (temperature * 0.3)
                + 40
            )
        )
    )

    st.progress(health_index / 100)

    st.write(
        f"🌱 Estate Health Index: {health_index}/100"
    )

    st.subheader("AI Recommendation Engine")

    if health_index >= 80:
        st.success(
            "Excellent growing conditions detected. Increase harvest preparation and workforce allocation."
        )

    elif health_index >= 60:
        st.warning(
            "Moderate growing conditions detected. Monitor weather trends and inventory levels."
        )

    else:
        st.error(
            "Potential production risk detected. Consider irrigation, crop protection, and contingency planning."
        )

    fig = px.line(
        forecast_df,
        x="Day",
        y=["Forecast", "Upper", "Lower"],
        title="30-Day Coffee Harvest Forecast"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    if adjusted_predictions.mean() > historical_avg:
        st.success(
            "AI Insight: Forecasted production is expected to exceed historical average yield."
        )
    else:
        st.warning(
            "AI Insight: Forecasted production may remain below historical average yield."
        )

    st.markdown("""
    ### Business Insight

    The AI forecasting engine analyzes historical production trends and
    simulates climate conditions to estimate future harvest output.

    - Forecast Line → Expected Harvest Yield
    - Upper Bound → Best-Case Scenario (+5%)
    - Lower Bound → Conservative Scenario (-5%)

    This supports workforce planning, inventory preparation,
    procurement decisions, and harvest scheduling.
    """)
def generate_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Coffee Estate Analytics Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"Total Revenue: ₹{total_revenue:,.0f}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Total Profit: ₹{total_profit:,.0f}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Warehouse Stock: {total_inventory:,.0f}",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            "This report was generated using the AI Coffee Estate Analytics System.",
            styles["BodyText"]
        )
    )

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf

# -----------------------------
# DATA PREVIEW
# -----------------------------
st.divider()

st.subheader("Operational Data Preview")

st.dataframe(
    df.head(25),
    width="stretch"
)
st.divider()
def generate_pdf():

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Coffee Estate Analytics Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"Total Revenue: ₹{total_revenue:,.0f}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Total Profit: ₹{total_profit:,.0f}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Warehouse Stock: {total_inventory:,.0f}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Expected Next-Day Yield: {adjusted_predictions[0]:.0f}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Expected 30-Day Yield: {adjusted_predictions.sum():,.0f}",
            styles["BodyText"]
        )
    )

    elements.append(
        Paragraph(
            f"Estate Health Index: {health_index}/100",
            styles["BodyText"]
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"Harvest Risk Score: {risk}",
            styles["BodyText"]
        )
    )

    doc.build(elements)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf
pdf = generate_pdf()

st.download_button(
    label="📄 Download Estate Analytics PDF",
    data=pdf,
    file_name="Coffee_Estate_Analytics_Report.pdf",
    mime="application/pdf"
)

st.subheader("Estate Operations Map")

map_data = pd.DataFrame({
    "lat": [
        13.3153,  # Chikkamagaluru
        12.4244,  # Kodagu (Madikeri)
        13.0072   # Hassan
    ],
    "lon": [
        75.7754,
        75.7382,
        76.0963
    ],
    "Location": [
        "Arabica Plantation - Chikkamagaluru",
        "Robusta Plantation - Kodagu",
        "Processing & Logistics Center - Hassan"
    ]
})

st.markdown("""
This map represents major coffee production and processing locations
across Karnataka used in the prototype analytics platform.
""")

fig = px.scatter_map(
    map_data,
    lat="lat",
    lon="lon",
    hover_name="Location",
    zoom=6,
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# -----------------------------
# EXECUTIVE SUMMARY
# -----------------------------
st.divider()

st.subheader("Executive Summary")

st.info("""
This AI-powered analytics platform demonstrates:

• Harvest Forecasting

• Inventory Planning

• Revenue Intelligence

• Operational Visibility

• Data-Driven Decision Support

The production version can be integrated directly with estate records,
yield data, warehouse inventory, procurement records, and sales transactions
to provide real-time management insights and predictive planning capabilities.
""")
import plotly.figure_factory as ff

corr = df[["Sales","Profit","Quantity"]].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    title="Operational Correlation Matrix"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# FOOTER
# -----------------------------
st.caption(
    "Prototype Version | AI Coffee Estate Analytics System | Developed by Nithya"
)