import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="ICU Strategic Hub", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المتطور: تأثير الحدود النيونية المتحركة (Futuristic Borders)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; padding: 10px 20px; }
    
    .section-title { color: #888; font-size: 14px; font-weight: bold; text-align: left; margin-bottom: 10px; letter-spacing: 1.5px; text-transform: uppercase; }

    /* --- تنسيق الـ KPIs الجديد (مزيج نيون متحرك) --- */
    
    /* 1. تأثير الحدود المتحركة للمربعات (Square Cards) */
    .kpi-card-animated {
        position: relative;
        background-color: #0d0d0d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        text-align: center;
        height: 165px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        overflow: hidden; /* لإخفاء الزوائد */
    }
    
    /* الطبقة المتحركة خلف الكرت (تأثير التحميل) */
    .kpi-card-animated::before {
        content: '';
        position: absolute;
        width: 150%;
        height: 150%;
        background: conic-gradient(#00d4ff, #00CC96, #00d4ff); /* ألوان نيون احترافية */
        animation: rotate 3s linear infinite;
        border-radius: 12px;
    }
    
    /* الواجهة الأمامية للكرت */
    .kpi-card-animated::after {
        content: '';
        position: absolute;
        background-color: #0d0d0d;
        inset: 4px; /* سُمك الحدود */
        border-radius: 10px;
    }
    
    /* المحتوى فوق الطبقة المتحركة */
    .kpi-content { position: relative; z-index: 10; }

    /* 2. تأثير الحدود المتحركة للدوائر (Circular Gauges) */
    .kpi-circle-animated {
        position: relative;
        width: 160px;
        height: 160px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: auto;
        margin-bottom: 15px;
        background-color: #0d0d0d;
        overflow: hidden;
    }
    
    .kpi-circle-animated::before {
        content: '';
        position: absolute;
        width: 150%;
        height: 150%;
        background: conic-gradient(#00d4ff, #FF007F, #00d4ff); /* ألوان نيون مختلفة للدوائر */
        animation: rotate 4s linear infinite;
        border-radius: 50%;
    }
    
    .kpi-circle-animated::after {
        content: '';
        position: absolute;
        background-color: #0d0d0d;
        inset: 6px; /* سُمك الحدود الدائرية */
        border-radius: 50%;
    }

    /* تعريف الحركة الدورانية */
    @keyframes rotate {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    
    .kpi-circle-animated::before, .kpi-card-animated::before {
        top: 50%;
        left: 50%;
    }

    /* المسميات الاحترافية الملونة (Cyan & Gold) */
    .kpi-label {
        color: #aaaaaa;
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .kpi-value { font-size: 34px; font-weight: 900; margin: 5px 0; text-shadow: 0 0 10px rgba(255,255,255,0.3); }
    .target-text { color: #555; font-size: 13px; font-weight: bold; margin-top: 5px; }

    /* كروت الأجهزة (يسار) */
    .dev-box {
        background-color: #0a0a0a; border: 1px solid #111; border-left: 4px solid #1f77b4;
        border-radius: 8px; padding: 15px; margin-bottom: 15px; text-align: center;
    }
    .dev-label { color: #aaaaaa; font-size: 14px; font-weight: bold; }
    .dev-value { color: #ffffff; font-size: 32px; font-weight: 900; }
    .stay-box { border-left: 4px solid #00CC96; background-color: #0d0d0d; }
    .stay-value { color: #00CC96; font-size: 45px; }

    hr { border: 0.1px solid #111; margin: 30px 0; }
    #stProgress { display: none; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. قاعدة البيانات الموسعة (المسميات الدولية + مزامنة Q و Weekly)
data_cycle = [
    {
        "period": "3Q 2025 (Period Alpha)", "week": "WEEK 01",
        # الصف العلوي (مربعات) - SAFETY & INFECTION INCIDENCE
        "square_metrics": [
            ("FALL INCIDENCE", 0.0, 0.18), ("INJURY FALLS", 0.0, 0.04), ("HAPI RATE %", 6.67, 4.58),
            ("CLABSI RATE", 1.50, 3.38), ("CAUTI RATE", 0.0, 0.44), ("VAP INCIDENCE", 1.2, 2.1)
        ],
        # الصف السفلي (دوائر) - EFFICIENCY & UTILIZATION
        "circle_metrics": [
            ("RESTRAINT USAGE", 0.45, 0.90), ("VAE RATE", 1.6, 3.4), ("BED TURNOVER", 2.5, 3.0),
            ("HPPD (HRS)", 14.5, 12.0, True), ("RN EDUCATION %", 85.01, 70.59, True), ("C-DIFFICLE RATE", 0.0, 0.12)
        ],
        "vents": 14, "foley": 15, "cvc": 8, "stay": 34
    },
    {
        "period": "2Q 2024 (Period Beta)", "week": "WEEK 02",
        "square_metrics": [
            ("FALL INCIDENCE", 0.24, 0.06), ("INJURY FALLS", 0.24, 0.01), ("HAPI RATE %", 14.29, 6.54),
            ("CLABSI RATE", 1.28, 2.67), ("CAUTI RATE", 0.70, 0.99), ("VAP INCIDENCE", 2.1, 2.1)
        ],
        "circle_metrics": [
            ("RESTRAINT USAGE", 0.70, 0.96), ("VAE RATE", 2.17, 3.4), ("BED TURNOVER", 3.1, 3.0),
            ("HPPD (HRS)", 12.8, 12.0, True), ("RN EDUCATION %", 82.99, 70.59, True), ("C-Difficle RATE", 0.1, 0.12)
        ],
        "vents": 12, "foley": 14, "cvc": 9, "stay": 28
    }
]
d = data_cycle[st.session_state.step % len(data_cycle)]

# الهيدر الأساسي
st.markdown(f"<h1 style='text-align: center; color: white;'>ICU STRATEGIC COMMAND HUB</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00d4ff; font-weight: bold;'>PERIOD Focus: {d['period']}</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 4. دالة الكروت المربعة النيونية المتحركة (الصف العلوي)
def draw_animated_square_kpi(label, val, target):
    # منطق الألوان (Traffic Lights) - أخضر للأمان، أحمر للخطر
    color = "#00CC96" if val <= target else "#FF4B4B"
    
    # استثناء لبعض المؤشرات (الأعلى أفضل)
    if "Education" in label or "HPPD" in label:
        color = "#00CC96" if val >= target else "#FF4B4B"

    # عرض الكرت المربع بحدود نيون متحركة
    st.markdown(f"""
    <div class="kpi-card-animated">
        <div class="kpi-content">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="color: {color}">{val}</div>
            <div class="target-text">Benchmark: {target}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 5. دالة المؤشرات الدائرية النيونية المتحركة (الصف السفلي)
def draw_animated_circle_kpi(label, val, target, is_perc=False, reverse=False):
    is_safe = (val <= target if not reverse else val >= target)
    color = "#00CC96" if is_safe else "#FF4B4B"
    
    # عرض الكرت الدائري بحدود نيون متحركة (والمحتوى بالداخل)
    st.markdown(f"""
    <div class="kpi-circle-animated">
        <div class="kpi-content">
            <div class="kpi-value" style="color: {color}; font-size:30px; margin-top:15px;">{val}{"%" if is_perc else ""}</div>
            <div class="target-text" style="color:white; font-size:11px;">Target: {target}</div>
        </div>
    </div>
    <div class="kpi-label" style="text-align:center; height:30px;">{label}</div>
    """, unsafe_allow_html=True)

# توزيع الـ 12 KPI (صف مربعات نيون متحركة + صف دوائر نيون متحركة)
st.markdown('<p class="section-title">SAFETY & INFECTION INCIDENCE (Neon Squares)</p>', unsafe_allow_html=True)
row1 = st.columns(6)
for i in range(6):
    with row1[i]: draw_animated_square_kpi(*d['square_metrics'][i])

st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<p class="section-title">EFFICIENCY & WORKFORCE INDICATORS (Neon Circles)</p>', unsafe_allow_html=True)
row2 = st.columns(6)
for i in range(6):
    # استخراج البيانات من tuple الـ metrics
    with row2[i]: draw_animated_circle_kpi(d['circle_metrics'][i][0], d['circle_metrics'][i][1], d['circle_metrics'][i][2], 
                                           is_perc=("EDUCATION" in d['circle_metrics'][i][0]),
                                           reverse=("HPPD" in d['circle_metrics'][i][0] or "EDUCATION" in d['circle_metrics'][i][0]))

st.markdown("<hr>", unsafe_allow_html=True)

# 6. الجزء السفلي: الأجهزة (Weekly) والبار تشارت الملون (Trends)
c_left, c_right = st.columns([1, 2.5])

with c_left:
    st.markdown(f'<div class="section-title">ATTACHED DEVICES ({d["week"]})</div>', unsafe_allow_html=True)
    def dev_card(l, v, is_stay=False):
        style = "dev-box stay-box" if is_stay else "dev-box"
        val_style = "dev-value stay-value" if is_stay else "dev-value"
        st.markdown(f'<div class="{style}"><div class="dev-label">{l}</div><div class="{val_style}">{v}</div></div>', unsafe_allow_html=True)
    
    dev_card("Ventilators", d['vents'])
    dev_card("Foley Catheter", d['foley'])
    dev_card("Central Line", d['cvc'])
    dev_card("Total Stay", d['stay'], is_stay=True)

with c_right:
    # البار تشارت الاحترافي (Trend Analysis) بألوان نيون
    st.markdown(f'<p style="color:#666; font-weight:bold; font-size:12px;">QUARTERLY PERFORMANCE TRENDS (Q-Sync)</p>', unsafe_allow_html=True)
    labels = ['FALLS', 'HAPI', 'CLABSI', 'CAUTI', 'VAP', 'VAE']
    unit_performance = [d['square_metrics'][0][1], d['square_metrics'][2][1], d['square_metrics'][3][1], d['square_metrics'][4][1], d['square_metrics'][5][1], d['circle_metrics'][1][1]]
    ndnqi_benchmark = [0.18, 4.58, 3.38, 0.44, 2.1, 3.4] # القيم المرجعية ثابتة
    
    fig_bar = go.Figure()
    # بار المستشفى باللون الوردي النيوني (تغيير للتميز)
    fig_bar.add_trace(go.Bar(
        name=f'Unit Performance', x=labels, y=unit_performance,
        marker=dict(color='#FF007F'), text=unit_performance, textposition='outside', textfont=dict(color='white')
    ))
    # بار الـ Benchmark باللون الأزرق النيوني
    fig_bar.add_trace(go.Bar(
        name='NDNQI Benchmark', x=labels, y=ndnqi_benchmark,
        marker=dict(color='#00D4FF'), text=ndnqi_benchmark, textposition='outside', textfont=dict(color='#cccccc')
    ))
    
    fig_bar.update_layout(
        height=400, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=14),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, font=dict(size=14)),
        xaxis=dict(tickfont=dict(size=14, weight='bold'))
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# التحديث التلقائي كل 15 ثانية (Quarterly & Weekly Sync)
time.sleep(15)
st.session_state.step += 1
st.rerun()
