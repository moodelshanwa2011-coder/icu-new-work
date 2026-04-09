import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Executive Dashboard | SGH", layout="wide", initial_sidebar_state="collapsed")

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
            border: 2px solid var(--neon-blue); margin-bottom: 15px;
            box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
        }

        .main-container {
            display: grid; grid-template-columns: 2.2fr 1.8fr; gap: 15px; height: 85vh;
        }

        .panel {
            background: var(--panel-bg); border: 1.5px solid var(--neon-blue);
            border-radius: 12px; padding: 15px; display: flex; flex-direction: column;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
        }

        .panel-title {
            font-size: 0.85rem; font-weight: 900; color: var(--neon-blue);
            text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px;
            border-left: 5px solid var(--neon-blue); padding-left: 10px;
        }

        /* المربعات الصغيرة المدمجة جداً */
        .mini-grid {
            display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px;
        }

        .mini-box {
            background: rgba(0, 242, 255, 0.03); border: 1px solid rgba(0, 242, 255, 0.2);
            border-radius: 6px; padding: 8px 4px; text-align: center;
        }

        .mini-val { font-size: 1.4rem; font-weight: 900; color: var(--neon-blue); display: block; }
        .mini-lbl { font-size: 0.55rem; color: #94a3b8; text-transform: uppercase; font-weight: 700; }

        #dateLabel {
            background: var(--neon-blue); color: #000; padding: 5px 20px; 
            border-radius: 4px; font-weight: 900; font-size: 1.1rem;
        }
    </style>
</head>
<body>

<div class="header">
    <div style="font-size: 1.4rem; font-weight: 900; letter-spacing: 2px;">ICU <span style="color:var(--neon-blue)">INTEGRATED</span> MONITOR</div>
    <div id="dateLabel">...</div>
</div>

<div class="main-container">
    <div class="panel">
        <div class="panel-title">Medical Device Census (Weekly)</div>
        <div style="flex-grow: 1;">
            <canvas id="deviceChart"></canvas>
        </div>
    </div>
    
    <div class="panel">
        <div class="panel-title">Clinical Indicators Summary</div>
        <div class="mini-grid" id="miniGrid"></div>
        
        <div class="panel-title" style="margin-top:20px; color: var(--neon-purple); border-color: var(--neon-purple);">Infection Rates (CLABSI & CAUTI)</div>
        <div style="flex-grow: 1;">
            <canvas id="infectionChart"></canvas>
        </div>
    </div>
</div>

<script>
    // بيانات من الملف المرفق (NDNQI)
    const clinicalStats = {
        falls: [0, 0.24, 0.24, 0.28, 1.59],
        clabsi: [1.38, 1.28, 1.56, 1.20, 1.26],
        cauti: [0, 0.70, 0.67, 0.40, 0.43],
        bsn: [67.2, 82.9, 82.7, 83.4, 83.8],
        periods: ["4Q23", "1Q24", "2Q24", "3Q24", "1Q25"]
    };

    // بيانات الأجهزة الأسبوعية (مارس وأبريل)
    const weeklyData = [
        {t: "MARCH - W1", total: 45, foley: 30, central: 18, ett: 14, tt: 5, iv: 42, fall: 0},
        {t: "MARCH - W2", total: 48, foley: 32, central: 20, ett: 15, tt: 5, iv: 45, fall: 0.24},
        {t: "APRIL - W1", total: 40, foley: 25, central: 14, ett: 10, tt: 3, iv: 36, fall: 0.28},
        {t: "APRIL - W2", total: 38, foley: 22, central: 12, ett: 9, tt: 3, iv: 34, fall: 1.59}
    ];

    let currentIdx = 0;
    let devChart, infChart;

    function update() {
        const d = weeklyData[currentIdx];
        document.getElementById('dateLabel').innerText = d.t;

        const miniGrid = document.getElementById('miniGrid');
        miniGrid.innerHTML = `
            <div class="mini-box"><span class="mini-val">${d.total}</span><span class="mini-lbl">Census</span></div>
            <div class="mini-box"><span class="mini-val">${d.fall}</span><span class="mini-lbl">Falls Rate</span></div>
            <div class="mini-box"><span class="mini-val">83%</span><span class="mini-lbl">BSN Edu</span></div>
            <div class="mini-box"><span class="mini-val">4.5</span><span class="mini-lbl">Turnover</span></div>
            <div class="mini-box"><span class="mini-val">${d.foley}</span><span class="mini-lbl">Foley</span></div>
            <div class="mini-box"><span class="mini-val">${d.central}</span><span class="mini-lbl">C-Line</span></div>
            <div class="mini-box"><span class="mini-val">${d.ett}</span><span class="mini-lbl">ETT</span></div>
            <div class="mini-box"><span class="mini-val">${d.iv}</span><span class="mini-lbl">IV Acc</span></div>
        `;

        // تشارت الأجهزة
        if(!
