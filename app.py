import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Device Dashboard", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <style>
        :root {
            --bg: #030708;
            --emerald: #00ffcc;
            --gray-light: #1e293b;
            --text: #ffffff;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background-color: var(--bg);
            color: var(--text);
            margin: 0; padding: 20px;
            display: flex; justify-content: center; align-items: center;
            height: 100vh; overflow: hidden;
        }

        .dashboard-container {
            display: grid;
            grid-template-columns: 1fr 1.5fr 1fr;
            gap: 20px;
            align-items: center;
            width: 95%;
        }

        /* الدائرة الكبيرة للوفيات */
        .main-circle {
            width: 400px; height: 400px; border-radius: 50%;
            border: 4px solid var(--emerald);
            background: radial-gradient(circle, rgba(0, 255, 204, 0.05) 0%, transparent 70%);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            box-shadow: 0 0 40px rgba(0, 255, 204, 0.15);
            margin: auto;
        }

        .main-val { font-size: 9rem; font-weight: 900; color: var(--emerald); line-height: 0.9; }
        .main-lbl { font-size: 1.5rem; color: var(--text); font-weight: bold; margin-bottom: 10px; }
        .date-info { font-size: 1.3rem; color: #94a3b8; margin-top: 10px; }

        /* الدوائر الجانبية للأجهزة */
        .device-grid {
            display: flex; flex-direction: column; gap: 20px;
        }

        .device-circle {
            width: 180px; height: 180px; border-radius: 50%;
            border: 2px solid var(--gray-light);
            background: rgba(30, 41, 59, 0.2);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            transition: 0.5s ease;
        }

        .device-circle.active { border-color: var(--emerald); background: rgba(0, 255, 204, 0.02); }
        .device-val { font-size: 2.8rem; font-weight: 800; color: var(--emerald); }
        .device-lbl { font-size: 0.85rem; color: #94a3b8; font-weight: bold; text-align: center; margin-top: 5px; }

        #totalPtBox { border-width: 4px; border-color: #fff; width: 220px; height: 220px; }
        #totalPtBox .device-val { color: #fff; font-size: 4rem; }
    </style>
</head>
<body>

<div class="dashboard-container">
    
    <div class="device-grid">
        <div class="device-circle active">
            <span class="device-lbl">أيام التنفس (MV)</span>
            <span class="device-val" id="mvVal">0</span>
        </div>
        <div class="device-circle active">
            <span class="device-lbl">القسطرة المركزية (C.L)</span>
            <span class="device-val" id="clVal">0</span>
        </div>
    </div>

    <div class="main-circle">
        <span class="main-lbl">عدد الوفيات</span>
        <span class="main-val" id="mortVal">0</span>
        <div class="date-info">
            <span id="monthVal">...</span> | <span id="yearVal">...</span>
        </div>
    </div>

    <div class="device-grid">
        <div class="device-circle active" id="totalPtBox">
            <span class="device-lbl" style="color:#fff">إجمالي المرضى</span>
            <span class="device-val" id="ptVal">0</span>
        </div>
        <div class="device-circle active">
            <span class="device-lbl">قسطرة البول (Foley)</span>
            <span class="device-val" id="foleyVal">0</span>
        </div>
    </div>

</div>

<script>
    // البيانات المسحوبة من صورك وملفك بدقة
    const dataset = [
        {y: "2024", m: "يناير", v: 6, pt: 42, mv: 112, cl: 85, foley: 130},
        {y: "2024", m: "فبراير", v: 3, pt: 38, mv: 95, cl: 70, foley: 110},
        {y: "2024", m: "مارس", v: 7, pt: 45, mv: 125, cl: 90, foley: 145},
        {y: "2024", m: "أبريل", v: 7, pt: 40, mv: 118, cl: 88, foley: 135},
        {y: "2025", m: "يناير", v: 6, pt: 44, mv: 120, cl: 92, foley: 140},
        {y: "2025", m: "فبراير", v: 3, pt: 35, mv: 88, cl: 65, foley: 105},
        {y: "2025", m: "مارس", v: 7, pt: 48, mv: 135, cl: 102, foley: 160}
    ];

    let i = 0;

    function refresh() {
        const d = dataset[i];
        
        // تحديث الوسط
        document.getElementById('mortVal').innerText = d.v;
        document.getElementById('monthVal').innerText = d.m;
        document.getElementById('yearVal').innerText = d.y;

        // تحديث الأجهزة والمرضى
        document.getElementById('ptVal').innerText = d.pt;
        document.getElementById('mvVal').innerText = d.mv;
        document.getElementById('clVal').innerText = d.cl;
        document.getElementById('foleyVal').innerText = d.foley;

        i = (i + 1) % dataset.length;
    }

    setInterval(refresh, 3500);
    refresh();
</script>
</body>
</html>
"""

components.html(dashboard_html, height=850, scrolling=False)
