import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Advanced Monitor | SGH", layout="wide", initial_sidebar_state="collapsed")

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
            --grid-line: rgba(0, 242, 255, 0.1);
            --border-glow: #00f2ff;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            background-image: 
                linear-gradient(var(--grid-line) 2px, transparent 2px),
                linear-gradient(90deg, var(--grid-line) 2px, transparent 2px);
            background-size: 50px 50px;
            color: #fff; margin: 0; padding: 15px; overflow: hidden;
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            background: var(--panel-bg); padding: 15px 40px; border-radius: 12px;
            border: 3px solid var(--safe-blue); margin-bottom: 20px;
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
        }

        .main-container {
            display: grid; grid-template-columns: 2.5fr 1.5fr; gap: 20px; height: 80vh;
        }

        .panel {
            background: var(--panel-bg); border: 2px solid var(--border-glow);
            border-radius: 15px; padding: 25px; backdrop-filter: blur(10px);
            display: flex; flex-direction: column;
            box-shadow: 0 0 10px rgba(0, 242, 255, 0.1);
        }

        .panel-title {
            font-size: 1.1rem; font-weight: 900; color: var(--safe-blue);
            text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px;
            border-left: 8px solid var(--safe-blue); padding-left: 15px;
        }

        /* تنسيق المربعات الصغيرة بدل الدائرة */
        .mini-grid {
            display: grid; grid-template-columns: 1fr 1fr; gap: 12px; width: 100%;
        }

        .mini-box {
            background: rgba(0, 242, 255, 0.05); border: 1.5px solid rgba(0, 242, 255, 0.4);
            border-radius: 10px; padding: 15px; text-align: center;
        }

        .mini-val { font-size: 2.2rem; font-weight: 900; color: var(--safe-blue); display: block; }
        .mini-lbl { font-size: 0.7rem; color: #cbd5e1; text-transform: uppercase; font-weight: 700; }

        .total-box {
            grid-column: span 2; background: rgba(255, 255, 255, 0.1); border-color: #fff;
        }
        .total-box .mini-val { color: #fff; font-size: 3rem; }

        #dateLabel {
            background: var(--safe-blue); color: #000; padding: 8px 30px; 
            border-radius: 8px; font-weight: 900; font-size: 1.3rem;
        }
    </style>
</head>
<body>

<div class="header">
    <div style="font-size: 1.8rem; font-weight: 900; letter-spacing: 3px;">ICU <span style="color:var(--safe-blue)">DEVICE MONITOR</span> 2026</div>
    <div id="dateLabel">...</div>
</div>

<div class="main-container">
    <div class="panel">
        <div class="panel-title">Device Utilization Analytics</div>
        <div style="flex-grow: 1; position: relative;">
            <canvas id="deviceChart"></canvas>
        </div>
    </div>
    
    <div class="panel">
        <div class="panel-title">Current Census Summary</div>
        <div class="mini-grid" id="miniGrid">
            </div>
    </div>
</div>

<script>
    const weeklyData = [
        {t: "MARCH - Week 1", total: 45, foley: 30, central: 18, ett: 14, tt: 5, iv: 42},
        {t: "MARCH - Week 2", total: 48, foley: 32, central: 20, ett: 15, tt: 5, iv: 45},
        {t: "MARCH - Week 3", total: 42, foley: 28, central: 16, ett: 12, tt: 4, iv: 40},
        {t: "MARCH - Week 4", total: 44, foley: 29, central: 17, ett: 13, tt: 4, iv: 41},
        {t: "APRIL - Week 1", total: 40, foley: 25, central: 14, ett: 10, tt: 3, iv: 36},
        {t: "APRIL - Week 2", total: 38, foley: 22, central: 12, ett: 9, tt: 3, iv: 34},
        {t: "APRIL - Week 3", total: 41, foley: 26, central: 15, ett: 11, tt: 4, iv: 37},
        {t: "APRIL - Week 4", total: 39, foley: 24, central: 13, ett: 10, tt: 3, iv: 35}
    ];

    let currentIdx = 0;
    let myChart;

    function updateDashboard() {
        const d = weeklyData[currentIdx];
        document.getElementById('dateLabel').innerText = d.t;

        // تحديث المربعات الصغيرة
        const miniGrid = document.getElementById('miniGrid');
        miniGrid.innerHTML = `
            <div class="mini-box total-box">
                <span class="mini-val">${d.total}</span>
                <span class="mini-lbl">Total Patients</span>
            </div>
            <div class="mini-box">
                <span class="mini-val">${d.foley}</span>
                <span class="mini-lbl">Foley Cath</span>
            </div>
            <div class="mini-box">
                <span class="mini-val">${d.central}</span>
                <span class="mini-lbl">Central Line</span>
            </div>
            <div class="mini-box">
                <span class="mini-val">${d.ett}</span>
                <span class="mini-lbl">ETT</span>
            </div>
            <div class="mini-box">
                <span class="mini-val">${d.tt}</span>
                <span class="mini-lbl">T.T</span>
            </div>
            <div class="mini-box" style="grid-column: span 2;">
                <span class="mini-val">${d.iv}</span>
                <span class="mini-lbl">IV Access</span>
            </div>
        `;

        // تحديث البار تشارت
        const chartData = [d.foley, d.central, d.ett, d.tt, d.iv];
        if(!myChart) {
            const ctx = document.getElementById('deviceChart').getContext('2d');
            myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ["Foley", "Central", "ETT", "T.T", "IV"],
                    datasets: [{
                        label: 'Patients Count',
                        data: chartData,
                        backgroundColor: '#00f2ff',
                        borderRadius: 5,
                        barThickness: 45
                    }]
                },
                options: {
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                        x: { ticks: { color: '#fff', font: { weight: 'bold' } } }
                    }
                }
            });
        } else {
            myChart.data.datasets[0].data = chartData;
            myChart.update();
        }

        currentIdx = (currentIdx + 1) % weeklyData.length;
    }

    updateDashboard();
    setInterval(updateDashboard, 15000); // تحديث كل 15 ثانية
</script>
</body>
</html>
"""

components.html(dashboard_html, height=900, scrolling=False)
