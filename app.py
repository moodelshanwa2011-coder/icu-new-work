import streamlit as st
import plotly.graph_objects as go
import time

# 1. إعدادات الصفحة (شاشة عرض كاملة)
st.set_page_config(page_title="ICU Live Command", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS احترافي (منع الوميض وتوضيح الحدود)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #000000; }
    /* تحسين حدود مربعات الأجهزة */
    .device-card {
        background-color: #0a0a0a;
        border: 2px solid #1f77b4; /* حدود واضحة وباحترافية */
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .device-label { color: #aaaaaa; font-size: 18px; font-weight: bold; margin-bottom: 15px; }
    .device-value { color: #00d4ff; font-size: 55px; font-weight: 900; text-shadow: 0 0 10px #00d4ff55; }
    .bench-label { color: #666666; font-size: 16px; margin-top: -5px; font-weight: bold; text-align: center; }
    /* إخفاء شريط التحميل بالأعلى لتقليل التشتت */
    #stProgress { display: none; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = 0

# 3. قاعدة البيانات (البيانات الكاملة)
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

# 4. منطق الألوان الذكي (إشارات المرور)
def get_status_color(val, target, reverse=False):
    # reverse=True تستخدم للـ Education لأن الأعلى هو الأفضل
    if reverse:
        if val >= target: return "#00CC96" # أخضر (آمن)
        if val >= target * 0.9: return "#FFD700" # أصفر (تحذير)
        return "#FF4B4B" # أحمر (خطر)
    else:
        if val <= target * 0.5: return "#00CC96" # أخضر (ممتاز)
        if val <= target: return "#FFD700" # أصفر (انتباه)
        return "#FF4B4B" # أحمر (تجاوز الهدف)

# --- العنوان الرئيسي ---
st.markdown(f"<h1 style='text-align: center; color: white;'>🏥 ICU COMMAND CENTER | {d['period']}</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# دالة رسم النص دائرة المحسنة
def draw_smart_gauge(label, val, target, is_perc=False, is_edu=False):
    color = get_status_color(val, target, reverse=is_edu)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        number={'suffix': "%" if is_perc else "", 'font': {'size': 35, 'color': 'white'}},
        title={'text': label, 'font': {'size': 18, 'color': 'white'}},
        gauge={
            'axis': {'range': [0, max(val, target)*1.5], 'tickcolor': "white"},
            'bar': {'color': color},
            'bgcolor': "#111",
            'threshold': {'line': {'color': "white", 'width': 3}, 'thickness': 0.8, 'value': target}
        }
    ))
    fig.update_layout(height=180, margin=dict(l=30, r=30, t=40, b=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown(f'<div class="bench-label">Benchmark: {target}{"%" if is_perc else ""}</div>', unsafe_allow_html=True)

# --- الصف الأول ---
c1, c2, c3, c4 = st.columns(4)
with c1: draw_smart_gauge("Total Falls", d['falls'], d['falls_m'])
with c2: draw_smart_gauge("Injury Falls", d['injury'], d['injury_m'])
with c3: draw_smart_gauge("HAPI %", d['hapi'], d['hapi_m'], is_perc=True)
with c4: draw_smart_gauge("RN Education", d['edu'], d['edu_m'], is_perc=True, is_edu=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- الصف الثاني ---
c5, c6, c7, c8 = st.columns(4)
with c5: draw_smart_gauge("Restraints", d['restraint'], d['restraint_m'])
with c6: draw_smart_gauge("CLABSI Rate", d['clabsi'], d['clabsi_m'])
with c7: draw_smart_gauge("CAUTI Rate", d['cauti'], d['cauti_m'])
with c8: draw_smart_gauge("VAE/VAP", d['vae'], d['vae_m'])

st.markdown("<br><br><br>", unsafe_allow_html=True)

# --- الجزء السفلي: الأجهزة الموصولة (المربعات المحسنة) ---
st.markdown("<h2 style='color: white; text-align: center; font-size: 30px;'>CURRENT ATTACHED DEVICES</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
d_cols = st.columns(4)

def device_card(label, value):
    st.markdown(f"""
        <div class="device-card">
            <div class="device-label">{label}</div>
            <div class="device-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

with d_cols[0]: device_card("Ventilators", d['vents'])
with d_cols[1]: device_card("Foley Catheter", d['foley'])
with d_cols[2]: device_card("Central Line", d['cvc'])
with d_cols[3]: device_card("Total Occupancy", d['stay'])

# 5. التحديث الصامت (تقليل الوميض)
time.sleep(15)
st.session_state.step += 1
st.rerun()
