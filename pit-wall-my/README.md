# 🏁 Pit Wall MY — Post-Race F1 Analytics Dashboard

**One-line summary:** An automated post-race analysis dashboard that turns raw session data into a readable story within 4 hours of the chequered flag — refreshed automatically via GitHub Actions, running at **$0/month**.

Built by a zero-coding-background FMCG business partner, guided step-by-step by AI.

🔗 **Live site:** https://pohpingai.github.io/f1-dashboard/
🔗 **Code repo:** https://github.com/pohpingai/f1-dashboard

---

## What it does

Every F1 session (practice, qualifying, race), Pit Wall MY pulls the session data and generates a post-race analysis — live on the dashboard about 4 hours after the chequered flag, with no manual step. A scheduled GitHub Actions workflow does the fetch, process, and publish; there's no server to run or pay for.

## Modules

- **Drama Log** — a timeline of the session's key moments (overtakes, pit stops, incidents, retirements) in the order they happened
- **Heroes & Zeroes** — the session's standout performers and underperformers, ranked by measurable results, not opinion
- **Rejoin Strip** — classifies every pit stop by what happened right after: clean rejoin, dirty air, or rejoin clash with another car
- **Gap Trace** — compares pace and race gap between any two drivers across the session, lap by lap

## The accuracy principle

The rule I held myself to throughout: **every number on the dashboard must be provable straight from the data.** No inferred causes, no "probably because" narratives baked into the automated output. Any interpretation — the "why," the storyline — is confined to a separate, manually-written **editor's take**, clearly separated from the data-driven modules. If it's not traceable to a timing sheet or telemetry field, it doesn't appear as fact.

### A note on accuracy

This is a personal, experimental project — not a certified data feed, and not built to compete with official F1 timing or professional broadcast tools. Every number here is meant to be traceable to the source data, and I actively remove any hook or headline that infers a cause the data can't prove. That said, this runs on free public APIs and AI-assisted code, both of which can be wrong — if you spot something that doesn't add up, I'd genuinely like to know.

## Architecture (at $0/month)

Session data → GitHub Actions (scheduled) → processing scripts → static site → GitHub Pages.

No paid hosting, no paid compute, no database — the whole pipeline runs on GitHub's free tier.
