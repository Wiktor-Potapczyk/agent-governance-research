# AI Agent Governance Framework: Reducing Supervision Overhead

This document summarizes a governance framework for AI coding agents, built to reduce manual oversight of LLM-assisted work sessions. It covers the problem, approach, architecture, evidence, and lessons learned.

---

## The Problem

Every AI-assisted work session required constant manual oversight. Without guardrails, the AI would attempt complex analysis itself rather than routing to the right specialist approach -- producing plausible-sounding but unreliable outputs. Correcting course mid-session was routine: catching biased reasoning, redirecting work to the right methodology, verifying that research questions were not framed to confirm existing assumptions. This supervision overhead consumed significant time on every project session -- time spent managing the tool instead of doing the work.

Two concrete failure patterns drove this initiative:

**Confirmation bias in research.** When investigating a problem, the AI would frame questions around whatever hypothesis was already in context, then surface supporting evidence. This meant research outputs looked thorough but were structurally biased -- they confirmed rather than investigated. Catching this required reading every delegation message before it was sent.

**No consistent methodology.** Each session started from scratch on how to approach a task. There was no automatic routing between "this needs research" vs. "this needs building" vs. "this needs a plan." The same methodology mistakes recurred across projects because nothing remembered or enforced the lessons from previous sessions.

**The business cost:** hours per week spent on supervision that should have been spent on project delivery.

---

## The Approach

Research first, build second, measure third.

Before writing any configuration, an autonomous research phase investigated how production multi-agent AI systems are structured, what bias prevention techniques actually work (vs. those that just sound good), and how successful solo operators scale AI-assisted work. This research ran as five independent tracks in parallel, was synthesized, and then stress-tested by a dedicated adversarial review that found three broken assumptions -- including a sequencing error in the build plan that would have caused downstream failures.

Development ran in **six increments**, each evaluated against real usage before the next began:

| Inc | What | Purpose |
|-----|------|---------|
| 1 | 28 specialized agents + anti-sycophancy controls | Right specialist for each task type; agents push back when wrong |
| 2 | Task classification system | Automatic routing: research, analysis, build, planning, content |
| 3-4 | 5 process templates + dispatcher | Consistent methodology per task type, enforced by routing |
| 5 | Enforcement hooks | Automated compliance reminders before every response |
| 6 | Bias prevention + adversarial review + quality metadata | Structural safeguards on research reliability |

Nothing was added speculatively. When an assumption was uncertain, it was tested before building around it.

---

## What It Enables

**Reduced supervision.** The system now automatically routes tasks to the correct methodology and reminds itself to follow delegation rules. The human role shifts from directing every step to reviewing outputs -- the same shift from "doing" to "managing" that scaling any operation requires.

**Reliable research outputs.** Research agents now carry structured quality metadata: confidence level, key assumptions, and source citations. A "blind analysis" rule -- enforced structurally, not just instructed -- prevents research from being framed to confirm existing assumptions. When an evaluator agent starts, it receives an automatic reminder to assess independently regardless of how the question was framed.

**Self-correcting infrastructure.** The system includes an evaluation framework that analyzes its own session transcripts to measure effectiveness. This is not theoretical -- it already caught a production bug that was invisible during normal operation (a detection regex that had never worked correctly since deployment). The system found the bug in itself.

**A foundation for increasing autonomy.** Each increment adds capability. The long-term direction: a system you can trust with progressively more complex autonomous work -- from structured research tasks today, toward proactive opportunity discovery and self-directed improvement over time.

---

## Evidence

The evaluation framework analyzed 5 sessions (~14 hours of real project work). Key findings:

| Metric | Result | Context |
|--------|--------|---------|
| Bias-free delegation rate | 97% (32/33) | Before the system: unmeasured, user caught violations by reading every message. Now: 1 violation in 33 delegations, caught same-session. |
| Agent output usability | 97% (32/33) | Outputs used as-is without rework. One output reworked due to framing correction. None discarded. |
| Self-healing | Bug found by eval loop | A broken detection regex had shipped unnoticed. The eval framework found it through transcript analysis. Invisible to normal operation. |
| Autonomous operation | Confirmed | Domain project sessions show parallel agent dispatches running correctly without manual prompting. |

**What we cannot yet measure:** exact hours saved per week (no pre-system baseline was tracked), and whether the compliance rate was already high before the system (likely lower given the 4 manual corrections per 14 hours observed, but not quantified). The next eval run after 3-5 more sessions will establish trends.

---

## What We Learned

