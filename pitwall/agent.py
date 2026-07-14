# =============================================================
#  PIT WALL AGENT  (baseline lap)
#  Reads fake consumer messages, processes each in 4 steps,
#  sends every step through YOUR LiteLLM toll booth,
#  and logs the cost of every single step to a CSV file.
# =============================================================

import json
import csv
import requests

# ---- SETTINGS ------------------------------------------------
PROXY = "http://0.0.0.0:4000/chat/completions"  # your toll booth
MODEL = "race-car"   # baseline: EVERYTHING on the expensive model
LIMIT = 50            # how many messages to process (5 = test lap, 50 = full race)
# --------------------------------------------------------------


def ask(prompt):
    """Send one question through the toll booth. Return answer + cost info."""
    r = requests.post(PROXY, json={
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
    })
    r.raise_for_status()
    data = r.json()
    answer = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {})
    cost = float(r.headers.get("x-litellm-response-cost", 0) or 0)
    return answer, usage, cost


# Load the fake consumer messages
with open("messages.json") as f:
    messages = json.load(f)[:LIMIT]

rows = []        # every step's cost gets stored here
total_cost = 0.0

for m in messages:
    text = m["text"]
    print("")
    print("=== Message %d: %s..." % (m["id"], text[:60]))

    # ---- STEP 1: classify --------------------------------------
    category, u, c = ask(
        "You work in consumer care for CrunchLab snacks. "
        "Classify this message into exactly one category: "
        "packaging, taste, pricing, delivery, safety, or praise. "
        "Also judge difficulty: EASY or HARD. "
        "Reply with only: category | difficulty\n\nMessage: " + text)
    rows.append([m["id"], "1-classify", MODEL, u.get("prompt_tokens"), u.get("completion_tokens"), c])
    total_cost += c
    print("  1-classify -> %s   ($%.6f)" % (category.strip(), c))

    # ---- STEP 2: extract facts ---------------------------------
    facts, u, c = ask(
        "From this consumer message, extract: product (or 'unknown'), "
        "batch number (or 'none'), sentiment (positive/neutral/negative). "
        "Reply in one short line.\n\nMessage: " + text)
    rows.append([m["id"], "2-extract", MODEL, u.get("prompt_tokens"), u.get("completion_tokens"), c])
    total_cost += c
    print("  2-extract  -> %s   ($%.6f)" % (facts.strip()[:60], c))

    # ---- STEP 3: draft a reply ---------------------------------
    draft, u, c = ask(
        "You are CrunchLab consumer care. Category: " + category +
        ". Facts: " + facts +
        ". If the category is safety, write a short URGENT internal "
        "escalation memo instead of a consumer reply. Otherwise write "
        "a polite consumer reply, max 80 words.\n\nMessage: " + text)
    rows.append([m["id"], "3-draft", MODEL, u.get("prompt_tokens"), u.get("completion_tokens"), c])
    total_cost += c
    print("  3-draft    -> written   ($%.6f)" % c)

    # ---- STEP 4: quality check ---------------------------------
    verdict, u, c = ask(
        "Check this reply for politeness and accuracy. "
        "Answer only APPROVED or NEEDS FIX.\n\nOriginal message: " + text +
        "\n\nReply: " + draft)
    rows.append([m["id"], "4-check", MODEL, u.get("prompt_tokens"), u.get("completion_tokens"), c])
    total_cost += c
    print("  4-check    -> %s   ($%.6f)" % (verdict.strip(), c))

# ---- Save the lap data ----------------------------------------
with open("results_baseline.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["message_id", "step", "model", "prompt_tokens", "completion_tokens", "cost_usd"])
    w.writerows(rows)

print("")
print("================ PIT WALL REPORT ================")
print("Messages processed : %d" % len(messages))
print("AI calls made      : %d" % len(rows))
print("TOTAL COST         : $%.4f" % total_cost)
print("Cost per message   : $%.4f" % (total_cost / len(messages)))
print("Saved every lap to : results_baseline.csv")
print("=================================================")
