import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون بملء الشاشة
st.set_page_config(
    page_title="ICU Clinical | Weekly Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #020617;
            --card-bg: rgba(15, 23, 42, 0.8);
            --neon-emerald: #10b981;
            --neon-blue: #22d3ee;
            --border-clr: rgba(255, 255, 255, 0.1);
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
        }
        
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            margin: 0;
            padding: 25px;
            overflow: hidden;
        }

        .dashboard-container { max-width: 1580px; margin: 0 auto; }

        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--card-bg);
            backdrop-filter: blur(20px);
            padding: 20px 45px;
            border-radius: 20px;
            border: 1px solid var(--border-clr);
            margin-bottom: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }

        .q-badge {
            background: linear-gradient(135deg, #059669, #10b981);
            color: #020617;
            padding: 10px 35px;
            border-radius: 12px;
            font-weight: 900;
            font-size: 1.4rem;
            box-shadow: 0 0 20px rgba(16, 185, 129, 0.3);
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 25px;
        }

        .kpi-card {
            background: var(--card-bg);
            border-radius: 22px;
            padding: 25px;
            text-align: center;
            border: 2px solid var(--border-clr);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .kpi-card:hover {
            transform: translateY(-5px);
            border-color: var(--neon-emerald);
            background: rgba(16, 185, 129, 0.03);
        }

        .kpi-title { 
            font-size: 0.9rem; 
            font-weight: 700; 
            color: var(--text-dim); 
            text-transform: uppercase; 
            margin-bottom: 10px;
            letter-spacing: 1px;
        }

        .val-large {
            font-size: 5rem;
            font-weight: 900;
            line-height: 1;
            color: var(--neon-emerald);
            text-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
        }

        .total-node { border-color: #fff; }
        .total-node .val-large { color: #fff; text-shadow: none; }

        .bottom-section {
            display: grid;
            grid-template-columns: 2fr 1.1fr;
            gap: 25px;
            height: 350px;
        }

        .glass-panel {
            background: var(--card-bg);
            border-radius: 25px;
            padding: 25px;
            border: 1px solid var(--border-clr);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .score-circle {
            width: 180px;
            height: 180px;
            border-radius: 50%;
            border: 10px solid var(--neon-emerald);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 30px rgba(16, 185, 129, 0.2);
        }

        .score-num { font-size: 3.5rem; font-weight: 900; color: var(--neon-emerald); }
        .score-txt { font-size: 1rem; font-weight: 700; color: var(--text-dim); margin-top: 15px; }

        .fade-in { animation: fadeIn 0.8s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; transform: scale(0.98); } to { opacity: 1; transform: scale(1); } }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="header">
            <div>
                <h1 style="margin:0; font-size:1.6rem; letter-spacing:1px;">ICU <span style="color:var(--neon-emerald)">DEVICE UTILIZATION</span></h1>
                <p style="margin:5px 0 0 0; color:var(--text-dim); font-weight:600;">PATIENT LOAD MONITORING</p>
            </div>
            <div class="q-badge" id="weekLabel">MARCH - WEEK 1</div>
        </div>

        <div class="grid" id="kpiGrid">
            </div>

        <div class="bottom-section">
            <div class="glass-panel">
                <canvas id="deviceChart"></canvas>
            </div>
            <div class="glass-panel">
                <div class="score-circle">
                    <div class="score-num" id="totalPtVal">0</div>
                </div>
                <div class="score-txt">TOTAL PATIENTS</div>
                <p style="color:#475569; font-size:0.75rem; margin-top:10px;">Current Week Census</p>
            </div>
        </div>
    </div>

    <script>
        // البيانات الأسبوعية لشهر مارس وأبريل
        const weeklyData = [
            {t: "MARCH - Week 1", total: 45, devices: [30, 18, 14, 5, 42]},
            {t: "MARCH - Week 2", total: 48, devices: [32, 20, 15, 5, 45]},
            {t: "MARCH - Week 3", total: 42, devices: [28, 16, 12, 4, 40]},
            {t: "MARCH - Week 4", total: 44, devices: [29, 17, 13, 4, 41]},
            {t: "APRIL - Week 1", total: 40, devices: [25, 14, 10, 3, 36]},
            {t: "APRIL - Week 2", total: 38, devices: [22, 12, 9, 3, 34]},
            {t: "APRIL - Week 3", total: 41, devices: [26, 15, 11, 4, 37]},
            {t: "APRIL - Week 4", total: 39, devices: [24, 13, 10, 3, 35]}
        ];

        const labels = ["Foley Cath", "Central Line", "ETT", "T.T", "IV Access"];
        let step = 0; 
        let barChart;

        function update() {
            const data = weeklyData[step];
            document.getElementById('weekLabel').innerText = data.t;
            document.getElementById('totalPtVal').innerText = data.total;
            
            const grid = document.getElementById('kpiGrid');
            grid.innerHTML = '';
            grid.classList.remove('fade-in');
            void grid.offsetWidth;
            grid.classList.add('fade-in');

            // إضافة الكروت الستة (5 أجهزة + 1 إجمالي المرضى)
            labels.forEach((label, i) => {
                grid.innerHTML += `
                    <div class="kpi-card">
                        <div class="kpi-title">Number of Pt with<br>${label}</div>
                        <div class="val-large">${data.devices[i]}</div>
                    </div>`;
            });
            
            // إضافة كرت إجمالي المرضى في الشبكة أيضاً
            grid.innerHTML += `
                <div class="kpi-card total-node">
                    <div class="kpi-title">TOTAL<br>PATIENTS</div>
                    <div class="val-large">${data.total}</div>
                </div>`;

            if(!barChart) {
                const ctx = document.getElementById('deviceChart').getContext('2d');
                barChart = new Chart(ctx, {
                    type: 'bar',
                    data: { 
                        labels: labels, 
                        datasets: [{ 
                            label: 'Device Utilization',
                            data: data.devices, 
                            backgroundColor: '#10b981', 
                            borderRadius: 8,
                            barThickness: 35
                        }] 
                    },
                    options: { 
                        maintainAspectRatio: false, 
                        plugins: { legend: { display: false } },
                        scales: { 
                            y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8' } },
                            x: { ticks: { color: '#f8fafc', font: { weight: 'bold' } } }
                        }
                    }
                });
            } else {
                barChart.data.datasets[0].data = data.devices;
                barChart.update();
            }

            step = (step + 1) % weeklyData.length;
        }

        update(); 
        setInterval(update, 15000); // التحديث كل 15 ثانية
    </script>
</body>
</html>
"""

components.html(dashboard_html, height=1000, scrolling=False)
