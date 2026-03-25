# Two-Layer Hook Purpose: Compliance Minimizes Errors, QA Maximizes Autonomous Run Length

AI agent governance hooks are often treated as a single category. This insight distinguishes two fundamentally different purposes — compliance and QA — and shows why both are necessary for practical agent autonomy.

## The Insight

Governance hooks serve two distinct purposes that are complementary, not redundant:

**Layer 1 — Compliance hooks minimize errors.**
Force the system to follow processes: classify, route to the right skill, dispatch declared agents, block dangerous operations. Prevents shortcuts, missed steps, going rogue. Keeps the system on the rails.

**Layer 2 — QA hooks maximize autonomous run length.**
Before completing, verify claims empirically. Before asking for help, reflect and try to improve. Before reporting, check against source material. Escalate only after exhausting autonomous capabilities. Keeps the system running on the rails longer before needing user intervention.

## Why This Matters

This applies to all agent autonomy models — not just Claude Code, not just this framework. Any system that delegates to AI agents faces two failure modes:

1. **Process failure** — the agent skips steps, takes shortcuts, goes down wrong paths. Compliance hooks prevent this.
2. **Premature escalation** — the agent encounters difficulty and immediately asks for help instead of trying to self-correct. QA hooks prevent this.

Without Layer 1, the system is unreliable. Without Layer 2, the system is high-maintenance. Both are needed for practical autonomy.

## The Autonomy Target

Not "no user needed." The target is: **exhaust all autonomous capabilities before asking for help.** Going down wrong paths, getting stuck, needing help — completely fine and expected. The system's job is to run as long as it productively can before requiring human judgment.

Multi-agent frameworks like Jules, MetaGPT, and ChatDev all require user judgment. None aim to eliminate it. They aim to maximize what gets done between user touchpoints. QA enforcement is the mechanism that extends those intervals.

## QA as Enforced Exploration

The model's default is confidence: "I built it, it works, done." QA enforcement reverses this:

```
Build/analyze/research → think you're finished
  → try to BREAK what you just did
    → if it breaks → you were wrong → try to fix
      → if fix works → loop back to QA
      → if no fix works → NOW ask the user
    → if it doesn't break → genuinely done
```

This is **enforced exploration via consequence.** Soft instructions can't make the model WANT to explore. But QA enforcement forces the CONSEQUENCE of exploring — testing and breaking. The model doesn't need to be curious. It needs to try to destroy its own output.

**The human parallel:** A skilled practitioner starts by questioning their ability to accomplish something. This leads to evaluating the path, trying to build, and trying to break. The exploration instinct drives the cycle. Since we can't install that instinct in the model, we install the consequence — the QA hook forces the breaking step that the instinct would have produced.

**Compliance hooks reduce the space where mistakes can happen (process minimizes friction points). QA hooks force you to find the mistakes that remain in the reduced space.**

## QA on QA — Who Watches the Watchmen?

QA's claims are themselves testable because QA produces reproducible evidence, not judgment.

| Layer | Question | Enforced by | Enforceable? |
|-------|----------|------------|-------------|
| 1 | Was QA invoked? | Dispatch compliance hook | Yes |
| 2 | Did QA actually run tests? | Stop hook — tool call evidence in transcript | Yes |
| 3 | Did QA test edge cases, not just happy path? | Stop hook — test diversity (all-PASS is suspicious, no negative assertions = red flag) | Partially |
| 4 | Were the RIGHT tests chosen? | User judgment | No — irreducibly human |

**Key insight:** The model defaults to happy-path testing (confidence mode). QA-on-QA catches this by checking for test diversity — edge cases, negative assertions, adversarial inputs. A QA report with only PASS and only positive assertions is structurally detectable as "didn't try to break it."

The recursion terminates at Layer 4: "were the tests meaningful?" This is judgment, not verification. Layers 1-3 are hook-enforceable.

## Implementation Gap

QA compound can be declared in routing metadata but is not always enforced. A stop hook verifying QA claims were tested when routing declares QA as required would close this gap — the same pattern used for agent dispatch enforcement.
