import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Monitor", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <style>
        :root {
            --bg: #05070a;
            --emerald: #10b981;
            --gray: #1e293b;
            --white: #ffffff;
        }
        
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: var(--bg);
            color: var(--white);
            margin: 0; padding: 0;
            display: flex; justify-content: center; align-items: center;
            height: 100vh; overflow: hidden;
        }

        .container {
            text-align: center;
            display: flex; flex-direction: column; gap: 20px;
        }

        /* تصميم الدائرة الكبيرة للوفيات */
        .mortality-circle {
            width: 320px; height: 320px; border-radius: 50%;
            border: 8px solid var(--emerald);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            background: rgba(16, 185, 129, 0.05);
            box-shadow: 0 0 50px rgba(16, 185, 129, 0.2);
            margin: auto;
        }

        .mortality-title { font-size: 1.8rem; font-weight: 800; color: var(--emerald); margin-bottom: 5px; }
        .mortality-val { font-size: 8rem; font-weight: 900; line-height: 1; }

        /* تصميم دوائر الشهور والسنين */
        .info-row { display: flex; gap: 30px; justify-content: center; }

        .info-circle {
            width: 150px; height: 150px; border-radius: 50%;
            border: 3px solid var(--gray);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            background: rgba(30, 41, 59, 0.2);
        }

        .info-lbl { font-size: 0.9rem; color: #94a3b8; margin-bottom: 5px; font-weight: bold; }
        .info-val { font-size: 1.8rem; font-weight: 700; color: var(--white); }

    </style>
</head>
<body>

<div class="container">
    <div class="mortality-circle">
        <span class="mortality-title">عدد الوفيات</span>
        <span class="mortality-val" id="mortVal">0</span>
    </div>

    <div class="info-row">
        <div class="info-circle">
            <span class="info-lbl">الشهر</span>
            <span class="info-val" id="monthVal">...</span>
        </div>
        <div class="info-circle">
            <span class="info-lbl">السنة</span>
            <span class="info-val" id="yearVal">...</span>
        </div>
    </div>
</div>

<script>
    // البيانات الفعلية المستخرجة من ملفك
    const data = [
        {y: "2023", m: "يناير", v: 8}, {y: "2023", m: "فبراير", v: 4}, {y: "2023", m: "مارس", v: 7}, {y: "2023", m: "أبريل", v: 5},
        {y: "2023", m: "مايو", v: 3}, {y: "2023", m: "يونيو", v: 8}, {y: "2023", m: "يوليو", v: 3}, {y: "2023", m: "أغسطس", v: 4},
        {y: "2023", m: "سبتمبر", v: 7}, {y: "2023", m: "أكتوبر", v: 2}, {y: "2023", m: "نوفمبر", v: 3}, {y: "2023", m: "ديسمبر", v: 4},
        {y: "2024", m: "يناير", v: 6}, {y: "2024", m: "فبراير", v: 3}, {y: "2024", m: "مارس", v: 7}, {y: "2024", m: "أبريل", v: 7},
        {y: "2024", m: "مايو", v: 1}, {y: "2024", m: "يونيو", v: 6}, {y: "2024", m: "يوليو", v: 2}, {y: "2024", m: "أغسطس", v: 8},
        {y: "2025", m: "يناير", v: 6}, {y: "2025", m: "فبراير", v: 3}, {y: "2025", m: "مارس", v: 7}
    ];

    let i = 0;

    function update() {
        const item = data[i];
        document.getElementById('mortVal').innerText = item.v;
        document.getElementById('monthVal').innerText = item.m;
        document.getElementById('yearVal').innerText = item.y;
        
        i = (i + 1) % data.length;
    }

    setInterval(update, 3000);
    update();
</script>
</body>
</html>
"""

components.html(dashboard_html, height=800, scrolling=False)
