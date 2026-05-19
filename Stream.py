import streamlit as st
import pandas as pd
import plotly.express as px
import random

st.set_page_config(
    page_title="Global Coal Plants Dashboard",
    layout="wide"
)

st.title("🌍 Global Coal Plants Analysis")
st.markdown("Interactive dashboard analyzing global coal power plants.")

def load_data():
    df = pd.read_csv("global-coal-plant-tracker.csv")
    df.columns = df.columns.str.lower().str.strip()
    return df


df = load_data()


st.sidebar.header("Filters")

# تجهيز الخيارات بشكل آمن
countries = list(df["country"].dropna().unique())
statuses = list(df["status"].dropna().unique())

# اختيار عشوائي أول مرة فقط (أو عند أول تشغيل)
if "rand_countries" not in st.session_state:
    st.session_state.rand_countries = random.sample(countries, min(5, len(countries)))

if "rand_status" not in st.session_state:
    st.session_state.rand_status = random.sample(statuses, min(5, len(statuses)))

# الفلاتر
country = st.sidebar.multiselect(
    "Select Country",
    countries,
    default=st.session_state.rand_countries
)

status = st.sidebar.multiselect(
    "Plant Status",
    statuses,
    default=st.session_state.rand_status
)

filtered_df = df[
    (df["country"].isin(country)) &
    (df["status"].isin(status))
]

col1, col2, col3 = st.columns(3)

col1.metric("Total Plants", len(filtered_df))
col2.metric("Total Capacity MW", int(filtered_df["capacity_mw"].sum()))
col3.metric("Countries", filtered_df["country"].nunique())

capacity_country = (
    filtered_df.groupby("country")["capacity_mw"]
    .sum()
    .reset_index()
)

fig = px.bar(
    capacity_country.sort_values("capacity_mw", ascending=False).head(10),
    x="country",
    y="capacity_mw",
    title="Top Countries by Coal Capacity",
    text="capacity_mw"   # 👈 دي أهم حاجة
)

fig.update_traces(
    texttemplate='%{text:.0f}',  # رقم بدون decimals
    textposition='outside'       # 👈 يخلي الرقم فوق العمود
)

fig.update_layout(
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

st.plotly_chart(fig, use_container_width=True)

fig2 = px.pie(
    filtered_df,
    names="status",
    title="Plant Status Distribution"
)

st.plotly_chart(fig2, use_container_width=True)



st.subheader("Which countries have the highest coal power capacity?")
capacity_country = (
    filtered_df
    .groupby("country")["capacity_mw"]
    .sum()
    .reset_index()
    .sort_values("capacity_mw", ascending=False)
)

import plotly.express as px

fig = px.bar(
    capacity_country.head(10),
    x="country",
    y="capacity_mw",
    title="Top 10 Countries by Coal Power Capacity",
    labels={
        "country": "Country",
        "capacity_mw": "Capacity (MW)"
    },
    text="capacity_mw"   # 👈 إظهار القيم
)

fig.update_traces(
    texttemplate='%{text:.0f}',  # رقم بدون كسور
    textposition='outside'       # فوق العمود
)

fig.update_layout(
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Which regions rely most on coal energy?")
region_capacity = (
    filtered_df
    .groupby("region")["capacity_mw"]
    .sum()
    .reset_index()
    .sort_values("capacity_mw", ascending=False)
)
fig = px.bar(
    region_capacity,
    x="region",
    y="capacity_mw",
    title="Coal Power Capacity by Region",
    labels={
        "region": "Region",
        "capacity_mw": "Total Capacity (MW)"
    },
    text="capacity_mw"   # 👈 إظهار القيم
)

fig.update_traces(
    texttemplate='%{text:.0f}',  # بدون كسور
    textposition='outside'       # فوق العمود
)

fig.update_layout(
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

st.plotly_chart(fig, use_container_width=True)

df_clean = filtered_df.dropna(subset=["region", "status", "capacity_mw"])
region_status = (
    df_clean
    .groupby(["region", "status"])["capacity_mw"]
    .sum()
    .reset_index()
)
import plotly.express as px

region_status_sorted = region_status.sort_values(
    by="capacity_mw",
    ascending=False
)

fig = px.bar(
    region_status_sorted,
    x="region",
    y="capacity_mw",
    color="status",
    title="Operating vs Retired Coal Capacity by Region",
    labels={
        "region": "Region",
        "capacity_mw": "Capacity (MW)",
        "status": "Status"
    },
    text="capacity_mw"   # 👈 إظهار القيم لكل جزء
)

fig.update_traces(
    texttemplate='%{text:.0f}',
    textposition='inside'  # 👈 الأفضل هنا عشان الأعمدة stacked
)

fig.update_layout(
    uniformtext_minsize=8,
    uniformtext_mode='hide'
)

st.plotly_chart(fig, use_container_width=True)


st.info(
    "This analysis highlights how coal infrastructure is distributed between operating and retired plants, "
    "revealing regional differences in energy transition progress."
)