**Structure beats instruction.** Telling the AI to delegate is unreliable. Automated hooks that fire before every response and inject compliance reminders are measurably more effective. The gap: the system can remind before a response but cannot yet detect when the response ignores the reminder. This is the primary open problem.

**The system found a bug in itself.** An audit regex shipped broken -- it appeared to work (the hook fired, content was injected) but the audit reporting was wrong. The eval loop caught it by analyzing transcripts. Lesson: "appears to work" and "works correctly" are different. Systematic measurement is the only way to tell them apart.

**Same-model review has limits.** The adversarial reviewer uses the same AI model family as the primary session. Different instructions create different failure modes, but correlated blind spots remain possible. Cross-model review (using a different AI provider) would close this gap. Evaluated, deferred -- added complexity was not justified yet, but it is a known limitation.

**Incremental beats waterfall.** The original plan tried to do too much at once. The adversarial review caught the sequencing error before any building started. The final six-increment approach, with evaluation between each step, produced a system that works. Given how fast AI tooling evolves, building incrementally -- smallest change, evaluate, then decide the next step -- is structurally better than planning everything upfront.

---

## Current Status and What Is Next

The system is live and being used on real project work. It is not a finished product -- it is a living system designed to evolve.

**The vision:** a system capable of self-healing (detecting and fixing its own issues), proactive self-advancement (discovering new capabilities to adopt), and autonomous deep research on demand. The target: run one command like "research emerging trends in our space" and trust the output -- backed by structured methodology, bias controls, and quality self-assessment.

**Near-term:**
- Rerun the eval loop after 3-5 more real sessions to establish performance trends
- Complete the structured audit on remaining agents (16 of 28)
- Continue using the system on real deliverables -- observed failures drive the next increment

**How we get there:** the same way we got here. Each increment adds capability, each eval reveals the next gap, each gap becomes the next increment. No speculative building. Evidence first.

---

## Appendix: How It Works in Practice

### A real work session

This is what actually happened when the user sent: *"Research the top 5 competitors in the awards automation space and compare their approaches"*

1. **The task classifier** ran immediately and announced: `TASK TYPE: Research`. It considered whether to use an autonomous research loop but determined the scope was bounded enough for direct delegation.

2. **The research process template** activated and defined the methodology: delegate to a research agent, then produce a structured report.

3. **A research-analyst agent was dispatched.** It ran 53 tool calls over ~8 minutes -- web searches, source evaluation, data extraction -- entirely autonomously. No steering required.

4. **A report-generator agent** took the findings and wrote a structured competitor comparison to disk.

5. **The result:** a substantive finding that no pure-play SaaS competitor exists in the awards automation space. The entire market is human consulting services, with only one AI-adjacent player. Five competitors profiled with pricing, approach, and positioning.

Total time from prompt to finished report: ~9 minutes. The user's role: send one message, review the output, decide what to do with it. The system handled methodology selection, agent routing, research execution, and report production without intervention.

**What the system adds beyond this flow:** The enforcement hook fired and injected the context bar before the response. The classifier invoked without needing the MANDATORY reminder -- the configuration file rules were sufficient. For tasks involving evaluation or review, a bias guard hook automatically injects an independence reminder into evaluator agents at startup. Research agents are instrumented to append quality metadata (confidence scores, assumptions, source citations) to substantial outputs -- giving the reviewer immediate visibility into output reliability.

### The infrastructure at a glance

```
User message
    |
    v
[Enforcement Hook] --- scans for task keywords, injects classifier reminder
    |
    v
[Task Classifier] --- routes to: Research / Analysis / Build / Planning / Content
    |
    v
[Process Template] --- defines methodology for that task type
    |
    v
[Specialist Agents] --- 28 agents, each with defined scope + anti-sycophancy controls
    |                     bias guard injected at startup for evaluator agents
    v
[Quality Metadata] --- confidence, assumptions, sources appended to output
    |
    v
[Self-Evaluation] --- transcript analysis measures system effectiveness over time
```

### Real example: the system catching its own bug

During the first evaluation run, the eval framework analyzed 5 session transcripts and tested whether the "audit signal" (which reports if the task classifier was recently used) was working. It found that the signal had **never** reported a positive detection -- across all sessions, it always said "not detected," even when the classifier had clearly been invoked.

The root cause: a field name mismatch in the detection logic. The hook searched for `"name": "task-classifier"` in the transcript, but the platform records it as `"skill": "task-classifier"`. One field name, wrong since deployment, invisible during normal use because the hook still fired and still reminded -- just the audit reporting was broken.

The fix was one line. The point: a human would never have caught this. The system's own evaluation framework did.
