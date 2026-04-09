
import streamlit as st
import pandas as pd
import random
import time
import plotly.express as px

# ---------- PAGE SETTINGS ----------
st.set_page_config(page_title="Live KPI Dashboard", layout="wide")

# ---------- DARK STYLE ----------
st.markdown("""
<style>
body {
    background-color:#0E1117;
}
.title {
    color:white;
    text-align:center;
    font-size:34px;
    margin-bottom:20px;
}
.circle {
    background: linear-gradient(145deg,#141E30,#243B55);
    border-radius:50%;
    height:150px;
    width:150px;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    margin:auto;
    box-shadow:0px 0px 25px rgba(0,255,255,0.15);
    border:1px solid rgba(255,255,255,0.08);
}
.number{
    font-size:34px;
    color:#00FFE0;
    font-weight:700;
}
.label{
    color:#AAB2BF;
    font-size:14px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🚀 Professional Live KPI Dashboard</div>', unsafe_allow_html=True)

placeholder = st.empty()

data = pd.DataFrame({"Time": [], "Performance": []})

# ---------- LIVE UPDATE LOOP ----------
while True:

    revenue = random.randint(3000,9000)
    users = random.randint(200,800)
    growth = random.randint(5,30)

    new_val = random.randint(80,180)

    new_row = pd.DataFrame({
        "Time":[pd.Timestamp.now()],
        "Performance":[new_val]
    })

    data = pd.concat([data, new_row]).tail(40)

    with placeholder.container():

        col1, col2, col3 = st.columns(3)

        col1.markdown(f"""
        <div class="circle">
            <div class="number">${revenue}</div>
            <div class="label">Revenue</div>
        </div>
        """, unsafe_allow_html=True)

        col2.markdown(f"""
        <div class="circle">
            <div class="number">{users}</div>
            <div class="label">Active Users</div>
        </div>
        """, unsafe_allow_html=True)

        col3.markdown(f"""
        <div class="circle">
            <div class="number">{growth}%</div>
            <div class="label">Growth Rate</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### Live Performance Trend")

        fig = px.line(
            data,
            x="Time",
            y="Performance",
            template="plotly_dark",
            markers=True
        )

        fig.update_layout(
            height=420,
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117"
        )

        st.plotly_chart(fig, use_container_width=True)

    time.sleep(2)
