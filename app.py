import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="ICU Elite Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS احترافي (Focus on Typography & Spacing)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; padding: 20px; }
    
    /* تنسيق كروت الأجهزة (يسار) */
    .dev-box {
        background-color: #0a0a0a;
        border: 1px solid #1f77b4;
        border-left: 4px solid #00d4ff;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 20px; /* مسافة أوسع بين المربعات */
        text-align: center;
    }
    .dev-label { color: #888; font-size: 14px; font-weight: bold; text-transform: uppercase; }
    .dev-value { color: #ffffff; font-size: 30px; font-weight: 900; }

    /* تحسين وضوح أسماء الـ KPIs */
    .gauge-title {
        color: #ffffff;
        font-size: 16px !important;
        font-weight: 800;
        margin-bottom: -10px;
        text-align: center;
    }
    .bench-label {
        color: #555;
        font-size: 14px;
        font-weight: bold;
        text-align: center;
        margin-top: -5px;
    }
    hr { border: 0.5px solid #222; margin: 30px 0; }
    #stProgress { display: none; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. داتا الـ PDF والصور
data_cycle = [
    {
        "period": "3Q 2025",
        "falls": 0.0, "falls_m": 0.18, "injury": 0.0, "injury_m": 0.04,
        "restraint": 0.45, "restraint_m": 0.90, "hapi": 6.67, "hapi_m": 4.58, 
        "clabsi": 1.50, "clabsi_m": 3.38, "cauti": 0.0, "cauti_m": 0.44,
        "vae": 1.6, "vae_m": 3.4, "edu": 85.01, "edu_m": 70.59,
        "vents": 14, "foley": 15, "cvc": 8, "stay": 34
    },
    {
        "period": "2Q 2024",
        "falls": 0.24, "falls_m": 0.06, "injury": 0.24, "injury_m": 0.01,
        "restraint": 0.70, "restraint_m": 0.96, "hapi": 14.29, "hapi_m": 6.54, 
        "clabsi": 1.28, "clabsi_m": 2.67, "cauti": 0.70, "cauti_m": 0.99,
        "vae": 2.17, "vae_m": 2.42, "edu": 82.99, "edu_m": 70.31,
        "vents": 12, "foley": 14, "cvc": 9, "stay": 28
    }
]
d = data_cycle[st.session_state.step % len(data_cycle)]

# --- العنوان العلوي ---
st.markdown(f"<h2 style='text-align: center; color: white; letter-spacing: 2px;'>ICU PERFORMANCE COMMAND CENTER</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00d4ff;'>REPORTING PERIOD: {d['period']}</p>", unsafe_allow_html=True)

# 4. دالة الـ Gauge المحسنة (صغيرة وواضحة)
def draw_clean_gauge(label, val, target, is_perc=False, is_edu=False):
    # منطق الألوان (إشارة المرور)
    color = "#00CC96" if (val <= target if not is_edu else val >= target) else "#FF4B4B"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=val,
        number={'suffix': "%" if is_perc else "", 'font': {'size': 26, 'color': 'white'}},
        gauge={'axis': {'range': [0, max(val, target)*1.8], 'visible': False},
               'bar': {'color': color, 'thickness': 0.75},
               'bgcolor': "#1a1a1a",
               'threshold': {'line': {'color': "white", 'width': 3}, 'thickness': 0.8, 'value': target}}))
    
    fig.update_layout(height=130, margin=dict(l=25, r=25, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)')
    
    # اسم الـ KPI فوق الرسم
    st.markdown(f'<div class="gauge-title">{label}</div>', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f'<div class="bench-label">Bench: {target}</div>', unsafe_allow_html=True)

# توزيع الـ 8 KPIs في صفين بمسافات واسعة
st.markdown("<br>", unsafe_allow_html=True)
g_c1, g_c2, g_c3, g_c4 = st.columns(4)
with g_c1: draw_clean_gauge("Total Falls", d['falls'], d['falls_m'])
with g_c2: draw_clean_gauge("Injury Falls", d['injury'], d['injury_m'])
with g_c3: draw_clean_gauge("HAPI %", d['hapi'], d['hapi_m'], True)
with g_c4: draw_clean_gauge("RN Education", d['edu'], d['edu_m'], True, True)

st.markdown("<div style='margin-top: 40px;'></div>", unsafe_allow_html=True) # مسافة بين الصفين

g_c5, g_c6, g_c7, g_c8 = st.columns(4)
with g_c5: draw_clean_gauge("Restraints", d['restraint'], d['restraint_m'])
with g_c6: draw_clean_gauge("CLABSI Rate", d['clabsi'], d['clabsi_m'])
with g_c7: draw_clean_gauge("CAUTI Rate", d['cauti'], d['cauti_m'])
with g_c8: draw_clean_gauge("VAE/VAP", d['vae'], d['vae_m'])

st.markdown("<hr>", unsafe_allow_html=True)

# 5. الجزء السفلي: المربعات (يسار) + البار الاحترافي (يمين)
col_left, col_right = st.columns([1, 2.5])

with col_left:
    def dev_card(l, v):
        st.markdown(f'<div class="dev-box"><div class="dev-label">{l}</div><div class="dev-value">{v}</div></div>', unsafe_allow_html=True)
    dev_card("Ventilators", d['vents'])
    dev_card("Foley Catheter", d['foley'])
    dev_card("Central Line", d['cvc'])
    dev_card("Total Stay", d['stay'])

with col_right:
    # بار تشارت احترافي (ألوان متدرجة وتصميم عصري)
    labels = ['Falls', 'Injury', 'Restraint', 'CLABSI', 'CAUTI', 'VAE']
    vals = [d['falls'], d['injury'], d['restraint'], d['clabsi'], d['cauti'], d['vae']]
    benchs = [d['falls_m'], d['injury_m'], d['restraint_m'], d['clabsi_m'], d['cauti_m'], d['vae_m']]
    
    fig_bar = go.Figure()
    # أعمدة المستشفى (أزرق نيون بحدود)
    fig_bar.add_trace(go.Bar(
        name='Current Performance', x=labels, y=vals,
        marker=dict(color='#00d4ff', line=dict(color='#ffffff', width=1.5)),
        text=vals, textposition='outside', textfont=dict(color='white', size=14)
    ))
    # أعمدة الـ Benchmark (رمادي داكن مطفي)
    fig_bar.add_trace(go.Bar(
        name='Benchmark', x=labels, y=benchs,
        marker=dict(color='#333333', line=dict(color='#555555', width=1)),
        text=benchs, textposition='outside', textfont=dict(color='#888', size=12)
    ))
    
    fig_bar.update_layout(
        height=450, barmode='group',
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='sans-serif'),
        legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5, font=dict(size=14)),
        margin=dict(l=0, r=0, t=10, b=0),
        yaxis=dict(showgrid=True, gridcolor='#222', zeroline=False),
        xaxis=dict(tickfont=dict(size=14, weight='bold'))
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

# تحديث تلقائي صامت
time.sleep(15)
st.session_state.step += 1
st.rerun()
