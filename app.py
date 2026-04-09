import streamlit as st
import plotly.graph_objects as go
import time
import numpy as np

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="ICU Performance Core", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (حدود بارزة، مسافات واسعة، شكل موحد)
st.markdown("""
    <style>
    /* منع التمرير الجانبي، خلفية سوداء عميقة، مسافات خارجية */
    [data-testid="stAppViewContainer"] { background-color: #000000; padding: 15px 25px; }
    
    /* عنوان الأجهزة الأسبوعي الصغير */
    .week-title { color: #888; font-size: 14px; font-weight: bold; text-align: left; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1.5px; }

    /* --- تنسيق الـ 12 KPI الجديد (كروت موحدة وحدود بارزة) --- */
    .kpi-card {
        background-color: #0a0a0a; /* خلفية داكنة جداً */
        border: 2px solid #00d4ff; /* حدود بارزة جداً ومضيئة */
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px; /* مسافة أوسع بين الكروت */
        text-align: center;
        height: 160px; /* طول ثابت للكروت */
        display: flex;
        flex-direction: column;
        justify-content: center; /* تمركز محتوى الكرت رأسياً */
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .kpi-card:hover { transform: scale(1.03); box-shadow: 0 0 20px rgba(0, 212, 255, 0.3); }
    
    /* وضوح الكلام والأسماء */
    .kpi-label {
        color: #ffffff;
        font-size: 16px;
        font-weight: 900;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .kpi-value { color: #ffffff; font-size: 36px; font-weight: 900; margin: 5px 0; }
    .target-text { color: #666; font-size: 14px; font-weight: bold; margin-top: 5px; }

    /* كروت الأجهزة (يسار) وحدود زرقاء رفيعة */
    .dev-box {
        background-color: #0a0a0a; border: 1px solid #111; border-left: 4px solid #1f77b4;
        border-radius: 8px; padding: 15px; margin-bottom: 15px; text-align: center;
    }
    .dev-label { color: #aaaaaa; font-size: 14px; font-weight: bold; }
    .dev-value { color: #ffffff; font-size: 32px; font-weight: 900; }
    
    /* تمييز Total Stay باللون الأخضر */
    .stay-box { border-left: 4px solid #00CC96; background-color: #0d0d0d; box-shadow: 0 0 10px rgba(0, 212, 255, 0.1); }
    .stay-value { color: #00CC96; font-size: 45px; }

    hr { border: 0.1px solid #111; margin: 30px 0; }
    #stProgress { display: none; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. قاعدة البيانات الموسعة (12 KPI) - مزامنة Q و Weekly
data_cycle = [
    {
        "period": "3Q 2025", "week": "WEEK 01",
        "metrics": [
            ("Total Falls", 0.0, 0.18), ("Injury Falls", 0.0, 0.04), ("HAPI %", 6.67, 4.58), 
            ("Restraints", 0.45, 0.90), ("CLABSI", 1.50, 3.38), ("CAUTI", 0.0, 0.44),
            ("VAP Rate", 1.2, 2.1), ("VAE Rate", 1.6, 3.4), ("Turnover", 2.5, 3.0),
            ("RN Education", 85.01, 70.59), ("C-Difficile", 0.0, 0.12), ("MRSA Rate", 0.0, 0.05)
        ],
        # بيانات الصور
        "vents": 14, "foley": 15, "cvc": 8, "stay": 34
    },
    {
        "period": "2Q 2024", "week": "WEEK 02",
        "metrics": [
            ("Total Falls", 0.24, 0.06), ("Injury Falls", 0.24, 0.01), ("HAPI %", 14.29, 6.54), 
            ("Restraints", 0.70, 0.96), ("CLABSI", 1.28, 2.67), ("CAUTI", 0.70, 0.99),
            ("VAP Rate", 2.1, 2.1), ("VAE Rate", 2.17, 3.4), ("Turnover", 3.1, 3.0),
            ("RN Education", 82.99, 70.59), ("C-Difficile", 0.1, 0.12), ("MRSA Rate", 0.05, 0.05)
        ],
        # بيانات الصور
        "vents": 12, "foley": 14, "cvc": 9, "stay": 28
    }
]
d = data_cycle[st.session_state.step % len(data_cycle)]

# --- العنوان ---
st.markdown(f"<h1 style='text-align: center; color: white; letter-spacing: 1px;'>ICU PERFORMANCE COMMAND CENTER</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00d4ff; font-weight: bold;'>PERIOD Focus: {d['period']}</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 4. دالة الـ KPI Card الجديدة (كروت مربعة وحدود بارزة)
def draw_bold_kpi_card(label, val, target, reverse=False):
    # منطق الألوان (Traffic Lights)
    is_safe = (val <= target if not reverse else val >= target)
    color = "#00CC96" if is_safe else "#FF4B4B" # أخضر للأمان، أحمر للخطر

    # عرض الكرت بحدود بارزة
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value" style="color: {color}">{val}</div>
        <div class="target-text">Bench: {target}</div>
    </div>
    """, unsafe_allow_html=True)

