import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Performance Monitor | SGH", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #01040a;
            --panel-bg: rgba(10, 25, 47, 0.95);
            --safe-blue: #00f2ff;
            --neon-purple: #bc13fe;
            --grid-line: rgba(0, 242, 255, 0.05);
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            background-image: linear-gradient(var(--grid-line) 1px, transparent 1px), linear-gradient(90deg, var(--grid-line) 1px, transparent 1px);
            background-size: 30px 30px;
            color: #fff; margin: 0; padding: 10px; overflow: hidden;
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            background: var(--panel-bg); padding: 10px 30px; border-radius: 8px;
            border: 2px solid var(--safe-blue); margin-bottom: 15px;
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
        }

        .main-container {
            display: grid; grid-template-columns: 2.2fr 1.8fr; gap: 15px; height: 85vh;
        }

        .panel {
            background: var(--panel-bg); border: 1.5px solid var(--safe-blue);
            border-radius: 12px; padding: 15px; display: flex; flex-direction: column;
        }

        .panel-title {
            font-size: 0.85rem; font-weight: 900; color: var(--safe-blue);
            text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px;
            border-left: 5px solid var(--safe-blue); padding-left: 10px;
        }

        /* مربعات الأجهزة - حجم صغير جداً ومدمج */
        .mini-grid {
            display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px; margin-bottom: 15px;
        }

        .mini-box {
            background: rgba(0, 242, 255, 0.03); border: 1px solid rgba(0, 242, 255, 0.2);
            border-radius: 6px; padding: 10px 2px; text-align: center;
        }

        .mini-val { font-size: 1.5rem; font-weight: 900; color: var(--safe-blue); display: block; }
        .mini-lbl { font-size: 0.55rem; color: #94a3b8; text-transform: uppercase; font-weight: 700; }

        #dateLabel {
            background: var(--safe-blue); color: #000; padding: 5px 20px; 
            border-radius: 4px; font-weight: 900; font-size: 1.1rem;
        }
    </style>
</head>
<body>

<div class="header">
    <div style="font-size: 1.4rem; font-weight: 900; letter-spacing: 2px;">ICU <span style="color:var(--safe-blue)">CLINICAL</span> INTEGRATION</div>
    <div id="dateLabel">...</div>
</div>

<div class="mini-grid" id="deviceStats"></div>

<div class="main-container">
    <div class="panel">
        <div class="panel-title">Medical Device Census (Weekly Trend)</div>
        <div style="flex-grow: 1;">
            <canvas id="deviceChart"></canvas>
        </div>
    </div>
    
    <div class="panel">
        <div class="panel-title">Infection Indicators (NDNQI - PDF Data)</div>
        <div style="flex-grow: 1;">
            <canvas id="pdfChart"></canvas>
        </div>
        <div style="margin-top:15px; font-size:0.7rem; color:#94a3b8; border-top:1px solid #1e293b; padding-top:10px;">
            * Data source: Saudi German Hospital - ICU Riyadh PDF (4Q23 - 1Q25)
        </div>
    </div>
</div>

<script>
    // بيانات الأجهزة الأسبوعية (الشغل الجديد)
    const deviceWeekly = [
        {t: "MARCH - Week 1", census: 45, foley: 30, central: 18, ett: 14, tt: 5, iv: 42},
        {t: "MARCH - Week 2", census: 48, foley: 32, central: 20, ett: 15, tt: 5, iv: 45},
        {t: "APRIL - Week 1", census: 40, foley: 25, central: 14, ett: 10, tt: 3, iv: 36},
        {t: "APRIL - Week 2", census: 38, foley: 22, central: 12, ett: 9, tt: 3, iv: 34}
    ];

    // بيانات من ملف الـ PDF الفعلي (Infection rates)
    const pdfData = {
        labels: ["4Q23", "1Q24", "2Q24", "3Q24", "1Q25"],
        clabsi: [1.38, 1.28, 1.56, 1.20, 1.26],
        cauti: [0, 0.70, 0.67, 0.40, 0.43],
        falls: [0, 0.24, 0.24, 0.28, 1.59]
    };

    let idx = 0;
    let devChart, infectionChart;

    function update() {
        const d = deviceWeekly[idx];
        document.getElementById('dateLabel').innerText = d.t;

        // تحديث المربعات (Devices only)
        document.getElementById('deviceStats').innerHTML = `
            <div class="mini-box"><span class="mini-val">${d.census}</span><span class="mini-lbl">Census</span></div>
            <div class="mini-box"><span class="mini-val">${d.foley}</span><span class="mini-lbl">Foley</span></div>
            <div class="mini-box"><span class="mini-val">${d.central}</span><span class="mini-lbl">C-Line</span></div>
            <div class="mini-box"><span class="mini-val">${d.ett}</span><span class="mini-lbl">ETT</span></div>
            <div class="mini-box"><span class="mini-val">${d.tt}</span><span class="mini-lbl">T.T</span></div>
            <div class="mini-box"><span class="mini-val">${d.iv}</span><span class="mini-lbl">IV Access</span></div>
        `;

        // تشارت الأجهزة
        const devValues = [d.foley, d.central, d.ett, d.tt, d.iv];
        if(!devChart) {
            devChart = new Chart(document.getElementById('deviceChart'), {
                type: 'bar',
                data: {
                    labels: ["Foley", "Central", "ETT", "T.T", "IV"],
                    datasets: [{ data: devValues, backgroundColor: '#00f2ff', barThickness: 40 }]
                },
                options: { maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { ticks: { color: '#64748b' } }, x: { ticks: { color: '#fff' } } } }
            });
        } else {
            devChart.data.datasets[0].data = devValues;
            devChart.update();
        }

        // تشارت الـ PDF (Infections)
        if(!infectionChart) {
            infectionChart = new Chart(document.getElementById('pdfChart'), {
                type: 'line',
                data: {
                    labels: pdfData.labels,
                    datasets: [
                        { label: 'CLABSI', data: pdfData.clabsi, borderColor: '#00f2ff', tension: 0.4 },
                        { label: 'CAUTI', data: pdfData.cauti, borderColor: '#bc13fe', tension: 0.4 }
                    ]
                },
                options: { maintainAspectRatio: false, plugins: { legend: { labels: { color: '#fff' } } }, scales: { y: { ticks: { color: '#64748b' } }, x: { ticks: { color: '#64748b' } } } }
            });
        }

        idx = (idx + 1) % deviceWeekly.length;
    }

    update();
    setInterval(update, 15000);
</script>
</body>
</html>
"""

components.html(dashboard_html, height=950, scrolling=False)
