# Thinking Techniques: How to Make Claude Think Better Before Answering

These are techniques discovered and tested in a Claude Code governance setup. They're based on actual research (85+ academic references) and hands-on experiments. Most of them work in Claude Projects via Custom Instructions or conversation techniques — they don't require Claude Code.

## The Core Problem

Claude has an inline bias — its default is to answer immediately rather than stop and think. This is built into how LLMs work (continuing text is always more probable than pausing). When you ask something ambiguous or short, Claude often gives a surface-level answer instead of engaging with what you actually need.

Research says: adding more rules ("always think carefully") doesn't fix this. What works is **forcing a reasoning step before the answer.**

---

## Technique 1: The Implication Question

**What it is:** Before answering, Claude asks itself: "What does this prompt imply?"

**Why it works:** It forces Claude to engage with the MEANING of your message before jumping to a response. Short messages like "okay" or "that seems off" look simple but often carry important context. Without this step, Claude classifies them as trivial and gives a shallow response.

**How to implement in Custom Instructions:**

```
Before responding to any message, first answer this question internally:
"What does this prompt imply?"
Write your answer as a one-line IMPLIES: field before your response.
This is not optional. Engage with what I actually need beneath the literal words.
```

**What you'll see:** Claude's responses will start with something like:
```
IMPLIES: User is questioning whether the current approach accounts for editorial vs judge audiences.
```

This one line often changes the entire response quality. Tested: with this question, Claude correctly handled 18/18 ambiguous prompts. Without it, it missed 2.

There are signs this effect scales with conversation length. In short conversations, any forced thinking step helps equally. In long conversations (50K+ tokens of context), "What does this imply?" draws on everything that was discussed — corrections, decisions, patterns — while a specific question like "list the key points" stays flat regardless of context. This hasn't been proven rigorously yet because it requires controlled experiments at different conversation lengths.

**The science:** This is based on "condition masking" (ProCo, EMNLP 2024) — forcing the model to re-derive meaning rather than pattern-matching to the most obvious interpretation.

---

## Technique 2: Burden of Proof on Quick Answers

**What it is:** Instead of defaulting to a quick answer and only going deep when forced, Claude defaults to depth and only goes quick when it can prove the answer is genuinely simple.

**How to implement in Custom Instructions:**

```
Default assumption: my message requires thoughtful analysis.
Only give a brief answer if ALL of these are true:
- The message is a single factual question with one clear answer
- No reasoning chain is needed
- A wrong answer has no consequences
- You are not investigating, comparing, or evaluating anything

If you're unsure whether to go deep or quick — go deep.
When I say things like "are you sure?", "think deeper", or push back on your answer,
that means escalate, not confirm.
```

---

## Technique 3: Exploration Before Extraction

**What it is:** When you need Claude to analyze something, start with an open question before a specific one.

**The pattern:**
- DON'T start with: "List the 5 key points from this document" (extraction — channels thinking into a track)
- DO start with: "What's actually going on in this document?" (exploration — lets Claude discover what matters)
- THEN follow with: "Now list the key points" (extraction — now informed by the exploration)

**Why it works:** Extraction questions ("list X", "find Y", "summarize Z") tell Claude what to look for. This is useful when you know what matters. But when the input is complex or ambiguous, extraction misses what it wasn't told to find. Exploration forces Claude to engage with the full content first.

**Practical examples:**

| Instead of | Try first |
|---|---|
| "Summarize this for the judges" | "What does this submission actually have going for it?" then "Now draft the summary" |
| "List the metrics we should include" | "What story do these metrics tell?" then "Pick the strongest 3 for this field" |
| "Write the 250-word response" | "What does the judge actually want to read here?" then "Now write it" |

---

## Technique 4: Chain of Implications (for complex tasks)

**What it is:** Don't just ask what something means — ask what THAT means, and what THAT means.

