
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Netflix Churn Analytics",
    page_icon="🎬",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("netflix_customer_churn-selected-columns.csv")

df = load_data()

st.title("🎬 Netflix Customer Churn Analytics")
st.subheader("Customer Behaviour and Churn Analysis")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

plans = st.sidebar.multiselect(
    "Subscription Type",
    df["subscription_type"].unique(),
    default=list(df["subscription_type"].unique())
)

regions = st.sidebar.multiselect(
    "Region",
    df["region"].unique(),
    default=list(df["region"].unique())
)

devices = st.sidebar.multiselect(
    "Device",
    df["device"].unique(),
    default=list(df["device"].unique())
)

filtered = df[
    (df["subscription_type"].isin(plans)) &
    (df["region"].isin(regions)) &
    (df["device"].isin(devices))
].copy()

# KPI metrics
total = len(filtered)
churned = (filtered["churned"] == 1).sum()
retained = (filtered["churned"] == 0).sum()
churn_rate = churned / total * 100 if total else 0
avg_watch = filtered["watch_hours"].mean() if total else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Customers", total)
c2.metric("Churned Customers", churned)
c3.metric("Retained Customers", retained)
c4.metric("Churn Rate", f"{churn_rate:.1f}%")
c5.metric("Average Watch Hours", f"{avg_watch:.1f}")

st.divider()

# Prepare labels
filtered["Customer Status"] = filtered["churned"].map({
    0: "Retained",
    1: "Churned"
})

# 1. Churn distribution
st.header("1. Customer Churn Distribution")
fig1 = px.pie(
    filtered,
    names="Customer Status",
    title="Churned vs Retained Customers",
    hole=0.4
)
st.plotly_chart(fig1, use_container_width=True)

# 2. Subscription plan
st.header("2. Churn by Subscription Plan")
plan_data = filtered.groupby("subscription_type")["churned"].mean().reset_index()
plan_data["Churn Rate"] = plan_data["churned"] * 100
fig2 = px.bar(
    plan_data,
    x="subscription_type",
    y="Churn Rate",
    color="subscription_type",
    title="Churn Rate by Subscription Type"
)
st.plotly_chart(fig2, use_container_width=True)

# 3. Region
st.header("3. Churn by Region")
region_data = filtered.groupby("region")["churned"].mean().reset_index()
region_data["Churn Rate"] = region_data["churned"] * 100
fig3 = px.bar(
    region_data,
    x="region",
    y="Churn Rate",
    color="region",
    title="Regional Churn Rate"
)
st.plotly_chart(fig3, use_container_width=True)

# 4. Device
st.header("4. Churn by Device")
device_data = filtered.groupby("device")["churned"].mean().reset_index()
device_data["Churn Rate"] = device_data["churned"] * 100
fig4 = px.bar(
    device_data,
    x="device",
    y="Churn Rate",
    color="device",
    title="Churn Rate by Device"
)
st.plotly_chart(fig4, use_container_width=True)

# 5. Watch hours
st.header("5. Watch Hours vs Customer Status")
fig5 = px.box(
    filtered,
    x="Customer Status",
    y="watch_hours",
    color="Customer Status",
    title="Viewing Hours by Churn Status"
)
st.plotly_chart(fig5, use_container_width=True)

# 6. Last login
st.header("6. Customer Inactivity")
fig6 = px.histogram(
    filtered,
    x="last_login_days",
    color="Customer Status",
    barmode="overlay",
    title="Days Since Last Login"
)
st.plotly_chart(fig6, use_container_width=True)

# 7. Age group
st.header("7. Churn by Age Group")
filtered["Age Group"] = pd.cut(
    filtered["age"],
    bins=[0, 20, 30, 40, 50, 60, 100],
    labels=["Under 20", "21-30", "31-40", "41-50", "51-60", "60+"]
)
age_data = filtered.groupby("Age Group", observed=False)["churned"].mean().reset_index()
age_data["Churn Rate"] = age_data["churned"] * 100
fig7 = px.bar(
    age_data,
    x="Age Group",
    y="Churn Rate",
    title="Churn Rate by Age Group"
)
st.plotly_chart(fig7, use_container_width=True)

# 8. Gender
st.header("8. Churn by Gender")
gender_data = filtered.groupby("gender")["churned"].mean().reset_index()
gender_data["Churn Rate"] = gender_data["churned"] * 100
fig8 = px.bar(
    gender_data,
    x="gender",
    y="Churn Rate",
    title="Churn Rate by Gender"
)
st.plotly_chart(fig8, use_container_width=True)

# 9. Monthly fee
st.header("9. Monthly Fee Analysis")
fig9 = px.box(
    filtered,
    x="Customer Status",
    y="monthly_fee",
    color="Customer Status",
    title="Monthly Fee by Customer Status"
)
st.plotly_chart(fig9, use_container_width=True)

# 10. Watch hours vs inactivity
st.header("10. Customer Engagement")
fig10 = px.scatter(
    filtered,
    x="watch_hours",
    y="last_login_days",
    color="Customer Status",
    hover_data=["subscription_type", "region"],
    title="Watch Hours vs Days Since Last Login"
)
st.plotly_chart(fig10, use_container_width=True)

# 11. Customer count by plan
st.header("11. Customer Count by Subscription")
fig11 = px.histogram(
    filtered,
    x="subscription_type",
    color="Customer Status",
    barmode="group",
    title="Customer Count by Plan and Status"
)
st.plotly_chart(fig11, use_container_width=True)

# 12. Correlation heatmap
st.header("12. Correlation Analysis")
numeric = filtered.select_dtypes(include="number")
fig12 = px.imshow(
    numeric.corr(),
    text_auto=True,
    aspect="auto",
    title="Correlation Heatmap"
)
st.plotly_chart(fig12, use_container_width=True)

# Insights
st.divider()
st.header("📊 Business Insights")

if total:
    st.write(f"- The overall customer churn rate is **{churn_rate:.1f}%**.")
    st.write(f"- Average customer viewing time is **{avg_watch:.1f} hours**.")

    churned_data = filtered[filtered["churned"] == 1]
    retained_data = filtered[filtered["churned"] == 0]

    if len(churned_data) and len(retained_data):
        st.write(
            f"- Churned customers watch an average of "
            f"{churned_data['watch_hours'].mean():.1f} hours."
        )
        st.write(
            f"- Retained customers watch an average of "
            f"{retained_data['watch_hours'].mean():.1f} hours."
        )

    st.subheader("Recommendations")
    st.write("1. Offer personalised content to inactive customers.")
    st.write("2. Improve engagement among Basic plan subscribers.")
    st.write("3. Send reminders to customers who have not logged in recently.")
    st.write("4. Analyse viewing patterns to identify customers at risk of churn.")
else:
    st.warning("No customers match the selected filters.")

# Data table and download
st.divider()
st.header("Filtered Customer Data")
st.dataframe(filtered, use_container_width=True)

st.download_button(
    "Download Filtered Data as CSV",
    data=filtered.to_csv(index=False),
    file_name="filtered_netflix_customers.csv",
    mime="text/csv"
)