# توزيع الـ 12 KPI (صفين × 6 كروت بمسافات واسعة)
row1 = st.columns(6)
for i in range(6):
    with row1[i]: draw_bold_kpi_card(*d['metrics'][i])

row2 = st.columns(6)
for i in range(6, 12):
    # إضافة استثناء لـ RN Education لأن الأعلى أفضل
    is_edu = "Education" in d['metrics'][i][0]
    with row2[i-6]: draw_bold_kpi_card(*d['metrics'][i], reverse=is_edu)

st.markdown("<hr>", unsafe_allow_html=True)

# 5. الجزء السفلي: الأجهزة (Weekly) والبار (Trends)
c_left, c_right = st.columns([1, 2.8])

with c_left:
    st.markdown(f'<div class="week-title">ATTACHED DEVICES ({d["week"]})</div>', unsafe_allow_html=True)
    def dev_card(l, v, is_stay=False):
        style = "dev-box stay-box" if is_stay else "dev-box"
        val_style = "dev-value stay-value" if is_stay else "dev-value"
        st.markdown(f'<div class="{style}"><div class="dev-label">{l}</div><div class="{val_style}">{v}</div></div>', unsafe_allow_html=True)
    
    dev_card("Ventilators", d['vents'])
    dev_card("Foley Catheter", d['foley'])
    dev_card("Central Line", d['cvc'])
    dev_card("Total Stay", d['stay'], is_stay=True)

with c_right:
    # البار تشارت الاحترافي (Trend Analysis) كما تم الاتفاق عليه
    st.markdown(f'<p style="color:#666; font-weight:bold; font-size:12px;">QUARTERLY PERFORMANCE TRENDS (Q-Sync)</p>', unsafe_allow_html=True)
    labels = ['Falls', 'HAPI', 'CLABSI', 'CAUTI', 'VAP', 'VAE']
    # ترتيب الداتا: الحالي ثم الـ Benchmark
    unit_performance = [d['metrics'][0][1], d['metrics'][2][1], d['metrics'][4][1], d['metrics'][5][1], d['metrics'][6][1], d['metrics'][7][1]]
    ndnqi_benchmark = [0.18, 4.58, 3.38, 0.44, 2.1, 3.4] # القيم المرجعية ثابتة للمقارنة
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name=f'Unit ({d["period"]})', x=labels, y=unit_performance,
        marker=dict(color='#00D4FF'), text=unit_performance, textposition='outside', textfont=dict(color='white')
    ))
    fig_bar.add_trace(go.Bar(
        name='NDNQI Benchmark', x=labels, y=ndnqi_benchmark,
        marker=dict(color='#222'), text=ndnqi_benchmark, textposition='outside', textfont=dict(color='#cccccc')
    ))
    
    fig_bar.update_layout(
        height=400, barmode='group',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=14),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, font=dict(size=14)),
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis=dict(showgrid=True, gridcolor='#222', zeroline=False),
        xaxis=dict(tickfont=dict(size=14, weight='bold'))
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# التحديث التلقائي كل 15 ثانية (Quarterly & Weekly Sync)
time.sleep(15)
st.session_state.step += 1
st.rerun()
