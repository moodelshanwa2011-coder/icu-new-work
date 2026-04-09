import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة
st.set_page_config(page_title="ICU PRO MONITORING", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #020617;
            --primary: #00f2ff; /* Ice Blue */
            --secondary: #ffffff; /* Pearl White */
            --panel: rgba(15, 23, 42, 0.95);
            --border: rgba(0, 242, 255, 0.4);
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg);
            background-image: radial-gradient(circle at 50% 50%, rgba(0, 242, 255, 0.05) 0%, transparent 80%);
            color: var(--secondary); margin: 0; padding: 15px; overflow: hidden;
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            background: var(--panel); padding: 20px 45px; border-radius: 15px;
            border: 2px solid var(--primary); margin-bottom: 20px;
            box-shadow: 0 0 30px rgba(0, 242, 255, 0.2);
        }

        .main-grid {
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 20px; margin-bottom: 20px;
        }

        .panel {
            background: var(--panel); border: 2px solid var(--border);
            border-radius: 20px; padding: 25px; backdrop-filter: blur(10px);
            position: relative; overflow: hidden;
        }

        .panel::before {
            content: ''; position: absolute; top: 0; left: 0; width: 5px; height: 100%;
            background: var(--primary);
        }

        .panel-title {
            font-size: 1.1rem; font-weight: 800; color: var(--primary);
            text-transform: uppercase; letter-spacing: 3px; margin-bottom: 20px;
        }

        .box {
            background: rgba(255, 255, 255, 0.02); border: 1.5px solid var(--border);
            border-radius: 15px; padding: 30px 15px; text-align: center;
        }

        .val { font-size: 4.8rem; font-weight: 900; display: block; line-height: 1; color: var(--primary); text-shadow: 0 0 20px rgba(0, 242, 255, 0.3); }
        .lbl { font-size: 1rem; color: var(--secondary); text-transform: uppercase; font-weight: 700; margin-top: 15px; letter-spacing: 1px;}

        .footer { display: grid; grid-template-columns: 2.8fr 1.2fr; gap: 20px; height: 380px; }

        .ring-container { position: relative; width: 220px; height: 220px; margin: auto; }
        .ring-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 4.5rem; font-weight: 900; color: var(--primary); }
        
        .ring-svg { transform: rotate(-90deg); width: 100%; height: 100%; }
        .ring-track { fill: none; stroke: rgba(255,255,255,0.05); stroke-width: 10; } 
        .ring-progress { 
            fill: none; stroke: var(--primary); stroke-width: 10; 
            stroke-dasharray: 283; stroke-dashoffset: 283; 
            stroke-linecap: round; transition: 1.5s ease;
        }
    </style>
</head>
<body>

<div class="header">
    <div style="font-size: 2.5rem; font-weight: 900; letter-spacing: 5px;">ICU <span style="color:var(--primary)">PRO</span> MONITOR</div>
    <div id="timelineLabel" style="background: var(--primary); color: #020617; padding: 10px 40px; border-radius: 40px; font-weight: 900; font-size: 1.3rem;">...</div>
</div>

<div class="main-grid">
    <div class="panel">
        <div class="panel-title">Mortality Index</div>
        <div class="box">
            <span class="val" id="mortVal">0</span>
            <span class="lbl">Patient Deaths</span>
        </div>
    </div>
    <div class="panel" style="grid-column: span 2;">
        <div class="panel-title">Clinical Quality Performance</div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px;">
            <div class="box"><span class="val">1.1</span><span class="lbl">CLABSI Rate</span></div>
            <div class="box"><span class="val">0.7</span><span class="lbl">CAUTI Rate</span></div>
            <div class="box"><span class="val">1.9</span><span class="lbl">VAE Index</span></div>
        </div>
    </div>
    <div class="panel">
        <div class="panel-title">Safety Control</div>
        <div class="box">
            <span class="val">98%</span>
            <span class="lbl">Compliance</span>
        </div>
    </div>
</div>

<div class="footer">
    <div class="panel">
        <div class="panel-title">Operational Achievement Equalizer</div>
        <canvas id="proChart"></canvas>
    </div>
    <div class="panel">
        <div class="panel-title" style="text-align: center;">Unit Health Score</div>
        <div class="ring-container">
            <div id="safetyVal" class="ring-text">0%</div>
            <svg class="ring-svg" viewBox="0 0 100 100">
                <circle class="ring-track" cx="50" cy="50" r="45"></circle>
                <circle id="safetyRing" class="ring-progress" cx="50" cy="50" r="45"></circle>
            </svg>
        </div>
    </div>
</div>

<script>
    // بيانات الوفيات الفعلية من ملفك لسنوات 2023, 2024, 2025
    const dataset = [
        {m: "JAN 23", v: 8}, {m: "FEB 23", v: 4}, {m: "MAR 23", v: 7}, {m: "APR 23", v: 5}, {m: "MAY 23", v: 3}, {m: "JUN 23", v: 8},
        {m: "JUL 23", v: 3}, {m: "AUG 23", v: 4}, {m: "SEP 23", v: 7}, {m: "OCT 23", v: 2}, {m: "NOV 23", v: 3}, {m: "DEC 23", v: 4},
        {m: "JAN 24", v: 8}, {m: "FEB 24", v: 4}, {m: "MAR 24", v: 7}, {m: "APR 24", v: 5}, {m: "MAY 24", v: 3}, {m: "JUN 24", v: 8},
        {m: "JUL 25", v: 2}, {m: "AUG 25", v: 8}, {m: "SEP 25", v: 2}, {m: "OCT 25", v: 1}, {m: "NOV 25", v: 3}, {m: "DEC 25", v: 6}
    ];
    
    let idx = 0;
    let chart;

    function refresh() {
        const current = dataset[idx];
        document.getElementById('timelineLabel').innerText = current.m;
        document.getElementById('mortVal').innerText = current.v;
        
        // حساب مجموعي للسكور
        const score = Math.max(70, 100 - (current.v * 3.5));
        document.getElementById('safetyVal').innerText = Math.round(score) + "%";
        document.getElementById('safetyRing').style.strokeDashoffset = 283 - (283 * score / 100);

        const chartData = [current.v * 1.5, 6, 8, 5, 9];

        if(!chart) {
            const ctx = document.getElementById('proChart').getContext('2d');
            chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['MORTALITY', 'INFECTION', 'VAE', 'SAFETY', 'COMPLIANCE'],
                    datasets: [{
                        data: chartData,
                        backgroundColor: '#00f2ff',
                        borderRadius: 5,
                        barThickness: 50
                    }]
                },
                options: {
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { display: false },
                        x: { ticks: { color: '#ffffff', font: { weight: 'bold', size: 12 } }, grid: { display: false } }
                    }
                },
                plugins: [{
                    id: 'eqLines',
                    afterDraw: (c) => {
                        const { ctx } = c; ctx.save();
                        ctx.strokeStyle = '#020617'; ctx.lineWidth = 4;
                        c.getDatasetMeta(0).data.forEach(bar => {
                            for(let y = bar.base; y > bar.y; y -= 12) {
                                ctx.beginPath(); ctx.moveTo(bar.x - bar.width/2, y);
                                ctx.lineTo(bar.x + bar.width/2, y); ctx.stroke();
                            }
                        });
                        ctx.restore();
                    }
                }]
            });
        } else {
            chart.data.datasets[0].data = chartData;
            chart.update('none');
        }
        idx = (idx + 1) % dataset.length;
    }

    setInterval(refresh, 3500);
    refresh();
</script>
</body>
</html>
"""

components.html(dashboard_html, height=1000, scrolling=False)
