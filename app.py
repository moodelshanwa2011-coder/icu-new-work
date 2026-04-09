import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Mixed Analytics | SGH", layout="wide", initial_sidebar_state="collapsed")

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
            --neon-blue: #00f2ff;
            --neon-green: #39ff14;
            --neon-red: #ff0044;
            --neon-yellow: #fefe33;
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
            background: var(--panel-bg); padding: 8px 25px; border-radius: 8px;
            border: 2px solid var(--neon-blue); margin-bottom: 15px;
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
        }

        .mini-grid {
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 15px;
        }

        .mini-box {
            background: rgba(0, 242, 255, 0.03); border: 1px solid rgba(0, 242, 255, 0.2);
            border-radius: 6px; padding: 12px; text-align: center;
        }

        .mini-val { font-size: 1.8rem; font-weight: 900; color: var(--neon-blue); display: block; }
        .mini-lbl { font-size: 0.65rem; color: #94a3b8; text-transform: uppercase; font-weight: 700; }

        .panel {
            background: var(--panel-bg); border: 1.5px solid var(--neon-blue);
            border-radius: 12px; padding: 20px; height: 65vh;
        }

        .panel-title {
            font-size: 1rem; font-weight: 900; color: var(--neon-blue);
            text-transform: uppercase; letter-spacing: 2px; margin-bottom: 20px;
            border-left: 5px solid var(--neon-blue); padding-left: 12px;
        }
    </style>
</head>
<body>

<div class="header">
    <div style="font-size: 1.4rem; font-weight: 900; letter-spacing: 2px;">ICU <span style="color:var(--neon-blue)">MIXED DATA</span> DASHBOARD</div>
    <div style="background: var(--neon-blue); color: #000; padding: 5px 15px; border-radius: 4px; font-weight: 900;">APRIL 2026 MONITOR</div>
</div>

<div class="mini-grid">
    <div class="mini-box"><span class="mini-val">27.3</span><span class="mini-lbl">Avg. Daily Census</span></div>
    <div class="mini-box"><span class="mini-val">83.8%</span><span class="mini-lbl">RN BSN Education</span></div>
    <div class="mini-box"><span class="mini-val">1.59</span><span class="mini-lbl">Fall Rate (1Q25)</span></div>
    <div class="mini-box" style="border-color: var(--neon-red);"><span class="mini-val" style="color:var(--neon-red)">7</span><span class="mini-lbl">Current Deaths (Apr 25)</span></div>
</div>

<div class="panel">
    <div class="panel-title">Integrated KPI Analytics (Devices vs Clinical vs Mortality)</div>
    <div style="height: 90%;">
        <canvas id="mixedChart"></canvas>
    </div>
</div>

<script>
    const ctx = document.getElementById('mixedChart').getContext('2d');
    
    // دمج البيانات من المصادر الثلاثة:
    // 1. أجهزة أبريل (متوسط يومي)
    // 2. الوفيات (من صورة الجدول) لشهر أبريل
    // 3. العدوى (من ملف PDF) لآخر ربع
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [
                'Foley Catheter (Apr 26)', 
                'Total Ventilators (Apr 26)', 
                'Deaths (Apr 2024)', 
                'Deaths (Apr 2025)', 
                'CLABSI Rate (1Q25)', 
                'CAUTI Rate (1Q25)'
            ],
            datasets: [{
                label: 'Metric Value',
                data: [14.6, 11.5, 5, 7, 1.26, 0.43], // أرقام مستخرجة من صورك وملفك
                backgroundColor: [
                    '#00f2ff', // Foley - Blue
                    '#39ff14', // Vent - Green
                    'rgba(255, 0, 68, 0.5)', // Death 24 - Light Red
                    '#ff0044', // Death 25 - Strong Red
                    '#fefe33', // CLABSI - Yellow
                    '#bc13fe'  // CAUTI - Purple
                ],
                borderColor: '#fff',
                borderWidth: 1,
                borderRadius: 8
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: { backgroundColor: '#0a192f', titleColor: '#00f2ff' }
            },
            scales: {
                y: { 
                    beginAtZero: true,
                    grid: { color: 'rgba(255,255,255,0.05)' },
                    ticks: { color: '#94a3b8' }
                },
                x: {
                    ticks: { color: '#fff', font: { size: 11, weight: 'bold' } }
                }
            }
        }
    });
</script>
</body>
</html>
"""

components.html(dashboard_html, height=850, scrolling=False)
