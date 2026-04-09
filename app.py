import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Weekly Monitor", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
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
            font-family: 'Segoe UI', sans-serif;
            background-color: var(--bg);
            background-image: radial-gradient(circle at 50% 50%, rgba(16, 185, 129, 0.05) 0%, transparent 80%);
            color: var(--silver); margin: 0; padding: 20px;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            height: 100vh; overflow: hidden;
        }

        .header { margin-bottom: 30px; text-align: center; }

        .date-tag {
            background: var(--emerald); color: #000; padding: 12px 50px;
            border-radius: 50px; font-weight: 900; font-size: 1.8rem;
            box-shadow: 0 0 25px rgba(16, 185, 129, 0.4);
            text-transform: uppercase;
        }

        .grid-container {
            display: grid; grid-template-columns: repeat(3, 1fr);
            gap: 40px; width: 85%;
        }

        .stat-circle {
            width: 270px; height: 270px; border-radius: 50%;
            border: 4px solid var(--border); background: var(--panel);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            text-align: center; margin: auto; transition: all 0.6s ease-in-out;
        }

        .val { font-size: 6rem; font-weight: 900; color: var(--emerald); line-height: 1; }
        .lbl { font-size: 1rem; font-weight: 800; color: var(--silver); margin-top: 15px; line-height: 1.3; }
        
        .total-node { border-color: #fff; background: rgba(255,255,255,0.05); }
        .total-node .val { color: #fff; }

        .fade { animation: fadeIn 1s; }
        @keyframes fadeIn { from { opacity: 0.3; } to { opacity: 1; } }
    </style>
</head>
<body>

<div class="header">
    <span id="dateTag" class="date-tag">...</span>
</div>

<div id="mainGrid" class="grid-container">
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
    // Weekly data for March & April (Month names in English)
    const weeklyData = [
        // MARCH - 4 Weeks
        {t: "MARCH - Week 1", total: 45, foley: 30, central: 18, ett: 14, tt: 5, iv: 42},
        {t: "MARCH - Week 2", total: 48, foley: 32, central: 20, ett: 15, tt: 5, iv: 45},
        {t: "MARCH - Week 3", total: 42, foley: 28, central: 16, ett: 12, tt: 4, iv: 40},
        {t: "MARCH - Week 4", total: 44, foley: 29, central: 17, ett: 13, tt: 4, iv: 41},
        // APRIL - 4 Weeks
        {t: "APRIL - Week 1", total: 40, foley: 25, central: 14, ett: 10, tt: 3, iv: 36},
        {t: "APRIL - Week 2", total: 38, foley: 22, central: 12, ett: 9, tt: 3, iv: 34},
        {t: "APRIL - Week 3", total: 41, foley: 26, central: 15, ett: 11, tt: 4, iv: 37},
        {t: "APRIL - Week 4", total: 39, foley: 24, central: 13, ett: 10, tt: 3, iv: 35}
    ];

    let currentIndex = 0;

    function refresh() {
        const d = weeklyData[currentIndex];
        const grid = document.getElementById('mainGrid');
        
        grid.classList.remove('fade');
        void grid.offsetWidth; 
        grid.classList.add('fade');

        document.getElementById('dateTag').innerText = d.t;
        document.getElementById('totalVal').innerText = d.total;
        document.getElementById('foleyVal').innerText = d.foley;
        document.getElementById('centralVal').innerText = d.central;
        document.getElementById('ettVal').innerText = d.ett;
        document.getElementById('ttVal').innerText = d.tt;
        document.getElementById('ivVal').innerText = d.iv;

        currentIndex = (currentIndex + 1) % weeklyData.length;
    }

    // Refresh every 15 seconds
    setInterval(refresh, 15000);
    refresh();
</script>
</body>
</html>
"""

components.html(dashboard_html, height=900, scrolling=False)
