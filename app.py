import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Monitor", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #06080a;
            --emerald: #00ffaa;
            --gray: #1e293b;
            --text: #f8fafc;
        }
        
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: var(--bg);
            color: var(--text); margin: 0; padding: 20px; overflow: hidden;
        }

        .header {
            text-align: center; margin-bottom: 40px; border-bottom: 1px solid var(--gray);
            padding-bottom: 20px;
        }

        .main-grid {
            display: flex; justify-content: space-around; align-items: center;
            height: 70vh;
        }

        /* الدائرة المركزية الكبيرة */
        .center-circle {
            width: 450px; height: 450px; border-radius: 50%;
            background: radial-gradient(circle, rgba(0, 255, 170, 0.05) 0%, transparent 70%);
            border: 4px solid var(--gray);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            position: relative; transition: 0.5s;
        }

        .center-circle::before {
            content: ''; position: absolute; top: -10px; left: -10px; right: -10px; bottom: -10px;
            border-radius: 50%; border: 1px dashed var(--emerald); opacity: 0.3;
        }

        .val-big { font-size: 10rem; font-weight: 900; color: var(--emerald); line-height: 1; text-shadow: 0 0 30px rgba(0, 255, 170, 0.3); }
        .lbl-big { font-size: 1.8rem; font-weight: 600; color: var(--text); margin-top: 10px; }

        /* الدوائر الجانبية */
        .side-circle {
            width: 220px; height: 220px; border-radius: 50%;
            border: 2px solid var(--gray); background: rgba(30, 41, 59, 0.2);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
        }

        .val-small { font-size: 3.5rem; font-weight: 700; color: var(--text); }
        .lbl-small { font-size: 0.9rem; color: #64748b; text-transform: uppercase; }

        #dateLabel {
            background: var(--emerald); color: #000; padding: 10px 30px;
            border-radius: 50px; font-weight: 900; font-size: 1.4rem;
        }
    </style>
</head>
<body>

<div class="header">
    <div style="margin-bottom:15px; font-size: 1.2rem; color: #64748b;">سجل بيانات العناية المركزة</div>
    <span id="dateLabel">...</span>
</div>

<div class="main-grid">
    <div class="side-circle">
        <span class="lbl-small">الهدف الشهري</span>
        <span class="val-small">4</span>
    </div>

    <div class="center-circle">
        <span class="lbl-big">عدد الوفيات</span>
        <span class="val-big" id="mainVal">0</span>
    </div>

    <div class="side-circle">
        <span class="lbl-small">مؤشر الحالة</span>
        <span id="statusText" class="val-small" style="font-size: 2rem;">مستقر</span>
    </div>
</div>

<script>
    // البيانات الفعلية من ملفك - مرتبة حسب السنوات
    const records = [
        // 2023
        {m: "يناير 2023", v: 8}, {m: "فبراير 2023", v: 4}, {m: "مارس 2023", v: 7}, {m: "أبريل 2023", v: 5},
        {m: "مايو 2023", v: 3}, {m: "يونيو 2023", v: 8}, {m: "يوليو 2023", v: 3}, {m: "أغسطس 2023", v: 4},
        {m: "سبتمبر 2023", v: 7}, {m: "أكتوبر 2023", v: 2}, {m: "نوفمبر 2023", v: 3}, {m: "ديسمبر 2023", v: 4},
        // 2024
        {m: "يناير 2024", v: 6}, {m: "فبراير 2024", v: 3}, {m: "مارس 2024", v: 7}, {m: "أبريل 2024", v: 7},
        {m: "مايو 2024", v: 1}, {m: "يونيو 2024", v: 6}, {m: "يوليو 2024", v: 2}, {m: "أغسطس 2024", v: 8},
        // 2025
        {m: "يناير 2025", v: 6}, {m: "فبراير 2025", v: 3}, {m: "مارس 2025", v: 7}
    ];

    let idx = 0;

    function rotateData() {
        const item = records[idx];
        document.getElementById('dateLabel').innerText = item.m;
        document.getElementById('mainVal').innerText = item.v;

        // تغيير نص الحالة بناءً على الرقم
        const status = document.getElementById('statusText');
        if(item.v > 6) {
            status.innerText = "مرتفع";
            status.style.color = "#ff4444";
        } else if(item.v > 4) {
            status.innerText = "متوسط";
            status.style.color = "#ffbb00";
        } else {
            status.innerText = "جيد جداً";
            status.style.color = "#00ffaa";
        }

        idx = (idx + 1) % records.length;
    }

    setInterval(rotateData, 3000);
    rotateData();
</script>
</body>
</html>
"""

components.html(dashboard_html, height=900, scrolling=False)
