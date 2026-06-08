# Measure Then Gate: Blocking Enforcement Needs an Evidence Bar

The instinct when a governance rule is violated is to ship a hard block. Across three independent enforcement decisions in a single framework, the blocking option was correctly declined or deferred once real data was consulted — and the pattern repeated often enough to become a rule.

## The Finding

Blocking enforcement imposes a cost: false positives, friction on high-traffic files, blast radius when the gate is wrong. That cost is only worth paying when the failure rate is high enough to justify it. Warn-first, instrument-first, then gate if the data demands it. Skipping measurement and shipping a block on intuition almost always over-enforces.

The three instances that crystallized this:

**1. A 2.7% failure rate does not warrant a blocking gate.**
A tool-recall habit was being skipped on some turns. The proposed fix was a Stop-hook that blocked the session until the recall was performed. Before shipping it, a governance log was instrumented. Measurement: 4 occurrences in 149 turns (2.7%), clustered on two days. A blocking gate that fires on fewer than 3% of turns imposes friction on 97% of clean turns and on every false positive in that 3%. The warn-only nudge was kept; the block was deferred pending a higher baseline.

**2. A constitution-blocker requires a proven trial before arming.**
A new edit-time validator caught broken dispatch-name references at write time. The tests passed (26/27). The obvious move was to register it and arm it immediately. It wasn't — because it gates writes to the highest-traffic files in the framework (the constitution and every skill specification). A residual false positive on those files is maximally disruptive. The hook shipped unregistered, opt-in, with a short trial window before arming. The evidence bar for a constitution-blocker is higher than for a narrow-scope hook.

**3. The block that never fired.**
A guardrail hook had been producing the right-looking output — logging block decisions — for 14 days while enforcing nothing. The hook emitted a block decision using the wrong hook protocol for its event type; the runtime silently ignored the decision and let the action through. It looked active in logs, passed its unit tests, and was referenced in governance dashboards. The failure rate it was meant to suppress continued undetected. (See also: [Wrong-Protocol Hooks Silently No-Op](wrong-protocol-hook-silently-noop.md) for the protocol mechanics.)

## The Mechanism

Enforcement is not free. The cost function has three components:

- **False-positive rate** — how often does the hook fire on legitimate behavior?
- **Blast radius** — which files / operations does the hook gate? Constitution-level gates multiply cost by traffic volume.
- **Detectability of failure** — a silently-dead hook produces no signal; cost without benefit runs indefinitely.

A blocking gate clears the bar when: measured failure rate is high enough that the false-positive tax is worth paying, the gate's blast radius is bounded, and the hook's liveness is verified against real runtime behavior (not just unit tests).

## The Decision Rule

```
Is the failure rate measured?        → if not, instrument first
Is the rate high enough to justify   → if not, ship warn/nudge
  blocking friction?
Is the blast radius bounded?         → if not, trial before arming
Is the hook verified live, not       → if not, do a live-fire check
  just unit-tested?
```

## Why This Keeps Recurring

The impulse to ship a block is not wrong — it comes from taking governance seriously. The error is treating "there exists a failure" as sufficient evidence for "a block is proportionate." Enforcement is a cost-benefit decision, and the benefit side needs a number.

This generalizes two older rules — "hooks are floors not ceilings" ([two-layer-hook-purpose.md](two-layer-hook-purpose.md)) and "low-false-positive enforcement only" ([hooks-over-prompts.md](hooks-over-prompts.md)) — into a quantitative decision rule: **measure the failure rate, then decide on the gate tier**.

## Connection to Other Insights

- **[Installed Is Not Adopted](installed-is-not-adopted.md):** The disciplined sequence (incorporate → instrument → gate on evidence) is the same sequence; this insight extends it to blocking specifically.
- **[Rubber-Stamp Enforcement Gaps](rubber-stamp-enforcement.md):** Both address enforcement that looks active but isn't. Measure-then-gate catches over-enforcement; rubber-stamp catches under-enforcement. They are the two sides of the same calibration problem.
- **[Wrong-Protocol Hooks Silently No-Op](wrong-protocol-hook-silently-noop.md):** Instance 3 above in full detail — the mechanism by which a hook can be silently dead for weeks without surfacing.
