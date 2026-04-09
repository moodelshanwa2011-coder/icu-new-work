import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="ICU Clinical Monitor", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <style>
        :root {
            --bg: #04070a;
            --emerald: #10b981;
            --silver: #e2e8f0;
            --panel: rgba(15, 23, 42, 0.6);
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
            margin-bottom: 50px; text-align: center;
        }

        .date-tag {
            background: var(--emerald); color: #000; padding: 10px 40px;
            border-radius: 50px; font-weight: 900; font-size: 1.6rem;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
        }

        .grid-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 30px;
            width: 85%;
        }

        .stat-circle {
            width: 260px; height: 260px; border-radius: 50%;
            border: 3px solid var(--border);
            background: var(--panel);
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            text-align: center; margin: auto;
            transition: all 0.5s ease;
        }

        .stat-circle:hover { border-color: var(--emerald); transform: scale(1.02); }

        .val { font-size: 5rem; font-weight: 900; color: var(--emerald); line-height: 1; }
        .lbl { font-size: 0.95rem; font-weight: 700; color: var(--silver); margin-top: 12px; max-width: 80%; }
        
        /* تمييز دائرة إجمالي المرضى */
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
        <span class="lbl">Total Patients</span>
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
    // البيانات الفعلية المستخرجة من الصور بدقة
    const dataRecords = [
        {m: "يناير 2024", total: 42, foley: 28, central: 15, ett: 12, tt: 4, iv: 38},
        {m: "فبراير 2024", total: 35, foley: 20, central: 10, ett: 8,
