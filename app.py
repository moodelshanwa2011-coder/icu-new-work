import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Executive Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المتطور جداً
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; color: #ffffff; }
    
    /* حركة الموجة النيونية */
    .wave-container {
        position: relative; background-color: #0a0a0a; border-radius: 15px;
        overflow: hidden; display: flex; flex-direction: column; justify-content: center;
        text-align: center; height: 160px; margin-bottom: 20px;
    }
    .wave-container::before {
        content: ''; position: absolute; width: 160%; height: 160%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 4s linear infinite; top: 50%; left: 50%;
    }
    .wave-container::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 4px; border-radius: 12px;
    }
    
    .wave-circle-outer {
        position: relative; width: 150px; height: 150px; border-radius: 50%;
        margin: auto; overflow: hidden; display: flex; justify-content: center; align-items: center;
    }
    .wave-circle-outer::before {
        content: ''; position: absolute; width: 160%; height: 160%;
        background: conic-gradient(#00d4ff, #001a1a, #00d4ff);
        animation: rotate-wave 5s linear infinite; top: 50%; left: 50%;
    }
    .wave-circle-outer::after {
        content: ''; position: absolute; background-color: #0a0a0a; inset: 5px; border-radius: 50%;
    }

    @keyframes rotate-wave {
        0% { transform: translate(-50%, -50%) rotate(0deg); }
        100% { transform: translate(-50%, -50%) rotate(360deg); }
    }

    .z-layer { position: relative; z-index: 10; }
    .gray-label { color: #aaaaaa; font-size: 14px; font-weight: 800; text-transform: uppercase; }
    .cyan-val { color: #00d4ff; font-size: 35px; font-weight: 900; }
    
    /* كرت التعداد الذهبي */
    .census-card {
        background: linear-gradient(145deg, #111111, #000000);
        border-bottom: 4px solid #FFD700; border-radius: 20px; padding: 25px; text-align: center;
        margin-bottom: 25px; box-shadow: 0 10px 30px rgba(255, 215, 0, 0.05);
    }
    .census-val { color: #FFD700; font-size: 65px; font-weight: 900; line-height: 1; }

    /* تصميم نصف الدائرة للأجهزة */
    .semi-circle-card {
        background: linear-gradient(90deg, #0a0a0a 0%, #151515 100%);
        border-radius: 0 50px 50px 0; /* شكل نصف دائري من اليمين */
        border-left: 5px solid #00d4ff;
        padding: 18px 25px;
        margin-bottom: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: 0.3s;
    }
    .semi-circle-card:hover { transform: translateX(10px); background: #1a1a1a; }
    .dev-text { color: #ffffff; font-size: 18px; font-weight: 700; text-transform: uppercase; }
    .dev-num { color: #00d4ff; font-size: 28px; font-weight: 900; }

    .side-title { color: #00d4ff; font-size: 28px; font-weight: 900; margin-bottom: 25px; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. البيانات المستقرة
data_source = [
    {
        "period": "CURRENT CYCLE: A-2026",
        "squares": [("Falls", 0.0, 0.18), ("Injuries", 0.0, 0.04), ("HAPI %", 6.67, 4.58), ("CLABSI Rate", 1.50, 3.38), ("CAUTI Rate", 0.0, 0.44), ("VAP Rate", 1.2, 2.1)],
        "circles": [("Restraints", 0.45, 0.90), ("VAE Rate", 1.6, 3.4), ("Turnover", 2.5, 3.0), ("Nursing Hr", 14.5, 12.0), ("RN Education", 85.0, 70.5), ("C-Diff", 0.0, 0.12)],
        "census": 32, "occupancy": "88.9%", "ett": 14, "foley": 18, "cvc": 9, "stay": 3.4
    },
    {
        "period": "PREVIOUS CYCLE: B-2025",
        "squares": [("Falls", 0.24, 0.06), ("Injuries", 0.15, 0.01), ("HAPI %", 14.2, 6.5), ("CLABSI Rate", 1.28, 2.67), ("CAUTI Rate", 0.7, 0.99), ("VAP Rate", 2.1, 2.1)],
        "circles": [("Restraints", 0.70, 0.96), ("VAE Rate", 2.17, 3.4), ("Turnover", 3.1, 3.0), ("Nursing Hr", 12.8, 12.0), ("RN Education", 82.9, 70.5), ("C-Diff", 0.1, 0.12)],
        "census": 30, "occupancy": "83.3%", "ett": 11, "foley": 15, "cvc": 10, "stay": 2.8
    }
]
d = data_source[st.session_state.step % 2]

# الهيدر
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 48px; font-weight: 900; margin-bottom:0;'>ICU STRATEGIC COMMAND</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #444; font-weight: bold; font-size: 18px;'>{d['period']}</p>", unsafe_allow_html=True)

# 4. الـ 12 KPI (نفس التوزيع الناجح)
cols1 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['squares']):
    color = "#00ffaa" if val <= bm else "#ff4b4b"
    with cols1[i]:
        st.markdown(f"""<div class="wave-container"><div class="z-layer">
            <div class="gray-label">{lab}</div>
            <div class="cyan-val" style="color:{color}">{val}</div>
            <div class="bm-val">Target: {bm}</div>
        </div></div>""", unsafe_allow_html=True)

cols2 = st.columns(6)
for i, (lab, val, bm) in enumerate(d['circles']):
    is_rev = any(x in lab for x in ["Hr", "Education"])
    color = "#00ffaa" if (val >= bm if is_rev else val <= bm) else "#ff4b4b"
    with cols2[i]:
        st.markdown(f"""<div class="wave-circle-outer"><div class="z-layer">
            <div class="cyan-val" style="font-size: 26px; color:{color}">{val}</div>
            <div class="bm-val" style="color:#888;">BM: {bm}</div>
        </div></div>
        <div class="gray-label" style="text-align:center; margin-top:10px; font-size:12px;">{lab}</div>""", unsafe_allow_html=True)

st.markdown("<br><hr style='border-color:#111;'><br>", unsafe_allow_html=True)

# 5. الجزء السفلي: الأجهزة والبار المطور
c1, c2 = st.columns([1.4, 2.4])

with c1:
    st.markdown('<div class="side-title">36 CAPACITY</div>', unsafe_allow_html=True)
    
    # كارت التعداد الفخم
    st.markdown(f"""<div class="census-card">
        <div class="gray-label" style="color:#FFD700;">Unit Census</div>
        <div class="census-val">{d['census']}</div>
        <div style="color:#FFD700; font-weight:bold;">OCCUPANCY: {d['occupancy']}</div>
    </div>""", unsafe_allow_html=True)
    
    # كروت الأجهزة بنصف الدائرة والخط الكبير
    devices = [
        ("Pt with ETT", d['ett']), 
        ("Pt with Foley", d['foley']), 
        ("Pt with CVC", d['cvc']),
        ("Avg Stay", d['stay'])
    ]
    for name, value in devices:
        st.markdown(f"""
            <div class="semi-circle-card">
                <span class="dev-text">{name}</span>
                <span class="dev-num">{value}</span>
            </div>
        """, unsafe_allow_html=True)

with c2:
    st.markdown('<div class="side-title" style="margin-left:20px;">Performance Analytics</div>', unsafe_allow_html=True)
    
    labels = [s[0] for s in d['squares']]
    vals = [s[1] for s in d['squares']]
    bms = [s[2] for s in d['squares']]

    # الرسم البياني الاحترافي المطور
    fig = go.Figure()
    
    # أعمدة الوحدة (نيون سيان مع حواف مستديرة)
    fig.add_trace(go.Bar(
        x=labels, y=vals, name="Unit Performance",
        marker=dict(color='#00d4ff', line=dict(color='#00ffff', width=1)),
        text=vals, textposition='outside',
        textfont=dict(size=14, color='#ffffff', family="Arial Black"), # خط واضح جداً للأرقام
    ))
    
    # أعمدة الـ Benchmark (تصميم زجاجي داكن)
    fig.add_trace(go.Bar(
        x=labels, y=bms, name="Benchmark",
        marker=dict(color='rgba(60, 60, 60, 0.4)', line=dict(color='#444', width=1)),
        text=bms, textposition='outside',
        textfont=dict(size=12, color='#888'),
    ))

    fig.update_layout(
        height=450, barmode='group',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=40, b=0, l=0, r=0),
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center", font=dict(size=14, color="#fff")),
        xaxis=dict(tickfont=dict(size=12, color="#aaa"), showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#151515', tickfont=dict(color="#444")),
        bargap=0.2, bargroupgap=0.1
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# التحديث التلقائي
time.sleep(15)
st.session_state.step += 1
st.rerun()
