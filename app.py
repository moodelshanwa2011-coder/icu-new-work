import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Performance Hub", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المستقر والاحترافي
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    /* حركة الموجة النيونية للمربعات والدوائر */
    .wave-container {
        position: relative; background-color: #0a0a0a; border-radius: 12px;
        overflow: hidden; display: flex; flex-direction: column; justify-content: center;
        text-align: center; height: 155px; margin-bottom: 10px;
    }
    .wave-container::before {
        content: ''; position: absolute; width: 200%; height: 200%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
    }
    .wave-container::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 3px; border-radius: 10px;
    }
    
    .wave-circle-outer {
        position: relative; width: 130px; height: 130px; border-radius: 50%;
        margin: auto; overflow: hidden; display: flex; justify-content: center; align-items: center;
    }
    .wave-circle-outer::before {
        content: ''; position: absolute; width: 200%; height: 200%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 5s linear infinite; top: 50%; left: 50%;
    }
    .wave-circle-outer::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 4px; border-radius: 50%;
    }

    @keyframes rotate-wave {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }

    .z-layer { position: relative; z-index: 10; width: 100%; }
    
    /* المسميات والقيم */
    .gray-label { color: #aaaaaa; font-size: 13px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; }
    .cyan-val { color: #00d4ff; font-size: 32px; font-weight: 900; }
    .bm-text { color: #444444; font-size: 11px; font-weight: bold; margin-top: 4px; }

    /* كارت Census الذهبي */
    .census-container {
        background: #0a0a0a; border-left: 6px solid #FFD700; border-radius: 10px; 
        padding: 25px; text-align: center; margin-bottom: 30px;
    }
    .census-big-num { color: #FFD700; font-size: 55px; font-weight: 900; line-height: 1; }

    /* كروت الأجهزة */
    .device-row { 
        background: #0f0f0f; border-left: 3px solid #00d4ff; 
        border-radius: 4px; padding: 14px; margin-bottom: 12px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .device-name { color: #888; font-size: 12px; font-weight: bold; text-transform: uppercase; }
    .device-val { color: #00d4ff; font-size: 24px; font-weight: 900; }

    .side-header { color: #00d4ff; font-size: 22px; font-weight: 900; margin-bottom: 25px; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. داتا المؤشرات الـ 12 كاملة
data_source = [
    {
        "period": "CYCLE A - 2026",
        "squares": [("Falls", 0.0, 0.18), ("Injuries", 0.0, 0.04), ("HAPI %", 6.67, 4.58), ("CLABSI", 1.5, 3.3), ("CAUTI", 0.0, 0.4), ("VAP", 1.2, 2.1)],
        "circles": [("Restraints", 0.45, 0.9), ("VAE Rate", 1.6, 3.4), ("Turnover", 2.5, 3.0), ("Nurse Hr", 14.5, 12.0), ("RN Edu", 85.0, 70.5), ("C-Diff", 0.0, 0.1)],
        "census": 32, "occ": "88.9%", "ett": 14, "foley": 18, "cvc": 9, "stay": 3.4
    },
    {
        "period": "CYCLE B - 2025",
        "squares": [("Falls", 0.2, 0.1), ("Injuries", 0.1, 0.0), ("HAPI %", 11.0, 6.0), ("CLABSI", 1.2, 2.5), ("CAUTI", 0.5, 0.8), ("VAP", 2.0, 2.1)],
        "circles": [("Restraints", 0.6, 0.9), ("VAE Rate", 2.0, 3.4), ("Turnover", 3.0, 3.0), ("Nurse Hr", 12.0, 12.0), ("RN Edu", 80.0, 70.0), ("C-Diff", 0.1, 0.1)],
        "census": 30, "occ": "83.3%", "ett": 11, "foley": 15, "cvc": 10, "stay": 2.8
    }
]
d = data_source[st.session_state.step % 2]

# الهيدر
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 40px; font-weight:900;'>ICU STRATEGIC COMMAND HUB</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #444; font-weight: bold;'>{d['period']}</p>", unsafe_allow_html=True)

# 4. المربعات الـ 6 (الصف الأول)
cols1 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['squares']):
    color = "#00ffaa" if val <= bm else "#ff4b4b"
    with cols1[i]:
        st.markdown(f"""<div class="wave-container"><div class="z-layer">
            <div class="gray-label">{lab}</div>
            <div class="cyan-val" style="color:{color}">{val}</div>
            <div class="bm-text">BENCHMARK: {bm}</div>
        </div></div>""", unsafe_allow_html=True)

# 5. الدوائر الـ 6 (الصف الثاني - رجعت كما طلبت)
cols2 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['circles']):
    is_rev = any(x in lab for x in ["Hr", "Edu"])
    color = "#00ffaa
