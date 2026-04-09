import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة الاحترافية
st.set_page_config(page_title="ICU Dynamic Hub", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المتطور: تأثير "الموجة النيونية" الدوارة وألوان الأسماء الاحترافية
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    /* منع التداخل */
    [data-testid="stHorizontalBlock"] { gap: 1rem; }

    /* --- تنسيق الـ KPIs الجديد (تأثير الموجة) --- */
    
    /* 1. المربعات الموجية (Wave Squares) */
    .kpi-wave-box {
        position: relative;
        background-color: #0a0a0a;
        border-radius: 12px;
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        text-align: center;
        overflow: hidden; /* لإخفاء الزوائد */
        margin-bottom: 20px;
        transition: transform 0.3s;
    }
    .kpi-wave-box:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0, 212, 255, 0.2); }
    
    /* الطبقة المتحركة خلف الكرت (تأثير الموجة الدورانية) */
    .kpi-wave-box::before {
        content: '';
        position: absolute;
        width: 150%;
        height: 150%;
        /* ألوان احترافية: سيان كهربائي وأزرق عميق */
        background: conic-gradient(#00d4ff, #001122, #00d4ff);
        animation: rotate-wave 4s linear infinite;
        border-radius: 12px;
    }
    
    /* الواجهة الأمامية للكرت */
    .kpi-wave-box::after {
        content: '';
        position: absolute;
        background-color: #0a0a0a;
        inset: 4px; /* سُمك الحدود */
        border-radius: 10px;
    }
    
    /* 2. الدوائر الموجية (Wave Circles) */
    .kpi-wave-circle-outer {
        position: relative;
        width: 140px;
        height: 140px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: auto;
        background-color: #0a0a0a;
        overflow: hidden;
    }
    
    .kpi-wave-circle-outer::before {
        content: '';
        position: absolute;
        width: 150%;
        height: 150%;
        background: conic-gradient(#00d4ff, #001122, #00d4ff);
        animation: rotate-wave 5s linear infinite;
        border-radius: 50%;
    }
    
    .kpi-wave-circle-outer::after {
        content: '';
        position: absolute;
        background-color: #0a0a0a;
        inset: 5px; /* سُمك الحدود */
        border-radius: 50%;
    }

    /* تعريف الحركة الدورانية للموجة */
    @keyframes rotate-wave {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }
    
    .kpi-wave-circle-outer::before, .kpi-wave-box::before {
        top: 50%;
        left: 50%;
    }

    /* المحتوى فوق الطبقة المتحركة */
    .kpi-content-layer { position: relative; z-index: 10; padding: 5px; }

    /* --- لون الأسماء (مش أبيض) رمادي معدني ناعم --- */
    .kpi-label-text {
        color: #aaaaaa; /* رمادي معدني ناعم واحترافي */
        font-size: 14px;
        font-weight: 800;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        height: 35px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .kpi-value-text { color: #00d4ff; font-size: 32px; font-weight: 900; }
    .kpi-bench-text { color: #555; font-size: 11px; font-weight: bold; margin-top: 5px; }

    /* كروت الأجهزة (يسار) */
    .dev-card-dynamic {
        background-color: #0a0a0a; border: 1px solid #111; border-left: 4px solid #00d4ff;
        border-radius: 8px; padding: 12px; margin-bottom: 12px; text-align: center;
    }
    /* لون اسم الجهاز رمادي */
    .dev-label-dynamic { color: #aaaaaa; font-size: 13px; font-weight: bold; }
    .dev-value-dynamic { color: #ffffff; font-size: 28px; font-weight: 900; }
    .stay-box-dynamic { border-left: 4px solid #00CC96; background-color: #0d0d0d; box-shadow: 0 0 10px rgba(0, 212, 255, 0.1); }
    .stay-value-dynamic { color: #00CC96; font-size: 38px; }

    hr { border: 0.1px solid #111; margin: 30px 0; }
    #stProgress { display: none; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. قاعدة البيانات بالمسميات القديمة
data_source = [
    {
        "period": "3Q 2025", "week": "WEEK 01",
        "squares": [
            ("Total Falls", 0.0, 0.18), ("Injury Falls", 0.0, 0.04), ("HAPI %", 6.67, 4.58),
            ("CLABSI Rate", 1.50, 3.38), ("CAUTI Rate", 0.0, 0.44), ("VAP Rate", 1.2, 2.1)
        ],
        "circles": [
            ("Restraints", 0.45, 0.90), ("VAE Rate", 1.6, 3.4), ("Turnover", 2.5, 3.0),
            ("HPPD (HRS)", 14.5, 12.0), ("RN Education", 85.01, 70.59), ("C-Diff / MRSA", 0.0, 0.12)
        ],
        "devs": [("Ventilators", 14), ("Foley Catheter", 15), ("Central Line", 8)],
        "occupancy": [("Unit Occupancy", 94), ("Average Stay", 34), ("Wait Time", 1.5)],
        "total_pt": 48
    },
    {
        "period": "2Q 2024", "week": "WEEK 02",
        "squares": [
            ("Total Falls", 0.24, 0.06), ("Injury Falls", 0.24, 0.01), ("HAPI %", 14.29, 6.54),
            ("CLABSI Rate", 1.28, 2.67), ("CAUTI Rate", 0.70, 0.99), ("VAP Rate", 2.1, 2.1)
        ],
        "circles": [
            ("Restraints", 0.70, 0.96), ("VAE Rate", 2.17, 3.4), ("Turnover", 3.1, 3.0),
            ("HPPD (HRS)", 12.8, 12.0), ("RN Education", 82.99, 70.59), ("C-Diff / MRSA", 0.1, 0.12)
        ],
        "devs": [("Ventilators", 12), ("Foley Catheter", 14), ("Central Line", 9)],
        "occupancy": [("Unit Occupancy", 88), ("Average Stay", 28), ("Wait Time", 2.1)],
        "total_pt": 42
    }
]

d = data_source[st.session_state.step % 2]

# الهيدر الأساسي
st.markdown(f"<h1 style='text-align: center; color: white; letter-spacing: 2px;'>ICU DYNAMIC HUB</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00d4ff; font-weight: bold;'>PERIOD Focus: {d['period']}</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# 4. المربعات الموجية النيونية (الصف العلوي)
cols_sq = st.columns(6)
for i, (lab, val, bench) in enumerate(d['squares']):
    color = "#00CC96" if val <= bench else "#FF4B4B"
    with cols_sq[i]:
        st.markdown(f"""
        <div class="kpi-wave-box"><div class="kpi-content-layer">
            <div class="kpi-label-text">{lab}</div>
            <div class="kpi-value-text" style="color: {color}">{val}</div>
            <div class="kpi-bench-text">Benchmark: {bench}</div>
        </div></div>""", unsafe_allow_html=True)

# 5. الدوائر الموجية النيونية (الصف السفلي)
cols_ci = st.columns(6)
for i, (lab, val, bench) in enumerate(d['circles']):
    is_rev = any(x in lab for x in ["Hours", "Education"])
    color = "#00CC96" if (val >= bench if is_rev else val <= bench) else "#FF4B4B"
    with cols_ci[i]:
        st.markdown(f"""
        <div class="kpi-wave-circle-outer"><div class="kpi-content-layer">
            <div class="kpi-value-text" style="color: {color}; font-size: 24px; margin-top:10px;">{val}</div>
            <div class="kpi-bench-text" style="color: #fff">Target: {bench}</div>
        </div></div>
        <div class="kpi-label-text" style="text-align:center; height:30px; margin-top:5px; text-shadow:none;">{lab}</div>
        """, unsafe_allow_html=True)

st.markdown("<hr style='border-color: #1a1a1a;'>", unsafe_allow_html=True)

# 6. الجزء السفلي: الأجهزة والبار
c_left, c_right = st.columns([1, 2.8])

with c_left:
    st.markdown(f'<p style="color:#666; font-weight:bold; font-size:12px; margin-bottom: 5px;">UNIT OCCUPANCY <span style="color:#00d4ff; font-size:36px; font-weight:bold;">//</span></p>', unsafe_allow_html=True)
    def dev_card(l, v):
        st.markdown(f"""
            <div class="dev-card-dynamic">
                <span class="dev-value-dynamic">{v}</span>
                <span class="dev-label-dynamic">{l}</span>
            </div>
        """, unsafe_allow_html=True)
    
    # تمييز Total Patient
    st.markdown(f"""
        <div class="dev-card-dynamic" style="border-left: 5px solid #FFD700; background-color: #0d0d0d; box-shadow: 0 0 10px rgba(255, 215, 0, 0.2);">
            <span class="dev-value-dynamic" style="color: #FFD700; font-size: 55px;">{d['total_pt']}</span>
            <span class="dev-label-dynamic" style="color: #FFD700;">TOTAL PATIENTS</span>
        </div>
    """, unsafe_allow_html=True)
    
    dev_card(d['occupancy'][0][0], f"{d['occupancy'][0][1]}%")
    dev_card(d['occupancy'][1][0], d['occupancy'][1][1])
    dev_card(d['occupancy'][2][0], d['occupancy'][2][1])
    
    dev_card("Ventilators", d['vents'])
    dev_card("Foley Catheter", d['foley'])
    dev_card("Central Line", d['cvc'])

with c_right:
    # الرسم البياني ثلاثي الأبعاد والشرطة المائلة
    st.markdown(f'<p style="color:#666; font-weight:bold; font-size:12px; margin-left: 20px; margin-bottom: 5px;">QUARTERLY PERFORMANCE TRENDS (Q-Sync) <span style="color:#00d4ff; font-size:36px; font-weight:bold;">//</span></p>', unsafe_allow_html=True)
    labels = [s[0] for s in d['squares']]
    vals = [s[1] for s in d['squares']]
    benches = [s[2] for s in d['squares']]
    
    # إنشاء رسم بياني شلالي تفاعلي (Animated Waterfall Chart) ثلاثي الأبعاد
    fig = go.Figure()
    fig.add_trace(go.Waterfall(
        name='Current Unit', x=labels, y=vals,
        marker=dict(color='#00d4ff', line=dict(color='#00CC96', width=2)),
        connector=dict(line=dict(color='#001122', width=1, dash='dash')),
        text=vals, textposition='outside'
    ))
    fig.add_trace(go.Waterfall(
        name='NDNQI Benchmark', x=labels, y=benches,
        marker=dict(color='rgba(255, 255, 255, 0.05)', line=dict(color='#222', width=2)),
        connector=dict(line=dict(color='#0d0d0d', width=1, dash='dash')),
        text=benches, textposition='outside'
    ))
    
    # إضافة تأثير ثلاثي الأبعاد ناعم
    fig.update_layout(
        height=450, showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#aaaaaa', size=14),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, font=dict(size=14)),
        margin=dict(l=0, r=0, t=20, b=0),
        scene=dict(aspectratio=dict(x=1, y=1.5, z=0.5)) # تأثير ثلاثي الأبعاد ناعم
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# التحديث التلقائي كل 15 ثانية صامتاً
time.sleep(15)
st.session_state.step += 1
st.rerun()
