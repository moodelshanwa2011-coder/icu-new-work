import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Performance Hub", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS الاحترافي - نظافة بصرية تامة
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    /* المربعات العلوية بتأثير الموجة الهادئ */
    .kpi-card {
        background: #0a0a0a; border-radius: 15px; border-top: 3px solid #00d4ff;
        padding: 20px; text-align: center; height: 140px; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* مسميات رمادية وقيم نيون */
    .gray-label { color: #888888; font-size: 13px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }
    .cyan-val { color: #00d4ff; font-size: 32px; font-weight: 900; margin: 5px 0; }
    .bm-val { color: #444444; font-size: 11px; font-weight: bold; }

    /* كرت التعداد الذهبي */
    .census-box {
        background: linear-gradient(180deg, #111, #000);
        border-radius: 20px; border-bottom: 4px solid #FFD700;
        padding: 25px; text-align: center; margin-bottom: 20px;
    }

    /* تصميم نصف الدائرة الانسيابي للأجهزة */
    .semi-round-card {
        background: linear-gradient(90deg, #0a0a0a 0%, #1a1a1a 100%);
        border-radius: 0 50px 50px 0; /* انحناء دائري من اليمين */
        border-left: 5px solid #00d4ff;
        padding: 15px 25px; margin-bottom: 10px;
        display: flex; justify-content: space-between; align-items: center;
    }
    .occ-card { border-left-color: #FFD700; background: linear-gradient(90deg, #0a0a0a 0%, #1a0d00 100%); }

    .dev-label { font-size: 16px; font-weight: 700; color: #fff; }
    .dev-val { font-size: 24px; font-weight: 900; color: #00d4ff; }
    
    .side-title { color: #00d4ff; font-size: 22px; font-weight: 900; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. البيانات الكاملة (12 KPIs)
data_source = [
    {
        "period": "CYCLE A - 2026",
        "squares": [("Falls", 0.0, 0.18), ("Injuries", 0.0, 0.04), ("HAPI %", 6.67, 4.58), ("CLABSI", 1.50, 3.38), ("CAUTI", 0.0, 0.44), ("VAP", 1.2, 2.1)],
        "circles": [("Restraints", 0.45, 0.9), ("VAE Rate", 1.6, 3.4), ("Turnover", 2.5, 3.0), ("Nursing Hr", 14.5, 12.0), ("RN Edu", 85.0, 70.0), ("C-Diff", 0.0, 0.1)],
        "census": 32, "occ": "88.9%", "ett": 14, "foley": 18, "cvc": 9, "stay": 3.4
    },
    {
        "period": "CYCLE B - 2025",
        "squares": [("Falls", 0.2, 0.1), ("Injuries", 0.1, 0.0), ("HAPI %", 10.0, 6.0), ("CLABSI", 1.1, 2.5), ("CAUTI", 0.6, 0.8), ("VAP", 2.0, 2.1)],
        "circles": [("Restraints", 0.6, 0.9), ("VAE Rate", 2.0, 3.4), ("Turnover", 3.0, 3.0), ("Nursing Hr", 12.0, 12.0), ("RN Edu", 80.0, 70.0), ("C-Diff", 0.1, 0.1)],
        "census": 30, "occ": "83.3%", "ett": 11, "foley": 15, "cvc": 10, "stay": 2.8
    }
]
d = data_source[st.session_state.step % 2]

# العنوان الرئيسي
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-weight: 900; letter-spacing: 2px;'>ICU PERFORMANCE COMMAND</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #444; font-weight: bold;'>{d['period']}</p>", unsafe_allow_html=True)

# 4. الـ 6 مربعات العلوية
cols1 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['squares']):
    color = "#00ffaa" if val <= bm else "#ff4b4b"
    with cols1[i]:
        st.markdown(f"""<div class="kpi-card">
            <div class="gray-label">{lab}</div>
            <div class="cyan-val" style="color:{color}">{val}</div>
            <div class="bm-val">TARGET: {bm}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. الجزء السفلي: الأجهزة والبار
c1, c2 = st.columns([1.2, 2.5])

with c1:
    st.markdown('<div class="side-title">UNIT CAPACITY</div>', unsafe_allow_html=True)
    
    # التعداد المركزي
    st.markdown(f"""<div class="census-box">
        <div class="gray-label" style="color:#FFD700;">UNIT CENSUS</div>
        <div style="color:#FFD700; font-size:55px; font-weight:900;">{d['census']}</div>
    </div>""", unsafe_allow_html=True)
    
    # كروت الأجهزة (نصف دائرة) + Occupancy
    items = [
        ("Occupancy Rate", d['occ'], True),
        ("Pt with ETT", d['ett'], False),
        ("Pt with Foley", d['foley'], False),
        ("Pt with CVC", d['cvc'], False),
        ("Avg Stay", d['stay'], False)
    ]
    for name, val, is_occ in items:
        card_class = "semi-round-card occ-card" if is_occ else "semi-round-card"
        val_color = "#FFD700" if is_occ else "#00d4ff"
        st.markdown(f"""
            <div class="{card_class}">
                <span class="dev-label">{name}</span>
                <span class="dev-val" style="color:{val_color}">{val}</span>
            </div>
        """, unsafe_allow_html=True)

with c2:
    st.markdown('<div class="side-title" style="margin-left:20px;">PERFORMANCE ANALYTICS</div>', unsafe_allow_html=True)
    
    labels = [s[0] for s in d['squares']]
    vals = [s[1] for s in d['squares']]
    bms = [s[2] for s in d['squares']]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels, y=vals, name="Actual",
        marker=dict(color='#00d4ff'),
        text=vals, textposition='outside',
        textfont=dict(size=14, color='#fff', family="Arial Black")
    ))
    fig.add_trace(go.Bar(
        x=labels, y=bms, name="Target",
        marker=dict(color='rgba(60, 60, 60, 0.5)'),
        text=bms, textposition='outside',
        textfont=dict(size=12, color='#888')
    ))

    fig.update_layout(
        height=400, barmode='group', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=30, b=0, l=0, r=0),
        legend=dict(orientation="h", y=1.15, x=0.5, xanchor="center"),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#111')
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# 6. الـ 6 دوائر السفلية (بشكل نظيف)
st.markdown("<br>", unsafe_allow_html=True)
cols3 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['circles']):
    is_rev = any(x in lab for x in ["Hr", "Edu"])
    color = "#00ffaa" if (val >= bm if is_rev else val <= bm) else "#ff4b4b"
    with cols3[i]:
        st.markdown(f"""
        <div style="text-align:center; background:#0a0a0a; padding:15px; border-radius:15px;">
            <div style="color:{color}; font-size:24px; font-weight:900;">{val}</div>
            <div class="gray-label" style="font-size:11px;">{lab}</div>
            <div style="color:#333; font-size:10px; font-weight:bold;">BM: {bm}</div>
        </div>
        """, unsafe_allow_html=True)

time.sleep(15)
st.session_state.step += 1
st.rerun()