**The pattern:**
```
You: "The team went from zero to submittable in 20 minutes"

Level 1: What does this imply? -> Structured inputs make drafting fast
Level 2: What does THAT imply? -> Automation should focus on input quality, not draft quality
Level 3: What does THAT imply? -> The system should be a context assembler, not a drafting engine
```

**How to use it:** When Claude gives you a surface-level answer, just say: "What does that imply for us?" Keep pulling the thread. Each level reveals a deeper insight.

This is how decomposition should work — not mechanically ("list the parts") but through meaning ("what does this lead to?").

---

## Technique 5: Name What You're Unsure About

**What it is:** Ask Claude to state its assumptions and uncertainties before presenting conclusions.

**How to implement in Custom Instructions:**

```
When presenting analysis or recommendations:
- State what you're assuming (not just what you concluded)
- If you lack data for a claim, say so explicitly
- If you're choosing one direction over another, name what you'd miss by going the other way
```

**Why this matters:** Claude tends to present conclusions confidently even when the evidence is thin. This instruction doesn't make Claude more honest internally (research shows self-reported confidence is unreliable), but it makes the reasoning VISIBLE to you — so you can catch when it's guessing.

---

## Quick Reference

| Technique | One-liner | When to use |
|---|---|---|
| Implication question | "What does this prompt imply?" | Every message (add to Custom Instructions) |
| Burden of proof | Default to depth, not quick | Every message (add to Custom Instructions) |
| Exploration before extraction | "What's actually going on?" before "List X" | Complex inputs, new documents, ambiguous tasks |
| Chain of implications | "What does that imply for us?" | When the first answer feels too surface-level |
| Name uncertainties | "What are you assuming here?" | Before committing to a direction |

---

## The Foundation: Structured Project Memory

Before the thinking tools — the most impactful change is how you organize project knowledge. Using an Obsidian vault (or any structured markdown folder) as project memory gives Claude access to context, decisions, specs, and research without pasting it every time.

### Recommended Structure

```
Your-Project/
  CLAUDE.md              <- System instructions (loaded automatically)
  .claude/
    skills/              <- thinking tools (task-classifier, ensemble, etc.)
    agents/              <- specialist agents (adversarial-reviewer, etc.)
    hooks/               <- automation scripts
    settings.local.json  <- hook registration + permissions
  Projects/
    Your-Project-Name/
      STATE.md           <- current status, next steps, blockers
      PROJECT.md         <- long-lived decisions, architecture
      task_plan.md       <- incremental task checklist
      work/              <- active work files — date-prefixed
      archive/           <- completed/superseded work files
```

### The Three-File Hierarchy

1. **PROJECT.md** — the constitution. Mission, architecture, long-lived decisions. Rarely changes.
2. **STATE.md** — the current state. What's in progress, what's next, what's blocked. Rewritten at checkpoints. Claude reads this FIRST when resuming.
3. **task_plan.md** — the checklist. Incremental steps with completion markers. Drives daily work.

### Key Rules

- **Filenames:** kebab-case, date-prefixed for work files (`2026-03-20-research-findings.md`)
- **Frontmatter:** every file gets `date`, `status`, `tags` in YAML frontmatter
- **Work output** goes to `work/` — never the root
- **Completed work** moves to `archive/`
- **State is saved, not memorized** — Claude reads STATE.md, doesn't rely on memory across sessions

---

## For Claude Code Users: Full Implementation Guide

If you're using Claude Code (CLI or Desktop), you can implement these as system components.

**Prerequisites:** Claude Code installed, a project folder with a system instruction file.

### 1. System Instructions — The Foundation

Create a system instruction file at your project root with:

