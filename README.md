# 🚀 My AI Journey

Hi! I'm a Digital Technologies Business Partner in FMCG, learning to build with AI — starting from **zero coding background**.

This repo is my public journal. Each folder is one project. The goal: look back every few months and see how far I've come, and show what a business person can build with AI as a co-pilot.

---

## 📅 Timeline

### Project 1 — 🧾 Toll Booth (July 2026 · built over a few evenings)
**FinOps for AI: cost visibility + model routing for an AI agent**

A 4-step consumer-feedback agent for a fictional snack brand, with every AI call metered through a LiteLLM proxy ("the toll booth").

Headline results:
- Built a cost dashboard: cost per task, per step, per message
- One routing rule (cheap model for easy messages, premium for hard/safety ones) cut total cost by **38.1%**
- Quality held at **96% approved** (measured by an AI quality-check step)

→ [See the project](./toll-booth/)

Skills unlocked: Terminal basics, Python scripts (run, not write — yet!), APIs & API keys, LiteLLM proxy, token economics, model routing, basic evals.

### Project 2 — 🏁 Pit Wall MY (July 2026)
**Post-race F1 analytics, refreshed automatically, for $0/month**

A post-race analysis dashboard that turns raw session data into Drama Log, Heroes & Zeroes, Rejoin Strip, and Gap Trace views — live within 4 hours of the chequered flag, with zero manual steps and zero hosting cost.

Headline results:
- Fully automated refresh via scheduled GitHub Actions — no server, no manual publishing step
- Runs end-to-end at **$0/month** (GitHub Actions + GitHub Pages)
- Enforced an accuracy principle: every number is provable from the data; all interpretation is confined to a manually-written editor's take

→ [See the project](./pit-wall-my/) · [Live dashboard](https://pohpingai.github.io/f1-dashboard/) · [Code repo](https://github.com/pohpingai/f1-dashboard)

Skills unlocked: automating a recurring task end-to-end (GitHub Actions), sourcing and reconciling APIs, bug reporting and accuracy auditing before shipping.

---

## 🧭 Why I'm doing this

AI agents don't cost like software — their costs are variable and hard to predict. Enterprises are racing to get visibility and control over AI spend (FinOps for AI). As a business partner, I want to speak both languages: the business case *and* the mechanics underneath it.

*Built with Claude as my guide. All code AI-assisted; all understanding hard-earned.* 😄
