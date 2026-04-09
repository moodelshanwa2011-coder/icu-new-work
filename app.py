import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS (النسخة المعتمدة العملاقة)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    .kpi-card {
        position: relative; background-color: #0a0a0a; border-radius: 20px;
        overflow: hidden; display: flex; flex-direction: column; justify-content: center;
        text-align: center; height: 250px; margin-bottom: 40px;
    }
    .kpi-card::before {
        content: ''; position: absolute; width: 250%; height: 250%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
    }
    .kpi-card::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 6px; border-radius: 16px;
    }
    .circle-container {
        position: relative; width: 230px; height: 230px; border-radius: 50%;
        margin: auto; overflow: hidden; display: flex; justify-content: center; align-items: center;
    }
    .circle-container::before {
        content: ''; position: absolute; width: 300%; height: 300%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 5s linear infinite; top: 50%; left: 50%;
    }
    .circle-container::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 8px; border-radius: 50%;
    }
    @keyframes rotate-wave {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    .z-layer { position: relative; z-index: 10; width: 100%; }
    .gray-label { color: #aaaaaa; font-size: 28px; font-weight: 900; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; }
    .cyan-val { color: #00d4ff; font-size: 60px; font-weight: 900; }
    .bm-full-text { color: #444444; font-size: 14px; font-weight: bold; margin-top: 10px; text-transform: uppercase; }
    .census-box-mini { background: #0a0a0a; border: 2px solid #FFD700; border-radius: 12px; padding: 15px 25px; text-align: left; max-width: 250px; margin-bottom: 20px; }
    .census-num-mini { color: #FFD700; font-size: 40px; font-weight: 900; line-height: 1; margin: 5px 0; }
    .gauge-label-bottom { color: #ffffff; font-size: 14px; font-weight: 900; text-transform: uppercase; margin-top: -20px; text-align: center; }
    .side-header { color: #00d4ff; font-size: 26px; font-weight: 900; margin-bottom: 15px; text-transform: uppercase; }
    .week-text { color: #FFD700; font-size: 18px; font-weight: bold; margin-left: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. قاعدة البيانات الكاملة لكل أسبوع
if 'week_index' not in st.session_state: st.session_state.week_index = 0

all_weeks = [
    {
        "date": "March 07", "q": "1Q 2026", "census": 30,
        "sq": [0.0, 0.0, 6.67, 1.5, 0.0, 1.2], # Falls, Inj, HAPI, CLABSI, CAUTI, VAP
        "cir": [0.45, 1.6, 2.5, 14.5, 85.0, 0.0], # Rest, VAE, Turn, Nurse, Edu, Cdiff
        "dev": [11, 27, 18, 4.1] # ETT, Foley, CVC, Stay
    },
    {
        "date": "March 14", "q": "1Q 2026", "census": 33,
        "sq": [0.1, 0.0, 7.20, 1.2, 0.2, 1.0],
        "cir": [0.50, 1.8, 2.8, 12.0, 80.0, 0.1],
        "dev": [14, 30, 21, 4.5]
    },
    {
        "date": "March 21", "census": 28, "q": "1Q 2026",
        "sq": [0.0, 0.0, 5.50, 0.8, 0.0, 1.5],
        "cir": [0.40, 1.5, 2.2, 15.0, 88.0, 0.0],
        "dev": [9, 25, 16, 3.8]
    },
    {
        "date": "March 28", "census": 35, "q": "1Q 2026",
        "sq": [0.2, 0
