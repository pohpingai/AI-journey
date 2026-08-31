| 4 | 🎯 [Course Fit Checker](./course-fit-checker) | August 2026 | 2 versions tested, 1 silent failure caught — a blunt sub-agent that vets a course against my budget and skill level |

# 🎯 Course Fit Checker

**A blunt sub-agent that tells me whether a course is worth the money and time — and admits when it can't tell.**

Built August 2026, over a few evenings.

---

## Why I built it

Not to solve a problem. I wanted to learn how sub-agents actually work, and I needed a task small enough that I could tell whether the thing was behaving.

Course-checking fit that well. The rules are pass/fail, so I'd know immediately if the agent got it wrong. The inputs are two short files I control, so I could change them and watch the behaviour change. And the output is one word, which makes hedging obvious the moment it happens.

The real subject here is the agent, not the course.

---

## What it does

Reads a course page and checks it against two files I control:

| File | What it holds |
|---|---|
| `my-skills.md` | My current level — "zero coder" |
| `what-i-want.md` | My ceilings — RM200 budget, 20 total hours |

Then it returns one of exactly three verdicts: **TAKE**, **SKIP**, or
**NEEDS INFO**. No "it depends." No "worth considering."

---

## 📋 What the output looks like

Real run, platform masked:

```
1. Course
   Intro to AI Agents and Agentic AI — [course platform]

2. Gates
   Price — PASS. Quote: "Current price RM59.90" / "Original Price RM79.90".
     RM59.90 is under the RM200 ceiling in what-i-want.md. Already in Ringgit,
     no conversion needed.
   Hours — PASS. Quote: "9 sections · 54 lectures · 2h 11m total length".
     2h 11m is under the 20-hour ceiling.
   Level — FITS. Quote: "Requirements / No prior knowledge is required".
     No programming language or coding prerequisite listed anywhere.

3. Findings
   1. "23 hours left at this price!" — the RM59.90 price is a time-limited
      discount, not a steady price. The RM79.90 fallback still passes.
   2. "Course content is not provided. There is no point in completing the
      course if we cannot revise or check it in the future." (1-star review)
      — a complaint about post-completion access. Does not affect the gates.
   3. Page shows a "Frequently bought together" bundle at RM139.80. Not the
      course under review; excluded from the gate checks.

4. Obstacles Encountered
   - The discount end is stated only as a countdown ("23 hours left at this
     price!"), not a fixed date. How long RM59.90 lasts is unclear — though
     irrelevant here, since the original price also clears the ceiling.
   - None of these affected the verdict.

5. Verdict
   TAKE
```

Every figure has to be quoted from the page. If it can't quote it, it didn't
see it — and the gate goes to UNSTATED instead of a guess.

---

## How I built it

Four decisions, made one at a time. That order mattered more than I expected —
designing the whole thing at once was overwhelming.

**1. Which file plays which role.** The two reference files are the standard;
the course is the only thing under review. Without spelling this out, the agent
starts critiquing my budget instead of measuring against it.

**2. Report card sections.** Five, in fixed order: Course → Gates → Findings →
Obstacles → Verdict.

**3. Obstacles Encountered.** A section where the agent must declare what it
couldn't check. This turned out to be the most important part.

**4. A fixed verdict menu.** Three words, nothing else allowed. This is the
honesty lever — it removes the room to hedge.

Tools: `Read` only. No write tools, so it physically cannot modify anything.

---

## 🔬 The accidental experiment

I built two versions to settle an argument with myself: is it better to paste
the course text in, or let the agent fetch the URL itself?

Same manual, same gates. Only difference in the frontmatter:

```yaml
tools: Read              # paste version
tools: Read, WebFetch    # fetch version
```

**What happened:**

The fetch version got blocked — the course platform returned HTTP 403 to an
automated request. My agent did exactly what I'd told it to:

```
2. Gates
   Price — UNSTATED. No text could be retrieved from the page.
   Hours — UNSTATED. No text could be retrieved from the page.
   Level — Could not be determined. No text could be retrieved.

5. Verdict
   NEEDS INFO — the page itself must load; without any content from it I
   cannot confirm price, hours, or whether coding is assumed.
```

It refused to fill the gap from what it already knew about that site.

Then the parent agent went and fetched the page with its browser — a tool my
sub-agent didn't have — and wrote its own report. Clean formatting. A nice
comparison table. **That's what appeared on my screen.**

I nearly concluded the URL version was the better one. It had never produced
that output at all.

---

## 🧠 What I learned

**An agent is only as capable as the tools you hand it.** Mine didn't fail at
reasoning. It was locked out of a room the parent could walk into. A plain
fetch sends a bare request; a browser renders the page and looks like a real
visit. Same task, different door.

**"I couldn't determine this" is a feature.** The Obstacles section is what
stops a gap from being quietly filled with a confident guess. Without it, the
report reads cleaner — and means less.

**Read what your agent actually said, not the summary.** The parent's polished
version sat on top of my agent's honest refusal. One collapsed panel stood
between me and the wrong conclusion.

**A saved page is a snapshot.** My two runs disagreed on price — RM59.90 vs
RM79.90. Not a bug. The sale had ended between saving the page and checking it.
Neither pasting nor fetching fixes that; only re-capturing does.

---

## 🪤 Traps I fell into

- **Both agent files declared the same `name:` in frontmatter.** Claude Code
  keeps one and silently discards the other. No error, no warning. The missing
  agent simply isn't there.
- **Ran it before restarting.** Agents load at startup, so I was testing an old
  version of a file I'd already fixed.
- **Contradicted myself in my own constraints file.** I wrote "hours per week
  ceiling: 20 hours for the entire course." Per week, or entire course? The
  agent would have had to guess. Caught it before running.

---

## Files

```
.claude/agents/
  course-fit-checker.md       # paste version — tools: Read
  course-fit-checker-url.md   # fetch version — tools: Read, WebFetch
my-skills.md                  # my level
what-i-want.md                # my ceilings
course-page.md                # the course under review
```

---

## Skills unlocked

Claude Code sub-agents, YAML frontmatter (`name`, `description`, `tools`,
`model`, `color`), tool-scoping as a safety lever, designing an output format
that resists hedging, and A/B testing two agents against the same input.
