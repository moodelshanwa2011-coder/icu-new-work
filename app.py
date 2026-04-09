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
            --bg: #06090c;
            --emerald: #10b981;
            --silver: #f1f5f9;
            --panel: rgba(30, 41, 59, 0.4);
            --border: rgba(16, 185, 129, 0.3);
        }
        
        body {
            font-family: 'Segoe UI', sans-serif;
            background-color: var(--bg);
            color: var(--silver); margin: 0; padding: 20px;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            height: 100vh; overflow: hidden;
        }

        .header {
            margin-bottom: 40px; text-align: center;
        }

        .date-tag {
            background: var(--emerald); color: #000; padding: 8px 30px;
            border-radius: 50px; font-weight: 900; font-size: 1.5rem;
        }

        .grid-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
            width: 90%;
        }

        .stat-group {
            display: flex; align-items: center; gap: 15px; justify-content: center;
        }

        /* الدائرة الأساسية للجهاز */
        .circle-main {
            width: 200px; height: 200px; border-radius: 50%;
            border: 4px solid var(--emerald);
            background: var(--panel);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.1);
        }

        /* دائرة الـ Total Pt الجانبية */
        .circle-total {
            width: 90px; height: 90px; border-radius: 50%;
            border: 2px solid #fff;
            background: rgba(255, 255, 255, 0.05);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            font-size: 0.7rem;
        }

        .val-large { font-size: 4rem; font-weight: 900; color: var(--emerald); line-height: 1; }
        .val-small { font-size: 1.8rem; font-weight: 800; color: #fff; }
        .lbl { font-size: 0.9rem; font-weight: bold; margin-top: 5px; text-align: center; }
        .total-lbl { color: #94a3b8; font-size: 0.6rem; text-transform: uppercase; }

    </style>
</head>
<body>

<div class="header">
    <div style="color: #64748b; margin-bottom: 10px; font-weight: bold;">مراقبة الأجهزة مقابل إجمالي المرضى</div>
    <span id="dateTag" class="date-tag">...</span>
</div>

<div class="grid-container">
    
    <div class="stat-group">
        <div class="circle-main">
            <span class="val-large" id="foleyVal">0</span>
            <span class="lbl">Foley Cath</span>
        </div>
        <div class="circle-total">
            <span class="total-lbl">Total Pt</span>
            <span class="val-small" id="t1">0</span>
        </div>
    </div>

    <div class="stat-group">
        <div class="circle-main">
            <span class="val-large" id="centralVal">0</span>
            <span class="lbl">Central Line</span>
        </div>
        <div class="circle-total">
            <span class="total-lbl">Total Pt</span>
            <span class="val-small" id="t2">0</span>
        </div>
    </div>

    <div class="stat-group">
        <div class="circle-main">
            <span class="val-large" id="ettVal">0</span>
            <span class="lbl">ETT</span>
        </div>
        <div class="circle-total">
            <span class="total-lbl">Total Pt</span>
            <span class="val-small" id="t3">0</span>
        </div>
    </div>

    <div class="stat-group">
        <div class="circle-main">
            <span class="val-large" id="ttVal">0</span>
            <span class="lbl">T.T</span>
        </div>
        <div class="circle-total">
            <span class="total-lbl">Total Pt</span>
            <span class="val-small" id="t4">0</span>
        </div>
    </div>

    <div class="stat-group">
        <div class="circle-main">
            <span class="val-large" id="ivVal">0</span>
            <span class="lbl">IV Access</span>
        </div>
        <div class="circle-total">
            <span class="total-lbl">Total Pt</span>
            <span class="val-small" id="t5">0</span>
        </div>
    </div>

    <div class="stat-group">
        <div class="circle-main" style="border-color: #fff; background: rgba(255,255,255,0.1);">
            <span class="val-large" id="totalPtVal" style="color:#fff">0</span>
            <span class="lbl" style="color:#fff">Total Patient</span>
        </div>
    </div>

</div>

<script>
    // البيانات الفعلية من الجداول والصور
    const dataRecords = [
        {m: "يناير 2024", total: 42, foley: 28, central: 15, ett: 12, tt: 4, iv: 38},
        {m: "فبراير 2024", total: 35, foley: 20, central: 10, ett: 8, tt: 3, iv: 30},
        {m: "مارس 2024", total: 48, foley: 32, central: 18, ett: 15, tt: 5, iv: 45},
        {m: "يناير 2025", total: 40, foley: 25, central: 14, ett: 10, tt: 4, iv: 35},
        {m: "فبراير 2025", total: 38, foley: 22, central: 12, ett: 9, tt: 2, iv: 33}
    ];

    let currentIdx = 0;

    function refresh() {
        const d = dataRecords[currentIdx];
        document.getElementById('dateTag').innerText = d.m;
        
        // الأرقام الأساسية
        document.getElementById('foleyVal').innerText = d.foley;
        document.getElementById('centralVal').innerText = d.central;
        document.getElementById('ettVal').innerText = d.ett;
        document.getElementById('ttVal').innerText = d.tt;
        document.getElementById('ivVal').innerText = d.iv;
        document.getElementById('totalPtVal').innerText = d.total;

        // تحديث دوائر الـ Total Pt الجانبية
        for(let i=1; i<=5; i++) {
            document.getElementById('t'+i).innerText = d.total;
        }

        currentIdx = (currentIdx + 1) % dataRecords.length;
    }

    setInterval(refresh, 3500);
    refresh();
</script>
</body>
</html>
"""

components.html(dashboard_html, height=850, scrolling=False)
