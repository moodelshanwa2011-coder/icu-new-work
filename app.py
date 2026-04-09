import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Monitor Pro", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <style>
        :root {
            --bg: #05080a;
            --emerald: #10b981;
            --silver: #e2e8f0;
            --gray-panel: rgba(30, 41, 59, 0.3);
            --border: rgba(16, 185, 129, 0.4);
        }
        
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: var(--bg);
            color: var(--silver); margin: 0; padding: 20px;
            display: flex; justify-content: center; align-items: center;
            height: 100vh; overflow: hidden;
        }

        .main-layout {
            display: grid;
            grid-template-columns: 1fr 1.5fr 1fr;
            gap: 30px;
            width: 95%;
            align-items: center;
        }

        /* الدائرة المركزية (عدد الوفيات والتاريخ) */
        .center-circle {
            width: 380px; height: 380px; border-radius: 50%;
            border: 6px solid var(--emerald);
            background: radial-gradient(circle, rgba(16, 185, 129, 0.1) 0%, transparent 75%);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            box-shadow: 0 0 50px rgba(16, 185, 129, 0.15);
            margin: auto;
        }

        .mort-val { font-size: 8rem; font-weight: 900; color: var(--emerald); line-height: 1; }
        .mort-lbl { font-size: 1.6rem; font-weight: 700; margin-bottom: 10px; }
        .date-box { font-size: 1.3rem; color: var(--silver); margin-top: 15px; border-top: 1px solid var(--border); padding-top: 10px; }

        /* الدوائر الجانبية للمتغيرات الستة */
        .side-grid {
            display: flex; flex-direction: column; gap: 20px;
        }

        .stat-circle {
            width: 170px; height: 170px; border-radius: 50%;
            border: 2px solid var(--border);
            background: var(--gray-panel);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            text-align: center; transition: 0.4s ease;
        }

        .stat-circle.highlight { border-color: #fff; border-width: 3px; width: 190px; height: 190px; }
        .stat-val { font-size: 2.5rem; font-weight: 800; color: var(--emerald); }
        .stat-lbl { font-size: 0.85rem; color: var(--silver); font-weight: 600; padding: 0 10px; margin-top: 5px; }
        .highlight .stat-val { color: #fff; font-size: 3.2rem; }

    </style>
</head>
<body>

<div class="main-layout">
    
    <div class="side-grid">
        <div class="stat-circle">
            <span class="stat-val" id="foleyVal">0</span>
            <span class="stat-lbl">Foley Cath</span>
        </div>
        <div class="stat-circle">
            <span class="stat-val" id="centralVal">0</span>
            <span class="stat-lbl">Central Line</span>
        </div>
        <div class="stat-circle">
            <span class="stat-val" id="ettVal">0</span>
            <span class="stat-lbl">ETT</span>
        </div>
    </div>

    <div class="center-circle">
        <span class="mort-lbl">عدد الوفيات</span>
        <span class="mort-val" id="mortVal">0</span>
        <div class="date-box">
            <span id="monthVal">...</span> | <span id="yearVal">...</span>
        </div>
    </div>

    <div class="side-grid">
        <div class="stat-circle highlight">
            <span class="stat-val" id="totalPtVal">0</span>
            <span class="stat-lbl">Total Patient</span>
        </div>
        <div class="stat-circle">
            <span class="stat-val" id="ttVal">0</span>
            <span class="stat-lbl">T.T</span>
        </div>
        <div class="stat-circle">
            <span class="stat-val" id="ivVal">0</span>
            <span class="stat-lbl">IV Access</span>
        </div>
    </div>

</div>

<script>
    // البيانات المسحوبة من الصور بدقة (تم دمجها مع جدول الوفيات)
    const records = [
        {y: "2024", m: "يناير", mort: 6, total: 42, foley: 28, central: 15, ett: 12, tt: 4, iv: 38},
        {y: "2024", m: "فبراير", mort: 3, total: 35, foley: 20, central: 10, ett: 8, tt: 3, iv: 30},
        {y: "2024", m: "مارس", mort: 7, total: 48, foley: 32, central: 18, ett: 15, tt: 5, iv: 45},
        {y: "2025", m: "يناير", mort: 6, total: 40, foley: 25, central: 14, ett: 10, tt: 4, iv: 35},
        {y: "2025", m: "فبراير", mort: 3, total: 38, foley: 22, central: 12, ett: 9, tt: 2, iv: 33}
    ];

    let current = 0;

    function updateDashboard() {
        const data = records[current];
        
        // المركز
        document.getElementById('mortVal').innerText = data.mort;
        document.getElementById('monthVal').innerText = data.m;
        document.getElementById('yearVal').innerText = data.y;

        // الإحصائيات الستة
        document.getElementById('totalPtVal').innerText = data.total;
        document.getElementById('foleyVal').innerText = data.foley;
        document.getElementById('centralVal').innerText = data.central;
        document.getElementById('ettVal').innerText = data.ett;
        document.getElementById('ttVal').innerText = data.tt;
        document.getElementById('ivVal').innerText = data.iv;

        current = (current + 1) % records.length;
    }

    setInterval(updateDashboard, 3000);
    updateDashboard();
</script>
</body>
</html>
"""

components.html(dashboard_html, height=850, scrolling=False)
