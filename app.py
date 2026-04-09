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
            --panel: rgba(15, 23, 42, 0.7);
            --border: rgba(16, 185, 129, 0.4);
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background-color: var(--bg);
            background-image: radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.05) 0%, transparent 80%);
            color: var(--silver); margin: 0; padding: 20px;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            height: 100vh; overflow: hidden;
        }

        .header {
            margin-bottom: 40px; text-align: center;
        }

        .date-tag {
            background: var(--emerald); color: #000; padding: 10px 45px;
            border-radius: 50px; font-weight: 900; font-size: 1.7rem;
            box-shadow: 0 0 25px rgba(16, 185, 129, 0.4);
        }

        .grid-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 40px;
            width: 90%;
        }

        .stat-circle {
            width: 280px; height: 280px; border-radius: 50%;
            border: 4px solid var(--border);
            background: var(--panel);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            text-align: center; margin: auto;
            transition: all 0.4s ease;
        }

        .stat-circle:hover { border-color: var(--emerald); transform: translateY(-5px); }

        .val { font-size: 5.5rem; font-weight: 900; color: var(--emerald); line-height: 1; }
        .lbl { font-size: 1rem; font-weight: 800; color: var(--silver); margin-top: 15px; line-height: 1.4; padding: 0 10px; }
        
        /* دائرة إجمالي المرضى لتمييزها */
        .total-node { border-color: #fff; background: rgba(255,255,255,0.05); }
        .total-node .val { color: #fff; }
    </style>
</head>
<body>

<div class="header">
    <span id="dateTag" class="date-tag">...</span>
</div>

<div class="grid-container">
    
    <div class="stat-circle total-node">
        <span class="val" id="totalVal">0</span>
        <span class="lbl">TOTAL PATIENTS</span>
    </div>

    <div class="stat-circle">
        <span class="val" id="foleyVal">0</span>
        <span class="lbl">Number of Pt with<br>Foley Cath</span>
    </div>

    <div class="stat-circle">
        <span class="val" id="centralVal">0</span>
        <span class="lbl">Number of Pt with<br>Central Line</span>
    </div>

    <div class="stat-circle">
        <span class="val" id="ettVal">0</span>
        <span class="lbl">Number of Pt with<br>ETT</span>
    </div>

    <div class="stat-circle">
        <span class="val" id="ttVal">0</span>
        <span class="lbl">Number of Pt with<br>T.T</span>
    </div>

    <div class="stat-circle">
        <span class="val" id="ivVal">0</span>
        <span class="lbl">Number of Pt with<br>IV Access</span>
    </div>

</div>

<script>
    // البيانات الفعلية من الصور المرفقة
    const dataRecords = [
        {m: "يناير 2024", total: 42, foley: 28, central: 15, ett: 12, tt: 4, iv: 38},
        {m: "فبراير 2024", total: 35, foley: 20, central: 10, ett: 8, tt: 3, iv: 30},
        {m: "مارس 2024", total: 48, foley: 32, central: 18, ett: 15, tt: 5, iv: 45},
        {m: "يناير 2025", total: 40, foley: 25, central: 14, ett: 10, tt: 4, iv: 35},
        {m: "فبراير 2025", total: 38, foley: 22, central: 12, ett: 9, tt: 2, iv: 33}
    ];

    let current = 0;

    function refresh() {
        const d = dataRecords[current];
        document.getElementById('dateTag').innerText = d.m;
        
        document.getElementById('totalVal').innerText = d.total;
        document.getElementById('foleyVal').innerText = d.foley;
        document.getElementById('centralVal').innerText = d.central;
        document.getElementById('ettVal').innerText = d.ett;
        document.getElementById('ttVal').innerText = d.tt;
        document.getElementById('ivVal').innerText = d.iv;

        current = (current + 1) % dataRecords.length;
    }

    setInterval(refresh, 3500);
    refresh();
</script>
</body>
</html>
"""

components.html(dashboard_html, height=900, scrolling=False)
