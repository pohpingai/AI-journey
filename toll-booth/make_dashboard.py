import csv
from collections import defaultdict

rows = []
with open("results_baseline.csv") as f:
    for r in csv.DictReader(f):
        r["cost_usd"] = float(r["cost_usd"])
        r["prompt_tokens"] = int(r["prompt_tokens"] or 0)
        r["completion_tokens"] = int(r["completion_tokens"] or 0)
        rows.append(r)

total_cost = sum(r["cost_usd"] for r in rows)
n_messages = len(set(r["message_id"] for r in rows))
n_calls = len(rows)
total_tokens = sum(r["prompt_tokens"] + r["completion_tokens"] for r in rows)

step_cost = defaultdict(float)
for r in rows:
    step_cost[r["step"]] += r["cost_usd"]
steps = sorted(step_cost.keys())

msg_cost = defaultdict(float)
for r in rows:
    msg_cost[int(r["message_id"])] += r["cost_usd"]
msg_ids = sorted(msg_cost.keys())

top5 = sorted(msg_cost.items(), key=lambda x: -x[1])[:5]

html = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Pit Wall - AI Cost Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
  body { font-family: -apple-system, Helvetica, Arial, sans-serif; background:#0f1220; color:#eef0f6; margin:0; padding:32px; }
  h1 { margin:0 0 4px 0; } .sub { color:#9aa3b8; margin-bottom:28px; }
  .cards { display:flex; gap:16px; flex-wrap:wrap; margin-bottom:28px; }
  .card { background:#1a1f33; border-radius:14px; padding:18px 24px; min-width:170px; }
  .card .big { font-size:30px; font-weight:700; margin-top:6px; }
  .card .label { color:#9aa3b8; font-size:13px; }
  .panel { background:#1a1f33; border-radius:14px; padding:20px; margin-bottom:24px; }
  .panel h2 { margin:0 0 14px 0; font-size:16px; color:#c9d1e3; }
  table { width:100%; border-collapse:collapse; font-size:14px; }
  td, th { padding:8px 10px; text-align:left; border-bottom:1px solid #2a3050; }
  th { color:#9aa3b8; font-weight:600; }
  .grid { display:grid; grid-template-columns:1fr 1fr; gap:24px; }
  @media (max-width:900px){ .grid{ grid-template-columns:1fr; } }
</style>
</head>
<body>
<h1>Pit Wall - AI Cost Dashboard</h1>
<div class="sub">CrunchLab consumer feedback agent - baseline run (all steps on race-car / Sonnet)</div>

<div class="cards">
  <div class="card"><div class="label">Messages processed</div><div class="big">__N_MSG__</div></div>
  <div class="card"><div class="label">AI calls</div><div class="big">__N_CALLS__</div></div>
  <div class="card"><div class="label">Total cost</div><div class="big">$__TOTAL__</div></div>
  <div class="card"><div class="label">Cost per message</div><div class="big">$__PER_MSG__</div></div>
  <div class="card"><div class="label">Total tokens</div><div class="big">__TOKENS__</div></div>
</div>

<div class="grid">
  <div class="panel">
    <h2>Cost by step - where does the money go?</h2>
    <canvas id="stepChart"></canvas>
  </div>
  <div class="panel">
    <h2>Top 5 most expensive messages</h2>
    <table>
      <tr><th>Message ID</th><th>Cost</th></tr>
      __TOP5_ROWS__
    </table>
  </div>
</div>

<div class="panel">
  <h2>Cost per message (all 50)</h2>
  <canvas id="msgChart" height="90"></canvas>
</div>

<script>
new Chart(document.getElementById('stepChart'), {
  type: 'bar',
  data: {
    labels: __STEP_LABELS__,
    datasets: [{ label: 'Cost (USD)', data: __STEP_DATA__, backgroundColor: ['#4e79ff','#38c6a5','#f2b134','#e35d7c'] }]
  },
  options: { plugins:{legend:{display:false}}, scales:{ y:{ ticks:{color:'#9aa3b8'} }, x:{ ticks:{color:'#9aa3b8'} } } }
});
new Chart(document.getElementById('msgChart'), {
  type: 'bar',
  data: {
    labels: __MSG_LABELS__,
    datasets: [{ label: 'Cost (USD)', data: __MSG_DATA__, backgroundColor: '#4e79ff' }]
  },
  options: { plugins:{legend:{display:false}}, scales:{ y:{ ticks:{color:'#9aa3b8'} }, x:{ ticks:{color:'#9aa3b8'} } } }
});
</script>
</body>
</html>
"""

top5_rows = "".join(
    "<tr><td>#%d</td><td>$%.4f</td></tr>" % (mid, c) for mid, c in top5
)

html = (html
    .replace("__N_MSG__", str(n_messages))
    .replace("__N_CALLS__", str(n_calls))
    .replace("__TOTAL__", "%.4f" % total_cost)
    .replace("__PER_MSG__", "%.4f" % (total_cost / n_messages))
    .replace("__TOKENS__", "{:,}".format(total_tokens))
    .replace("__STEP_LABELS__", str(steps))
    .replace("__STEP_DATA__", str([round(step_cost[s], 6) for s in steps]))
    .replace("__MSG_LABELS__", str([str(m) for m in msg_ids]))
    .replace("__MSG_DATA__", str([round(msg_cost[m], 6) for m in msg_ids]))
    .replace("__TOP5_ROWS__", top5_rows)
)

with open("dashboard.html", "w") as f:
    f.write(html)

print("Dashboard created: dashboard.html")
