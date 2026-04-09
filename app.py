import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المعتمد - ثابت ومستقر
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
    .census-num-mini { color: #FFD700; font-size: 40px; font-weight: 900; margin: 5px 0; }
    .gauge-label-bottom { color: #ffffff; font-size: 14px; font-weight: 900; text-transform: uppercase; margin-top: -20px; text-align: center; }
    .side-header { color: #00d4ff; font-size: 26px; font-weight: 900; margin-bottom: 15px; text-transform: uppercase; }
    </style>
    """, unsafe_allow_html=True)

# 3. داتا الأسابيع (مستخرجة من صورك)
if 'week_index' not in st.session_state: st.session_state.week_index = 0

all_weeks = [
    {"label": "First Week of March", "census": 23, "dev": [12, 16, 4, 3.5], "sq_vals": [0.0, 0.0, 6.67, 1.5, 0.0, 1.2], "cir_vals": [0.45, 1.6, 2.5, 14.5, 85.0, 0.0]},
    {"label": "Second Week of March", "census": 24, "dev": [10, 16, 3, 3.8], "sq_vals": [0.1, 0.0, 7.20, 1.2, 0.2, 1.0], "cir_vals": [0.50, 1.8, 2.8, 12.0, 80.0, 0.1]},
    {"label": "Third Week of March", "census": 28, "dev": [10, 13, 8, 4.0], "sq_vals": [0.0, 0.0, 5.50, 0.8, 0.0, 1.5], "cir_vals": [0.40, 1.5, 2.2, 15.0, 88.0, 0.0]},
    {"label": "Fourth Week of March", "census": 25, "dev": [13, 16, 7, 4.2], "sq_vals": [0.2, 0.1, 8.10, 2.0, 0.5, 2.1], "cir_vals": [0.60, 2.0, 3.2, 11.5, 75.0, 0.2]},
    {"label": "First Week of April", "census": 30, "dev": [11, 15, 6, 4.5], "sq_vals": [0.0, 0.0, 6.80, 1.4, 0.1, 1.3], "cir_vals": [0.48, 1.7, 2.6, 14.0, 84.0, 0.0]}
]

cur = all_weeks[st.session_state.week_index % len(all_weeks)]
sq_info = [("Falls", 0.18), ("Injuries", 0.04), ("HAPI %", 4.58), ("CLABSI", 3.3), ("CAUTI", 0.4), ("VAP", 2.1)]
cir_info = [("Restraints", 0.9), ("VAE Rate", 3.4), ("Turnover", 3.0), ("Nurse Hr", 12.0), ("RN Edu", 70.5), ("C-Diff", 0.1)]

# دالة رسم العدادات
def create_gauge(v, mx, s):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = v,
        number = {'font': {'size': 38, 'color': '#fff', 'family': 'Arial Black'}},
        gauge = {'axis': {'range': [None, mx], 'tickvals': []}, 'bar': {'color': "#222"}, 'bgcolor': "#000", 'borderwidth': 0,
                 'steps': [{'range': [0, s[0]], 'color': "#00ffaa"}, {'range': [s[0], s[1]], 'color': "#FFD700"}, {'range': [s[1], mx], 'color': "#ff4b4b"}]}
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=0, l=10, r=10), height=130)
    return fig

# --- واجهة المستخدم ---
st.markdown(f"<h1 style='text-align: center; color: #00d4ff; font-size: 50px; font-weight:900;'>ICU DASHBOARD</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #444; font-weight: bold; font-size: 20px; margin-bottom: 30px;'>PERIOD: 1Q 2026</p>", unsafe_allow_html=True)

# 4. المربعات العلوية
cols1 = st.columns(6)
for i, (name, bm) in enumerate(sq_info):
    v = cur['sq_vals'][i]
    color = "#00ffaa" if v <= bm else "#ff4b4b"
    with cols1[i]:
        st.markdown(f"""<div class="kpi-card"><div class="z-layer"><div class="gray-label">{name}</div><div class="cyan-val" style="color:{color}">{v}</div><div class="bm-full-text">BM: {bm}</div></div></div>""", unsafe_allow_html=True)

# 5. الدوائر
st.markdown("<div style='margin-top:40px;'></div>", unsafe_allow_html=True)
cols2 = st.columns(6)
for i, (name, bm) in enumerate(cir_info):
    v = cur['cir_vals'][i]
    is_rev = any(x in name for x in ["Hr", "Edu"])
    color = "#00ffaa" if (v >= bm if is_rev else v <= bm) else "#ff4b4b"
    with cols2[i]:
        st.markdown(f"""<div style="text-align:center;"><div class="circle-container"><div class="z-layer"><div class="cyan-val" style="font-size: 45px; color:{color}">{v}</div></div></div><div class="gray-label" style="margin-top:20px; font-size:24px;">{name}</div><div class="bm-full-text">BM: {bm}</div></div>""", unsafe_allow_html=True)

st.markdown("<hr style='border-color:#111; margin:60px 0;'>", unsafe_allow_html=True)

# 6. الجزء السفلي (الأجهزة + السلم الموسيقي المطور)
c1, c2 = st.columns([2.2, 1.8])
with c1:
    st.markdown(f"""<div class="census-box-mini"><div style="color:#FFD700; font-size:12px; font-weight:bold;">CURRENT CENSUS</div><div class="census-num-mini">{cur['census']}</div></div>""", unsafe_allow_html=True)
    st.markdown(f'<div class="side-header">ATTACHED DEVICES <span style="color:#FFD700; font-size:18px;">({cur["label"]})</span></div>', unsafe_allow_html=True)
    g_cols = st.columns(4)
    dev_meta = [("ETT", 36, [10, 18]), ("Foley", 36, [24, 30]), ("CVC", 36, [16, 22]), ("Stay", 10, [4, 6])]
    for i, (n, m, s) in enumerate(dev_meta):
        with g_cols[i]:
            st.plotly_chart(create_gauge(cur['dev'][i], m, s), use_container_width=True, config={'displayModeBar': False})
            st.markdown(f'<div class="gauge-label-bottom">{n}</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="side-header" style="margin-left:20px;">PERFORMANCE Staff Chart</div>', unsafe_allow_html=True)
    
    x_names = [n[0] for n in sq_info]
    y_raw = cur['sq_vals']
    y_bms = [n[1] for n in sq_info]
    
    # حساب أقصى قيمة للمحور لضمان عدم الاختفاء
    max_val = max(y_raw + y_bms + [1.0]) * 1.3
    
    fig = go.Figure()

    # خطوط السلم الموسيقي الـ 5
    for i in range(1, 6):
        level = (max_val / 6) * i
        fig.add_shape(type="line", x0=-0.5, x1=5.5, y0=level, y1=level, line=dict(color="#1a1a1a", width=1))

    # إضافة رمز الموسيقى كخلفية
    fig.add_annotation(x=-0.4, y=(max_val/2), text="𝄞", showarrow=False, font=dict(size=60, color="#111"))

    # الأعمدة (بقيم افتراضية بسيطة للأصفار لضمان الرسم)
    y_display = [max(v, 0.01) for v in y_raw]
    
    fig.add_trace(go.Bar(
        x=x_names, y=y_display, 
        marker_color='#00d4ff', width=0.03, 
        showlegend=False, hoverinfo='skip'
    ))

    # النوتات (الأرقام الفعلية)
    node_colors = ['#00d4ff' if y <= b else '#ff4b4b' for y, b in zip(y_raw, y_bms)]
    fig.add_trace(go.Scatter(
        x=x_names, y=y_display, 
        mode='markers+text',
        marker=dict(size=30, color=node_colors, symbol='circle', line=dict(color='#000', width=2)),
        text=y_raw,
        textfont=dict(color='#000', size=10, family='Arial Black'),
        textposition='midcenter',
        showlegend=False
    ))

    fig.update_layout(
        height=450,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=10, b=20, l=0, r=0),
        xaxis=dict(tickfont=dict(color='#888', size=10), showgrid=False, range=[-0.7, 5.7]),
        yaxis=dict(showgrid=False, showticklabels=False, range=[0, max_val])
    )
    
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# حلقة التحديث التلقائي
time.sleep(15)
st.session_state.week_index += 1
st.rerun()
