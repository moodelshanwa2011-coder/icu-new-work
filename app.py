import streamlit as st
import streamlit.components.v1 as components

# إعداد الصفحة لتكون بملء الشاشة وإخفاء القائمة الجانبية
st.set_page_config(page_title="شاشة مراقبة المؤشرات الإكلينيكية", layout="wide", initial_sidebar_state="collapsed")

dashboard_html = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #050a09; /* كربوني داكن جداً */
            --emerald: #00f2a1; /* أخضر زمردي مشع */
            --white: #ffffff;
            --panel: rgba(10, 20, 19, 0.9); /* لوحة كربونية */
            --border: rgba(0, 242, 161, 0.3); /* حدود زمردية شفافة */
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg);
            background-image: radial-gradient(circle at 50% 50%, rgba(0, 242, 161, 0.05) 0%, transparent 80%);
            color: var(--white); margin: 0; padding: 20px; overflow: hidden;
        }

        .header {
            display: flex; justify-content: space-between; align-items: center;
            background: var(--panel); padding: 15px 50px; border-radius: 50px;
            border: 2px solid var(--emerald); margin-bottom: 25px;
            box-shadow: 0 0 30px rgba(0, 242, 161, 0.2);
        }

        .circles-grid {
            display: grid; grid-template-columns: repeat(4, 1fr);
            gap: 25px; margin-bottom: 25px; align-items: center;
        }

        .circle-panel {
            background: var(--panel); border: 3px solid var(--border);
            border-radius: 50%; width: 280px; height: 280px;
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            backdrop-filter: blur(10px); margin: auto;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3), inset 0 0 15px rgba(0, 242, 161, 0.1);
            transition: all 0.5s ease;
        }

        .circle-panel.large { width: 350px; height: 350px; grid-column: span 2; }

        .circle-title {
            font-size: 1.1rem; font-weight: 800; color: var(--emerald);
            text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px;
        }

        .val { font-size: 6rem; font-weight: 900; line-height: 1; color: var(--emerald); text-shadow: 0 0 20px rgba(0, 242, 161, 0.5); }
        .large .val { font-size: 8rem; }
        .lbl { font-size: 1.1rem; color: var(--white); font-weight: 700; margin-top: 10px; }

        .footer-grid { display: grid; grid-template-columns: 2.5fr 1.5fr; gap: 25px; height: 350px; }

        .chart-panel {
            background: var(--panel); border: 3px solid var(--border);
            border-radius: 30px; padding: 25px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        }

        .chart-title { font-size: 1.3rem; font-weight: 800; color: var(--emerald); margin-bottom: 15px; text-align: right; }

        .ring-container { position: relative; width: 280px; height: 280px; margin: auto; }
        .ring-text { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 5rem; font-weight: 900; color: var(--emerald); }
        
        .ring-svg { transform: rotate(-90deg); width: 100%; height: 100%; }
        .ring-track { fill: none; stroke: rgba(255,255,255,0.05); stroke-width: 10; } 
        .ring-progress { 
            fill: none; stroke: var(--emerald); stroke-width: 10; 
            stroke-dasharray: 283; stroke-dashoffset: 283; 
            stroke-linecap: round; transition: 1.5s ease-out;
        }
    </style>
</head>
<body>

<div class="header">
    <div style="font-size: 2.2rem; font-weight: 900; letter-spacing: 1px;">شاشة مراقبة <span style="color:var(--emerald)">المؤشرات الإكلينيكية</span></div>
    <div id="dateLabel" style="background: var(--emerald); color: #000; padding: 10px 45px; border-radius: 50px; font-weight: 900; font-size: 1.5rem;">...</div>
</div>

<div class="circles-grid">
    <div class="circle-panel">
        <div class="circle-title">إحصائيات الوفيات</div>
        <span class="val" id="mortVal">0</span>
        <span class="lbl">عدد الوفيات</span>
    </div>
    
    <div class="circle-panel large">
        <div class="circle-title">مؤشرات جودة الرعاية</div>
        <div style="display: flex; gap: 20px; align-items: center; justify-content: center;">
            <div style="text-align:center;"><span class="val">1.1</span><span class="lbl">عدوى الدم</span></div>
            <div style="text-align:center;"><span class="val">0.7</span><span class="lbl">عدوى البول</span></div>
            <div style="text-align:center;"><span class="val">1.5</span><span class="lbl">عدوى التنفس</span></div>
        </div>
    </div>
    
    <div class="circle-panel">
        <div class="circle-title">كفاءة القسم</div>
        <span class="val">96%</span>
        <span class="lbl">نسبة الالتزام</span>
    </div>
</div>

<div class="footer-grid">
    <div class="chart-panel">
        <div class="chart-title">تحليل الأداء الديناميكي (عدد الوفيات مقابل الهدف)</div>
        <canvas id="emeraldChart"></canvas>
    </div>
    
    <div class="circle-panel" style="width: 350px; height: 350px;">
        <div class="circle-title">مؤشر أمان الوحدة</div>
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
    // البيانات الفعلية من ملفك الخاص
    const months = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر"];
    const data2023 = [8, 4, 7, 5, 3, 8, 3, 4, 7, 2, 3, 4];
    const data2024 = [8, 4, 7, 5, 3, 8, 3, 4, 7, 2, 3, 4]; // نفس بيانات 23 حسب الملف
    const data2025 = [6, 3, 7, 7, 1, 6, 2, 8, 2, 1, 3, 6];

    // تجميع البيانات في مصفوفة زمنية واحدة
    const timeline = [
        ...data2023.map((v, i) => ({ date: months[i] + " 2023", val: v })),
        ...data2024.map((v, i) => ({ date: months[i] + " 2024", val: v })),
        ...data2025.map((v, i) => ({ date: months[i] + " 2025", val: v }))
    ];

    let idx = 0;
    let chart;

    function refresh() {
        const current = timeline[idx];
        document.getElementById('dateLabel').innerText = current.date;
        document.getElementById('mortVal').innerText = current.val;
        
        // حساب نسبة الأمان (معادلة عكسية مع عدد الوفيات)
        const safetyScore = Math.max(65, 100 - (current.val * 4));
        document.getElementById('safetyVal').innerText = Math.round(safetyScore) + "%";
        document.getElementById('safetyRing').style.strokeDashoffset = 283 - (283 * safetyScore / 100);

        // تحديث الرسم البياني
        if(!chart) {
            const ctx = document.getElementById('emeraldChart').getContext('2d');
            chart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['الوفيات', 'العدوى', 'التنفس', 'الالتزام', 'القوى العاملة'],
                    datasets: [{
                        data: [current.val, 5, 8, 4, 7],
                        backgroundColor: '#00f2a1', // زمردي مشع
                        borderRadius: 10,
                        barThickness: 50
                    }]
                },
                options: {
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { display: false },
                        x: { 
                            ticks: { color: '#ffffff', font: { weight: 'bold', size: 14 } },
                            grid: { display: false }
                        }
                    }
                }
            });
        } else {
            // تحديث قيمة الوفيات فقط في الرسم البياني
            chart.data.datasets[0].data[0] = current.val;
            chart.update('none'); // تحديث بدون حركة لإعطاء إحساس بالسرعة
        }
        idx = (idx + 1) % timeline.length;
    }

    // تحديث البيانات كل 3 ثوانٍ
    setInterval(refresh, 3000);
    refresh(); // التحديث الأولي
</script>
</body>
</html>
"""

components.html(dashboard_html, height=1050, scrolling=False)
