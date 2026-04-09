import streamlit as st
import pandas as pd
import plotly.express as px

# إعدادات الصفحة لتكون احترافية وعريضة
st.set_page_config(page_title="ICU Performance Dashboard", layout="wide")

# تنسيق العنوان والشعار
st.title("🏥 Saudi German Hospital - Riyadh")
st.subheader("Intensive Care Unit Performance Dashboard")
st.markdown("---")

# --- الجزء الأول: بيانات الـ PDF (المؤشرات المرجعية NDNQI) ---
st.header("📊 Quarterly Benchmarks & Clinical Indicators")

# تحميل البيانات (استبدل هذا بملف البيانات الخاص بك)
# df_benchmarks = pd.read_csv("icu_benchmarks.csv")

# عرض المؤشرات في كروت (Metrics) لأهم البيانات
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Falls (3Q 2025)", value="0.18", delta="Target: 0")
with col2:
    st.metric(label="CLABSI Rate", value="3.38", delta="-1.50", delta_color="inverse")
with col3:
    st.metric(label="HAPI %", value="4.58%", delta="Benchmark: 6.67%")
with col4:
    st.metric(label="RN Education (BSN+)", value="70.59%", delta="85.01%")

# عرض الجدول كاملاً بشكل منظم
with st.expander("View Full Benchmark Table (NDNQI)"):
    # هنا يتم عرض الجدول المستخرج من الـ PDF
    st.info("Historical data from 4Q 2023 to 3Q 2025")
    # st.dataframe(df_benchmarks, use_container_width=True)

st.markdown("---")

# --- الجزء الثاني: بيانات الصور (التعداد اليومي للأجهزة) ---
st.header("📅 Daily Medical Device Census - April 2026")

# تفريغ بيانات من الصور المرفقة (مثال لأول 5 أيام)
daily_data = {
    'Day': [1, 2, 3, 4, 5],
    'Patient Stay': [34, 31, 24, 25, 24],
    'Foley Catheter': [14, 16, 15, 15, 15],
    'Ventilators': [14, 13, 11, 12, 13],
    'IV Sites': [25, 29, 24, 24, 14]
}
df_daily = pd.DataFrame(daily_data)

# عرض البيانات اليومية في رسم بياني تفاعلي
fig = px.line(df_daily, x='Day', y=['Patient Stay', 'Ventilators', 'Foley Catheter'],
              title="Daily Device Utilization Trends",
              markers=True,
              color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c"])

st.plotly_chart(fig, use_container_width=True)

# عرض الجدول اليومي أسفل الرسم البياني
col_table, col_pie = st.columns([2, 1])

with col_table:
    st.subheader("Daily Census Detail")
    st.dataframe(df_daily.style.highlight_max(axis=0), use_container_width=True)

with col_pie:
    st.subheader("Device Ratio (Avg)")
    avg_data = df_daily[['Foley Catheter', 'Ventilators']].mean()
    fig_pie = px.pie(values=avg_data.values, names=avg_data.index, hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# تذييل الصفحة
st.markdown("---")
st.caption("Developed for ICU Monitoring System | Data accurate as of April 2026")
