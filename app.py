import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="ICU Matrix Command", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المتطور: تأثير الحدود النيونية المتحركة (Futuristic Matrix Green)
st.markdown("""
    <style>
    /* منع التمرير الجانبي، خلفية سوداء عميقة (True Black) */
    [data-testid="stAppViewContainer"] { background-color: #000000; padding: 5px 20px; color: #00ff00; }
    
    .section-title { color: #00ff00; font-size: 14px; font-weight: bold; text-align: left; margin-bottom: 10px; letter-spacing: 1.5px; text-transform: uppercase; }

    /* --- تنسيق الـ KPIs الجديد (مزيج نيون متحرك - Matrix style) --- */
    
    /* 1. تأثير الحدود المتحركة النيونية للمربعات (Square Cards) */
    .kpi-card-matrix {
        position: relative;
        background-color: #000000;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        text-align: center;
        height: 165px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        overflow: hidden; /* لإخفاء الزوائد */
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.1);
    }
    
    /* الطبقة المتحركة خلف الكرت (تأثير النيون الدوراني) */
    .kpi-card-matrix::before {
        content: '';
        position: absolute;
        width: 150%;
        height: 150%;
        background: conic-gradient(#00ff00, #001a00, #00ff00); /* ألوان نيون مصفوفية (Neon Green) */
        animation: rotate 4s linear infinite;
        border-radius: 12px;
    }
    
    /* الواجهة الأمامية للكرت */
    .kpi-card-matrix::after {
        content: '';
        position: absolute;
        background-color: #000000;
        inset: 4px; /* سُمك الحدود */
        border-radius: 10px;
    }
    
    /* المحتوى فوق الطبقة المتحركة */
    .kpi-content-matrix { position: relative; z-index: 10; }

    /* 2. تأثير الحدود المتحركة النيونية للدوائر (Circular Gauges) */
    .kpi-circle-matrix {
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
        background-color: #000000;
        overflow: hidden;
        box-shadow: 0 0 10px rgba(0, 255, 0, 0.1);
    }
    
    .kpi-circle-matrix::before {
        content: '';
        position: absolute;
        width: 150%;
        height: 150%;
        background: conic-gradient(#00ff00, #001a00, #00ff00); /* ألوان نيون مصفوفية ثابتة */
        animation: rotate 5s linear infinite;
        border-radius: 50%;
    }
    
    .kpi-circle-matrix::after {
        content: '';
        position: absolute;
        background-color: #000000;
        inset: 6px; /* سُمك الحدود الدائرية */
        border-radius: 50%;
    }

    /* تعريف الحركة الدورانية النيونية */
    @keyframes rotate {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    
    .kpi-circle-matrix::before, .kpi-card-matrix::before {
        top: 50%;
        left: 50%;
    }

    /* المسميات الاحترافية النيونية (Matrix Green) */
    .kpi-label {
        color: #00ff00; /* ألوان نيون مصفوفية */
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-shadow: 0 0 5px rgba(0, 255, 0, 0.5);
    }
    
    .kpi-value { font-size: 34px; font-weight: 900; margin: 5px 0; color: #00ff00; text-shadow: 0 0 10px rgba(0, 255, 0, 0.7); }
    .target-text { color: #666; font-size: 13px; font-weight: bold; margin-top: 5px; text-shadow: none; }

    /* كروت الأجهزة (يسار) النيونية الثابتة */
    .dev-box {
        background-color: #000000; border: 1px solid #00ff00; border-left: 5px solid #00ff00;
        border-radius: 8px; padding: 15px; margin-bottom: 15px; text-align: center;
        box-shadow: inset 0 0 5px rgba(0, 255, 0, 0.1);
    }
    .dev-label { color: #00ff00; font-size: 14px; font-weight: bold; opacity: 0.8; }
    .dev-value { color: #00ff00; font-size: 32px; font-weight: 900; text-shadow: 0 0 10px rgba(0, 255, 0, 0.7); }
    .stay-box { border-left: 5px solid #00ff00; background-color: #000000; }
    .stay-value { color: #00ff00; font-size: 45px; }

    hr { border: 0.1px solid #222; margin: 30px 0; }
    #stProgress { display: none; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. قاعدة البيانات الموسعة (المسميات الدولية + مزامنة Q و Weekly)
data_cycle = [
    {
        "period": "3Q 2025 (Period Alpha)", "week": "WEEK 01",
        # الصف العلوي (مربعات نيون) - SAFETY & INFECTION INCIDENCE
        "square_metrics": [
            ("FALL INCIDENCE", 0.0, 0.18), ("INJURY FALLS", 0.0, 0.04), ("HAPI RATE %", 6.67, 4.58, True),
            ("CLABSI INCIDENCE", 1.50, 3.38), ("CAUTI INCIDENCE", 0.0, 0.44), ("VAP INCIDENCE", 1.2, 2.1)
        ],
        # الصف السفلي (دوائر نيون) - EFFICIENCY & UTILIZATION
        "circle_metrics": [
            ("RESTRAINT USAGE", 0.45, 0.90), ("VAE RATE", 1.6, 3.4), ("BED TURNOVER", 2.5, 3.0),
            ("HPPD (HRS)", 14.5, 12.0, False, True), ("RN EDUCATION %", 85.01, 70.59, True, True), ("NOSOCOMIAL INFEC", 0.0, 0.12)
        ],
        "vents": 14, "foley": 15, "cvc": 8, "stay": 34
    },
    {
        "period": "2Q 2024 (Period Beta)", "week": "WEEK 02",
        "square_metrics": [
            ("FALL INCIDENCE", 0.24, 0.06), ("INJURY FALLS", 0.24, 0.01), ("HAPI RATE %", 14.29, 6.54, True),
            ("CLABSI INCIDENCE", 1.28, 2.67), ("CAUTI INCIDENCE", 0.70, 0.99), ("VAP INCIDENCE", 2.1, 2.1)
        ],
        "circle_metrics": [
            ("RESTRAINT USAGE", 0.70, 0.96), ("VAE RATE", 2.17, 3.4), ("BED TURNOVER", 3.1, 3.0),
            ("HPPD (HRS)", 12.8, 12.0, False, True), ("RN EDUCATION %", 82.99, 70.59, True, True), ("NOSOCOMIAL INFEC", 0.1, 0.12)
        ],
        "vents": 12, "foley": 14, "cvc": 9, "stay": 28
    }
]
d = data_cycle[st.session_state.step % len(data_cycle)]

# الهيدر الأساسي
st.markdown(f"<h1 style='text-align: center; color: #00ff00; letter-spacing: 2px; text-shadow: 0 0 10px rgba(0, 255, 0, 0.7);'>ICU MATRIX COMMAND HUB</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00ff00; font-weight: bold; opacity: 0.8;'>PERIOD Focus: {d['period']}</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 4. دالة الكروت المربعة النيونية المتحركة (العلوي)
def draw_animated_matrix_kpi(label, val, target):
    # اللون بناءً على الأداء (كلها أخضر للأمان في تصميم الـ Matrix، وسنضيف تلميحاً بصرياً فقط للأداء السلبي)
    color = "#00ff00"
    
    # استثناء لبعض المؤشرات (الأعلى أفضل)
    if "Education" in label or "HPPD" in label:
        pass # كلها أخضر في الـ Matrix

    # عرض الكرت المربع بحدود نيون مصفوفية متحركة
    st.markdown(f"""
    <div class="kpi-card-matrix">
        <div class="kpi-content-matrix">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value" style="color: {color}">{val}</div>
            <div class="target-text">Benchmark: {target}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 5. دالة المؤشرات الدائرية النيونية المتحركة (السفلي)
def draw_animated_matrix_circle_kpi(label, val, target, is_perc=False, reverse=False):
    is_safe = (val <= target if not reverse else val >= target)
    color = "#00ff00" # أخضر للأمان مصفوفياً
    
    # عرض الكرت الدائري بحدود نيون مصفوفية متحركة (والمحتوى بالداخل)
    st.markdown(f"""
    <div class="kpi-circle-matrix">
        <div class="kpi-content-matrix">
            <div class="kpi-value" style="color: {color}; font-size:30px; margin-top:15px;">{val}{"%" if is_perc else ""}</div>
            <div class="target-text" style="color:white; font-size:11px;">Target: {target}</div>
        </div>
    </div>
    <div class="kpi-label" style="text-align:center; height:30px; font-weight:800; color:#00ff00;">{label}</div>
    """, unsafe_allow_html=True)

# توزيع الـ 12 KPI (صف مربعات مصفوفية + صف دوائر مصفوفية)
st.markdown('<p class="section-title">INCIDENCE DATA (Matrix Squares)</p>', unsafe_allow_html=True)
row1 = st.columns(6)
for i in range(6):
    with row1[i]: draw_animated_matrix_kpi(*d['square_metrics'][i])

st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<p class="section-title">WORKFORCE & EFFICIENCY DATA (Matrix Circles)</p>', unsafe_allow_html=True)
row2 = st.columns(6)
for i in range(6):
    with row2[i]: draw_animated_matrix_circle_kpi(d['circle_metrics'][i][0], d['circle_metrics'][i][1], d['circle_metrics'][i][2], 
                                               is_perc=("EDUCATION" in d['circle_metrics'][i][0]),
                                               reverse=("HPPD" in d['circle_metrics'][i][0] or "EDUCATION" in d['circle_metrics'][i][0]))

st.markdown("<hr>", unsafe_allow_html=True)

# 6. الجزء السفلي: الأجهزة (Weekly) والبار تشارت النيوني (Trends)
c_left, c_right = st.columns([1, 2.5])

with c_left:
    st.markdown(f'<div class="section-title">ATTACHED DEVICES ({d["week"]})</div>', unsafe_allow_html=True)
    def dev_card(l, v, is_stay=False):
        cls = "dev-box stay-box" if is_stay else "dev-box"
        val_cls = "dev-value stay-value" if is_stay else "dev-value"
        st.markdown(f'<div class="{cls}"><div class="dev-label">{l}</div><div class="{val_cls}">{v}</div></div>', unsafe_allow_html=True)
    
    dev_card("Ventilators", d['vents'])
    dev_card("Foley Catheter", d['foley'])
    dev_card("Central Line", d['cvc'])
    dev_card("Total Stay", d['stay'], is_stay=True)

with c_right:
    # البار تشارت الاحترافي (Trend Analysis) بألوان نيون مصفوفية
    st.markdown(f'<p style="color:#666; font-weight:bold; font-size:12px; margin-left: 20px;">QUARTERLY PERFORMANCE TRENDS (Q-Sync)</p>', unsafe_allow_html=True)
    labels = ['FALLS', 'HAPI', 'CLABSI', 'CAUTI', 'VAP', 'VAE']
    unit_performance = [d['square_metrics'][0][1], d['square_metrics'][2][1], d['square_metrics'][3][1], d['square_metrics'][4][1], d['square_metrics'][5][1], d['circle_metrics'][1][1]]
    ndnqi_benchmark = [0.18, 4.58, 3.38, 0.44, 2.1, 3.4] # القيم المرجعية ثابتة للمقارنة
    
    fig_bar = go.Figure()
    # بار المستشفى باللون الأخضر النيوني (Matrix Green)
    fig_bar.add_trace(go.Bar(
        name=f'Unit Performance', x=labels, y=unit_performance,
        marker=dict(color='#00ff00'), text=unit_performance, textposition='outside', textfont=dict(color='#00ff00', weight='bold')
    ))
    # بار الـ Benchmark باللون الأخضر الداكن النيوني (Neon Green)
    fig_bar.add_trace(go.Bar(
        name='NDNQI Benchmark', x=labels, y=ndnqi_benchmark,
        marker=dict(color='#001a00', line=dict(color='#00ff00', width=1)),
        text=ndnqi_benchmark, textposition='outside', textfont=dict(color='#aaaaaa')
    ))
    
    fig_bar.update_layout(
        height=400, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#00ff00', size=14, weight='bold'),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, font=dict(size=14, color='#00ff00')),
        xaxis=dict(tickfont=dict(size=14, weight='bold', color='#00ff00')),
        yaxis=dict(showgrid=True, gridcolor='#001a00', zeroline=False)
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# التحديث التلقائي كل 15 ثانية (Quarterly & Weekly Sync)
time.sleep(15)
st.session_state.step += 1
st.rerun()
