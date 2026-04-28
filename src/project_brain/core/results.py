from collections import defaultdict

def generate_html(results):

    grouped = defaultdict(list)
    for item in results:
        grouped[item["file"]].append(item)

    sections = ""

    for file, items in grouped.items():
        rows = ""

        for item in items:
            risk = item["risk"] or "unknown"

            if "high" in risk.lower():
                risk_class = "risk-high"
            elif "medium" in risk.lower():
                risk_class = "risk-medium"
            else:
                risk_class = "risk-low"

            rows += f"""
            <div class="function-card">
                <div class="fn-header">
                    <span class="fn-name">{item['function']}</span>
                    <span class="badge {risk_class}">{risk}</span>
                </div>

                <div class="section">
                    <b>Change</b>
                    <p>{item['change']}</p>
                </div>

                <div class="section">
                    <b>Impact</b>
                    <p>{item['impact']}</p>
                </div>

                <div class="section">
                    <b>Risk</b>
                    <p>{item['risk']}</p>
                </div>
            </div>
            """

        sections += f"""
        <div class="file-block">
            <div class="file-header" onclick="toggle(this)">
                📂 {file}
            </div>
            <div class="file-content">
                {rows}
            </div>
        </div>
        """

    return f"""
<html>
<head>
<meta charset="UTF-8">
<title>Project Brain Report</title>

<style>
body {{
    font-family: Inter, Arial;
    background: #0f172a;
    color: #e2e8f0;
    padding: 20px;
}}

h1 {{
    color: #38bdf8;
    margin-bottom: 20px;
}}

.file-block {{
    margin-bottom: 20px;
    border: 1px solid #334155;
    border-radius: 10px;
    overflow: hidden;
}}

.file-header {{
    background: #1e293b;
    padding: 12px;
    cursor: pointer;
    font-weight: bold;
}}

.file-content {{
    display: none;
    padding: 15px;
}}

.function-card {{
    background: #020617;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 12px;
}}

.fn-header {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
}}

.fn-name {{
    font-weight: bold;
    color: #22c55e;
}}

.section {{
    margin-bottom: 8px;
}}

.section p {{
    margin: 4px 0;
    color: #cbd5f5;
}}

.badge {{
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 12px;
}}

.risk-high {{
    background: #dc2626;
}}

.risk-medium {{
    background: #f59e0b;
}}

.risk-low {{
    background: #16a34a;
}}
</style>

<script>
function toggle(el) {{
    let content = el.nextElementSibling;
    content.style.display =
        content.style.display === "block" ? "none" : "block";
}}
</script>

</head>

<body>

<h1>🧠 Project Brain - Diff Analysis</h1>

{sections}

</body>
</html>
"""