# =============================================================
#  PIT WALL AGENT v2 - TIRE STRATEGY (model routing)
#  Step 1 (triage) always on fast-car.
#  EASY messages  -> fast-car for everything (soft tires)
#  HARD messages  -> race-car for steps 2-4  (hard tires)
#  SAFETY messages -> always race-car (never cheap out on safety)
# =============================================================

import json
import csv
import requests

PROXY = "http://0.0.0.0:4000/chat/completions"
LIMIT = 50

def ask(prompt, model):
    r = requests.post(PROXY, json={
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    })
    r.raise_for_status()
    data = r.json()
    answer = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    cost = float(r.headers.get("x-litellm-response-cost", 0) or 0)
    return answer, usage, cost

with open("messages.json") as f:
    messages = json.load(f)[:LIMIT]

rows = []
total_cost = 0.0
approved = 0
needs_fix = 0

for m in messages:
    text = m["text"]
    print("")
    print("=== Message %d: %s..." % (m["id"], text[:60]))

    # STEP 1: triage - always on the cheap model
    category, u, c = ask(
        "You work in consumer care for CrunchLab snacks. "
        "Classify this message into exactly one category: "
        "packaging, taste, pricing, delivery, safety, or praise. "
        "Also judge difficulty: EASY or HARD. "
        "Reply with only: category | difficulty\n\nMessage: " + text,
        "fast-car")
    rows.append([m["id"], "1-classify", "fast-car", u.get("prompt_tokens"), u.get("completion_tokens"), c])
    total_cost += c

    # THE ROUTING RULE (tire strategy)
    is_hard = "HARD" in category.upper()
    is_safety = "safety" in category.lower()
    model = "race-car" if (is_hard or is_safety) else "fast-car"
    print("  1-classify -> %s  [tires: %s]  ($%.6f)" % (category.strip(), model, c))

    # STEP 2: extract facts
    facts, u, c = ask(
        "From this consumer message, extract: product (or 'unknown'), "
        "batch number (or 'none'), sentiment (positive/neutral/negative). "
        "Reply in one short line.\n\nMessage: " + text, model)
    rows.append([m["id"], "2-extract", model, u.get("prompt_tokens"), u.get("completion_tokens"), c])
    total_cost += c
    print("  2-extract  -> %s   ($%.6f)" % (facts.strip()[:60], c))

    # STEP 3: draft
    draft, u, c = ask(
        "You are CrunchLab consumer care. Category: " + category +
        ". Facts: " + facts +
        ". If the category is safety, write BOTH a short empathetic holding "
        "reply to the customer AND a short URGENT internal escalation memo. "
        "Otherwise write a polite consumer reply, max 80 words.\n\nMessage: " + text, model)
    rows.append([m["id"], "3-draft", model, u.get("prompt_tokens"), u.get("completion_tokens"), c])
    total_cost += c
    print("  3-draft    -> written   ($%.6f)" % c)

    # STEP 4: quality check
    verdict, u, c = ask(
        "Check this reply for politeness and accuracy. "
        "Answer only APPROVED or NEEDS FIX.\n\nOriginal message: " + text +
        "\n\nReply: " + draft, model)
    rows.append([m["id"], "4-check", model, u.get("prompt_tokens"), u.get("completion_tokens"), c])
    total_cost += c
    v = verdict.strip().upper()
    if "APPROVED" in v:
        approved += 1
    else:
        needs_fix += 1
    print("  4-check    -> %s   ($%.6f)" % (verdict.strip()[:40], c))

with open("results_routed.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["message_id", "step", "model", "prompt_tokens", "completion_tokens", "cost_usd"])
    w.writerows(rows)

# Compare against the baseline lap
baseline_cost = 0.0
try:
    with open("results_baseline.csv") as f:
        for r in csv.DictReader(f):
            baseline_cost += float(r["cost_usd"])
except Exception:
    pass

print("")
print("============= TIRE STRATEGY REPORT =============")
print("Messages processed : %d" % len(messages))
print("TOTAL COST (v2)    : $%.4f" % total_cost)
print("Cost per message   : $%.4f" % (total_cost / len(messages)))
print("Quality check      : %d APPROVED / %d NEEDS FIX" % (approved, needs_fix))
if baseline_cost > 0:
    saving = (baseline_cost - total_cost) / baseline_cost * 100
    print("Baseline cost      : $%.4f" % baseline_cost)
    print("SAVING             : %.1f%%" % saving)
print("Saved every lap to : results_routed.csv")
print("================================================")
