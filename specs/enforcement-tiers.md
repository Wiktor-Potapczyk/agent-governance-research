# Process Step Enforcement Tiers

## The Problem

When a governance hook checks whether a process was followed correctly, some violations are clear-cut (missing a required output block) while others require judgment (was the right agent chosen?). Treating all violations the same -- either blocking on everything or logging everything -- leads to either brittle enforcement or toothless monitoring.

## Two-Tier Solution

### Hard Enforcement (Block)

Reserve blocking for violations that are:
- **Unambiguous** -- the check has no false positive risk
- **Structural** -- presence/absence of a required artifact, not quality judgment
- **Recoverable** -- the model can fix the violation in the same turn

Examples:
- Missing SCOPE block (every process skill must output one)
- Missing QA REPORT with PASS/FAIL (QA must produce a structured report)
- Missing PENTEST REPORT (pentesting must produce structured findings)

### Soft Enforcement (Log)

Reserve logging for violations that are:
- **Judgment-dependent** -- reasonable disagreement about whether it is a violation
- **Context-sensitive** -- sometimes the "violation" is the correct behavior
- **Data-gathering** -- collecting compliance rates before deciding whether to tighten

Examples:
- No synthesis agent when 2+ research agents dispatched (sometimes synthesis is overkill)
- No architect-review after a build (small changes might not need it)
- Zero agent dispatches for a process skill (some analyses can be done inline)

## The Principle

**Collect data before tightening.** Start with hard enforcement only on clear-cut violations. Log everything else. After enough data, identify which soft violations actually correlate with quality problems -- then promote those to hard enforcement with evidence.

This avoids the "mandatory exploration backfires" trap: forcing compliance on every check produces performative compliance, not genuine quality.