```markdown
## Style
- Direct and minimal. No fluff. Short answers unless depth is needed.

## Task Classification (mandatory)
Before any substantive task, invoke the `task-classifier` skill. This determines task type and approach before any work begins. Skip only for truly trivial one-liners.

## Delegation
Never produce analysis, evaluation, or documents inline when a specialist agent exists. Delegate first.

Available agents (in .claude/agents/):
- adversarial-reviewer — challenges decisions before you commit

When dispatching an agent for evaluation, provide ONLY what to examine and criteria — no hypothesis or expected outcome (blind analysis rule).

## State Management
- Read STATE.md first when resuming — it has current status and next task
- Save STATE.md after milestones, before ending sessions
- Work output goes to work/ with date prefix
```

### 2. Task Classifier Skill

Create `.claude/skills/task-classifier/SKILL.md`:

```markdown
---
name: task-classifier
description: Classify the current task before any work begins.
---

# Task Classifier

## Step 0 — Read for Depth
Before anything else, answer: **What does this prompt imply?**
Write your answer as `IMPLIES:` in the classification block.

## Step 1 — Classify
- Research — open questions, needs source materials
- Analysis — investigating causes, evaluating, comparing
- Content — producing written copy for an audience
- Build — implementing code, scripts, workflows
- Planning — designing architecture, sequencing work

## Step 2 — Quick Check (burden of proof is on Quick)
Quick ONLY if ALL true: no depth signals, not a follow-up, single factual lookup, no reasoning needed, no consequences.

## Step 3 — Announce
IMPLIES: [what the prompt actually means]
TASK TYPE: [Quick / Research / Analysis / Content / Build / Planning]
APPROACH: [what to do and how]
```

### 3. Adversarial Reviewer Agent

Create `.claude/agents/adversarial-reviewer.md`:

```markdown
---
description: Challenge decisions, plans, and designs. Read-only.
---

You are a critical reviewer dispatched to challenge a decision or plan.

Your job:
1. Find the strongest argument AGAINST the proposed direction
2. Identify unstated or unverified assumptions
3. Name the specific failure mode everyone is ignoring
4. State what you would do instead, with reasoning

Rules:
- Be direct. No praise. No hedging. Only critique.
- You are one perspective, not the final judge
- Do not suggest "more research" as a catch-all
- Under 300 words.
```

### 4. Ensemble Skill

Create `.claude/skills/ensemble/SKILL.md` — spawns 4 parallel agents with different analytical lenses (Reframe, Decompose, Stakeholder, Adversarial) on any design question. Produces a divergence map showing agreement and disagreement.

### 5. UserPromptSubmit Hook — Classifier Enforcement

Register in `.claude/settings.local.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo \"MANDATORY: Invoke the task-classifier skill before responding to EVERY message.\""
          }
        ]
      }
    ]
  }
}
```

Without this hook, agents skip classification ~75% of the time. With it, activation goes to 90%+.

### 6. Epistemic Check Stop Hook (Advanced, CLI Only)

A second model (Haiku) reviews every non-trivial response for overconfidence before it reaches the user. If conclusions are presented without acknowledging uncertainty, the check blocks and forces the agent to state its assumptions.

**Note:** This only works in CLI mode. In the Desktop app, subprocess calls trigger permission prompts on every response.

### Priority Order

| # | Tool | Setup Time | Impact |
|---|---|---|---|
| 1 | IMPLIES in Custom Instructions | 2 min | High |
| 2 | System instructions + task classifier | 15 min | High |
| 3 | UserPromptSubmit hook | 10 min | High |
| 4 | Adversarial reviewer agent | 5 min | Medium |
| 5 | Ensemble skill | 15 min | High for design |
| 6 | Epistemic check Stop hook | 30 min | High (CLI only) |

---

## What We're Still Testing

- **The implication question scales with context.** In short conversations, any forced question helps. In long conversations (200K+ tokens), "What does this imply?" draws on the full context in ways specific questions don't. Observed but not yet proven.
- **The epistemic honesty problem is hard.** Even with these tools, Claude converges on conclusions fast and rarely says "I might be wrong."
- **User pushback is still the best quality mechanism.** When you say "are you sure?" or "think deeper," that produces more improvement than any tool we've built. Don't stop doing it.
