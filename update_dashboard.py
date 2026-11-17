import os
import json
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def read_csv(filename):
    path = os.path.join(BASE_DIR, filename)
    rows = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                rows.append(r)
    return rows

def generate_html_dashboard():
    results = read_csv("results.csv")
    payable = read_csv("payable.csv")
    review = read_csv("review.csv")
    summary_path = os.path.join(BASE_DIR, "summary.txt")
    summary_text = ""
    if os.path.exists(summary_path):
        with open(summary_path, "r", encoding="utf-8") as f:
            summary_text = f.read()

    status_counts = {}
    for r in results:
        st = r.get("status", "unknown")
        status_counts[st] = status_counts.get(st, 0) + 1

    data = {
        "results": results,
        "payable": payable,
        "review": review,
        "summary_text": summary_text,
        "status_counts": status_counts
    }

    # Generate clean HTML
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>College Club Expense Claim Checker - Dashboard</title>
<style>
  :root {{ --bg-primary: #0f172a; --bg-card: #1e293b; --text-primary: #f8fafc; --text-muted: #94a3b8; --accent: #38bdf8; --success: #22c55e; --warning: #f59e0b; --danger: #ef4444; --border: #334155; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }}
  body {{ background-color: var(--bg-primary); color: var(--text-primary); padding: 24px; }}
  .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 16px; margin-bottom: 24px; }}
  .header h1 {{ font-size: 24px; color: var(--accent); }}
  .badge {{ background: #0369a1; color: #e0f2fe; padding: 5px 12px; border-radius: 9999px; font-size: 13px; font-weight: 600; }}
  .tabs {{ display: flex; gap: 8px; margin-bottom: 20px; border-bottom: 1px solid var(--border); }}
  .tab-btn {{ background: none; border: none; color: var(--text-muted); font-size: 15px; font-weight: 600; padding: 10px 18px; cursor: pointer; border-bottom: 2px solid transparent; }}
  .tab-btn.active {{ color: var(--accent); border-bottom-color: var(--accent); }}
  .tab-content {{ display: none; }}
  .tab-content.active {{ display: block; }}
  .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin-bottom: 24px; }}
  .metric-card {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 18px; }}
  .metric-label {{ font-size: 13px; color: var(--text-muted); margin-bottom: 8px; }}
  .metric-val {{ font-size: 28px; font-weight: 700; }}
  .table-container {{ background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; overflow: hidden; margin-top: 16px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 14px; text-align: left; }}
  th {{ background: #182234; color: var(--text-muted); padding: 12px 14px; border-bottom: 1px solid var(--border); font-weight: 600; }}
  td {{ padding: 12px 14px; border-bottom: 1px solid var(--border); }}
  .status-tag {{ padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 700; text-transform: uppercase; }}
  .tag-ok_to_pay {{ background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid #22c55e; }}
  .tag-needs_bill {{ background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid #f59e0b; }}
  .tag-needs_approval {{ background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid #ef4444; }}
  .tag-over_budget {{ background: rgba(217, 70, 239, 0.2); color: #e879f9; border: 1px solid #d946ef; }}
  .tag-needs_more_info {{ background: rgba(148, 163, 184, 0.2); color: #cbd5e1; border: 1px solid #94a3b8; }}
  pre {{ background: #182234; border: 1px solid var(--border); border-radius: 6px; padding: 16px; overflow-x: auto; color: #38bdf8; font-family: monospace; font-size: 13px; line-height: 1.5; }}
</style>
</head>
<body>
<div class="header">
  <div>
    <h1>🎓 College Club Expense Claim Checker</h1>
    <p style="color: var(--text-muted); font-size: 13px; margin-top: 4px;">CIT AI-Native Engineering Capstone · Automated Audit Triage Dashboard</p>
  </div>
  <span class="badge">Faculty Treasurer Checkpoint</span>
</div>

<div class="tabs">
  <button class="tab-btn active" onclick="switchTab('tab-audit')">📊 Audit Run (22 Claims)</button>
  <button class="tab-btn" onclick="switchTab('tab-payable')">🟢 Payable Claims ({len(payable)})</button>
  <button class="tab-btn" onclick="switchTab('tab-review')">🔴 Flagged For Review ({len(review)})</button>
  <button class="tab-btn" onclick="switchTab('tab-summary')">📑 Official Summary Report</button>
</div>

<div id="tab-audit" class="tab-content active">
  <div class="metrics-grid">
    <div class="metric-card"><div class="metric-label">Total Claims</div><div class="metric-val">{len(results)}</div><div style="color:var(--accent); font-size:12px; margin-top:6px;">Audited</div></div>
    <div class="metric-card"><div class="metric-label">OK to Pay</div><div class="metric-val" style="color:var(--success);">{status_counts.get("ok_to_pay", 0)}</div><div style="color:var(--success); font-size:12px; margin-top:6px;">Disbursement ready</div></div>
    <div class="metric-card"><div class="metric-label">Needs Bill</div><div class="metric-val" style="color:var(--warning);">{status_counts.get("needs_bill", 0)}</div><div style="color:var(--warning); font-size:12px; margin-top:6px;">Missing receipts</div></div>
    <div class="metric-card"><div class="metric-label">Needs Approval</div><div class="metric-val" style="color:var(--danger);">{status_counts.get("needs_approval", 0)}</div><div style="color:var(--danger); font-size:12px; margin-top:6px;">&gt;5k / Split claims</div></div>
    <div class="metric-card"><div class="metric-label">Over Budget</div><div class="metric-val" style="color:#e879f9;">{status_counts.get("over_budget", 0)}</div><div style="color:#e879f9; font-size:12px; margin-top:6px;">Exceeds limit</div></div>
  </div>

  <div class="table-container">
    <table>
      <thead><tr><th>ID</th><th>Club</th><th>Date</th><th>Category</th><th>Amount</th><th>Status</th><th>Reason</th></tr></thead>
      <tbody>
"""
    for r in results:
        amt = f"Rs. {int(r['amount']):,}" if r.get('amount') else "N/A"
        st = r.get('status', '')
        html_content += f"""        <tr>
          <td><strong>{r.get('id')}</strong></td><td>{r.get('club')}</td><td>{r.get('date')}</td><td>{r.get('category')}</td>
          <td>{amt}</td><td><span class="status-tag tag-{st}">{st}</span></td>
          <td style="color: var(--text-muted); font-size: 12px;">{r.get('reason')}</td>
        </tr>\n"""

    html_content += """      </tbody>
    </table>
  </div>
</div>

<div id="tab-payable" class="tab-content">
  <div class="table-container">
    <table>
      <thead><tr><th>ID</th><th>Club</th><th>Date</th><th>Category</th><th>Amount</th><th>Summary</th></tr></thead>
      <tbody>
"""
    for r in payable:
        amt = f"Rs. {int(r['amount']):,}" if r.get('amount') else "N/A"
        html_content += f"        <tr><td><strong>{r.get('id')}</strong></td><td>{r.get('club')}</td><td>{r.get('date')}</td><td>{r.get('category')}</td><td>{amt}</td><td>{r.get('summary')}</td></tr>\n"

    html_content += """      </tbody>
    </table>
  </div>
</div>

<div id="tab-review" class="tab-content">
  <div class="table-container">
    <table>
      <thead><tr><th>ID</th><th>Club</th><th>Date</th><th>Category</th><th>Amount</th><th>Status</th><th>Reason</th><th>Note</th></tr></thead>
      <tbody>
"""
    for r in review:
        amt = f"Rs. {int(r['amount']):,}" if r.get('amount') else "N/A"
        st = r.get('status', '')
        html_content += f"""        <tr>
          <td><strong>{r.get('id')}</strong></td><td>{r.get('club')}</td><td>{r.get('date')}</td><td>{r.get('category')}</td><td>{amt}</td>
          <td><span class="status-tag tag-{st}">{st}</span></td>
          <td style="color:#f87171; font-size:12px;">{r.get('reason')}</td><td style="color:var(--text-muted); font-size:12px;">{r.get('note')}</td>
        </tr>\n"""

    html_content += f"""      </tbody>
    </table>
  </div>
</div>

<div id="tab-summary" class="tab-content">
  <pre>{summary_text}</pre>
</div>

<script>
function switchTab(tabId) {{
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
  event.target.classList.add('active');
}}
</script>
</body>
</html>
"""
    out_path = os.path.join(BASE_DIR, "dashboard.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_html_dashboard()
