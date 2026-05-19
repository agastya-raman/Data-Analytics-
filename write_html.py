html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LangGraph Analytics</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e0e0e0; min-height: 100vh; }
        .header { background: linear-gradient(135deg, #1a1a2e, #16213e); padding: 30px; text-align: center; border-bottom: 2px solid #0f3460; }
        .header h1 { font-size: 2.5rem; color: #00d4ff; margin-bottom: 8px; }
        .header p { color: #888; font-size: 1rem; }
        .container { max-width: 1200px; margin: 0 auto; padding: 30px 20px; }
        .upload-section { background: #1a1a2e; border: 2px dashed #0f3460; border-radius: 16px; padding: 50px; text-align: center; margin-bottom: 30px; }
        .upload-section h2 { color: #00d4ff; margin-bottom: 15px; font-size: 1.5rem; }
        .upload-section p { color: #888; margin-bottom: 25px; }
        input[type="file"] { display: none; }
        .file-label { background: #0f3460; color: #00d4ff; padding: 12px 30px; border-radius: 8px; cursor: pointer; font-size: 1rem; border: 1px solid #00d4ff; }
        .file-name { display: block; margin-top: 10px; color: #888; font-size: 0.9rem; }
        .analyze-btn { display: block; width: 100%; max-width: 300px; margin: 15px auto 0; padding: 15px; background: linear-gradient(135deg, #00d4ff, #0f3460); color: white; border: none; border-radius: 10px; font-size: 1.1rem; cursor: pointer; }
        .analyze-btn:disabled { opacity: 0.5; cursor: not-allowed; }
        .progress-section { display: none; background: #1a1a2e; border-radius: 16px; padding: 30px; margin-bottom: 30px; }
        .progress-section h2 { color: #00d4ff; margin-bottom: 20px; }
        .agent-step { display: flex; align-items: flex-start; gap: 15px; padding: 15px; margin-bottom: 10px; background: #0f1117; border-radius: 10px; border-left: 3px solid #0f3460; }
        .agent-step.success { border-left-color: #00ff88; }
        .agent-step.error { border-left-color: #ff4444; }
        .agent-step.loading { border-left-color: #ffaa00; }
        .agent-icon { font-size: 1.5rem; }
        .agent-name { font-weight: bold; color: #00d4ff; font-size: 1rem; }
        .agent-msg { color: #aaa; font-size: 0.85rem; margin-top: 4px; }
        .agent-error { color: #ff4444; font-size: 0.85rem; margin-top: 4px; }
        .loading-spinner { display: inline-block; width: 20px; height: 20px; border: 2px solid #0f3460; border-top-color: #00d4ff; border-radius: 50%; animation: spin 0.8s linear infinite; }
        @keyframes spin { to { transform: rotate(360deg); } }
        .results-section { display: none; }
        .tabs { display: flex; gap: 10px; margin-bottom: 20px; }
        .tab-btn { padding: 10px 25px; background: #1a1a2e; border: 1px solid #0f3460; border-radius: 8px; color: #888; cursor: pointer; font-size: 0.95rem; }
        .tab-btn.active { background: #0f3460; color: #00d4ff; border-color: #00d4ff; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        .report-box { background: #1a1a2e; border-radius: 16px; padding: 30px; white-space: pre-wrap; line-height: 1.7; color: #ddd; max-height: 600px; overflow-y: auto; }
        .charts-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(350px, 1fr)); gap: 20px; }
        .chart-card { background: #1a1a2e; border-radius: 12px; overflow: hidden; border: 1px solid #0f3460; }
        .chart-card img { width: 100%; height: 250px; object-fit: contain; background: white; padding: 10px; }
        .chart-card p { padding: 10px 15px; font-size: 0.85rem; color: #888; text-align: center; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 15px; margin-bottom: 25px; }
        .stat-card { background: #1a1a2e; border-radius: 12px; padding: 20px; text-align: center; border: 1px solid #0f3460; }
        .stat-number { font-size: 2rem; color: #00d4ff; font-weight: bold; }
        .stat-label { color: #888; font-size: 0.85rem; margin-top: 5px; }
        .download-btn { display: inline-block; padding: 10px 20px; background: #0f3460; color: #00d4ff; border: 1px solid #00d4ff; border-radius: 8px; cursor: pointer; font-size: 0.9rem; text-decoration: none; margin-top: 15px; }
    </style>
</head>
<body>
<div class="header">
    <h1>LangGraph Analytics</h1>
    <p>7-Agent AI Pipeline - Upload CSV and Get Full Analysis</p>
</div>
<div class="container">
    <div class="upload-section">
        <h2>Upload Your Dataset</h2>
        <p>Supports any CSV file. The AI will profile, clean, analyze and report automatically.</p>
        <label class="file-label" for="fileInput">Choose CSV File</label>
        <input type="file" id="fileInput" accept=".csv">
        <span class="file-name" id="fileName">No file chosen</span>
        <br><br>
        <button class="analyze-btn" id="analyzeBtn" onclick="runAnalysis()">Run Analysis</button>
    </div>
    <div class="progress-section" id="progressSection">
        <h2>Pipeline Running...</h2>
        <div id="agentSteps"></div>
    </div>
    <div class="results-section" id="resultsSection">
        <div class="stats-grid" id="statsGrid"></div>
        <div class="tabs">
            <button class="tab-btn active" onclick="showTab('report', event)">Report</button>
            <button class="tab-btn" onclick="showTab('charts', event)">Charts</button>
            <button class="tab-btn" onclick="showTab('agents', event)">Agent Log</button>
        </div>
        <div class="tab-content active" id="tab-report">
            <div class="report-box" id="reportBox"></div>
            <a href="/report" download="report.md" class="download-btn">Download Report</a>
        </div>
        <div class="tab-content" id="tab-charts">
            <div class="charts-grid" id="chartsGrid"></div>
        </div>
        <div class="tab-content" id="tab-agents">
            <div id="agentLogFull"></div>
        </div>
    </div>
</div>
<script>
    document.getElementById('fileInput').addEventListener('change', function() {
        document.getElementById('fileName').textContent = this.files[0] ? this.files[0].name : 'No file chosen';
    });
    function showTab(tab, event) {
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        document.getElementById('tab-' + tab).classList.add('active');
        event.target.classList.add('active');
    }
    const agentIcons = { 'PROFILER':'🔍','QUALITY':'⚠️','CLEANING':'🧹','EDA':'📈','CRITIC':'🎯','VISUALIZATION':'📊','REPORTER':'📝' };
    function addStep(agent, message, errors, status) {
        const icon = agentIcons[agent] || '⚙️';
        const div = document.createElement('div');
        div.className = 'agent-step ' + status;
        div.innerHTML = '<div class="agent-icon">' + (status === 'loading' ? '<div class="loading-spinner"></div>' : icon) + '</div><div class="agent-info"><div class="agent-name">' + agent + '</div>' + (message ? '<div class="agent-msg">' + message + '</div>' : '') + errors.map(e => '<div class="agent-error">ERROR: ' + e + '</div>').join('') + '</div>';
        document.getElementById('agentSteps').appendChild(div);
        div.scrollIntoView({ behavior: 'smooth' });
    }
    async function runAnalysis() {
        const fileInput = document.getElementById('fileInput');
        if (!fileInput.files[0]) { alert('Please choose a CSV file first!'); return; }
        document.getElementById('progressSection').style.display = 'block';
        document.getElementById('resultsSection').style.display = 'none';
        document.getElementById('agentSteps').innerHTML = '';
        document.getElementById('analyzeBtn').disabled = true;
        document.getElementById('analyzeBtn').textContent = 'Analyzing... (3-5 mins)';
        addStep('PIPELINE', 'Starting AI agents...', [], 'loading');
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);
        try {
            const response = await fetch('/analyze', { method: 'POST', body: formData });
            const data = await response.json();
            document.getElementById('agentSteps').innerHTML = '';
            data.steps.forEach(step => {
                addStep(step.agent, step.messages.join(' | '), step.errors, step.errors.length > 0 ? 'error' : 'success');
            });
            showResults(data);
        } catch(err) {
            addStep('ERROR', 'Something went wrong: ' + err.message, [], 'error');
        }
        document.getElementById('analyzeBtn').disabled = false;
        document.getElementById('analyzeBtn').textContent = 'Run Analysis';
    }
    function showResults(data) {
        document.getElementById('resultsSection').style.display = 'block';
        const findings = data.steps.filter(s => s.agent === 'EDA').length;
        document.getElementById('statsGrid').innerHTML =
            '<div class="stat-card"><div class="stat-number">' + data.steps.length + '</div><div class="stat-label">Agents Run</div></div>' +
            '<div class="stat-card"><div class="stat-number">' + findings + '</div><div class="stat-label">Hypotheses Tested</div></div>' +
            '<div class="stat-card"><div class="stat-number">' + data.charts.length + '</div><div class="stat-label">Charts Generated</div></div>' +
            '<div class="stat-card"><div class="stat-number">' + data.steps.filter(s => s.errors.length > 0).length + '</div><div class="stat-label">Errors</div></div>';
        document.getElementById('reportBox').textContent = data.report;
        const grid = document.getElementById('chartsGrid');
        grid.innerHTML = '';
        data.charts.forEach(chart => {
            grid.innerHTML += '<div class="chart-card"><img src="/charts/' + chart + '" alt="' + chart + '"><p>' + chart.replace('.png','').replace(/_/g,' ') + '</p></div>';
        });
        const log = document.getElementById('agentLogFull');
        log.innerHTML = '';
        data.steps.forEach(step => {
            const icon = agentIcons[step.agent] || '⚙️';
            log.innerHTML += '<div class="agent-step ' + (step.errors.length ? 'error' : 'success') + '"><div class="agent-icon">' + icon + '</div><div class="agent-info"><div class="agent-name">' + step.agent + ' to ' + step.phase + '</div>' + step.messages.map(m => '<div class="agent-msg">' + m + '</div>').join('') + step.errors.map(e => '<div class="agent-error">' + e + '</div>').join('') + step.charts.map(c => '<div class="agent-msg">Chart: ' + c + '</div>').join('') + '</div></div>';
        });
        document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
    }
</script>
</body>
</html>"""

with open("templates/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("templates/index.html written successfully!")