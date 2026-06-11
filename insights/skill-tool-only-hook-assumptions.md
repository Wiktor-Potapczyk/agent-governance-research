# Skill-Tool-Only Hook Assumptions

Governance hooks are written against a model of how a skill is invoked. When that model changes — a skill becomes a workflow — hooks written against the old model silently fail in one of three ways. This is a structural bug class, not a one-off oversight: every hook that contains a skill name is a candidate.

## The Finding

When a prose process skill converts to a deterministic workflow script, the invocation path changes: `Skill tool_use {name: "process-planning"}` becomes `Workflow tool_use {scriptPath: "...process-planning.js"}`. Hooks written when skills were the only invocation path detect the `Skill` event shape. They do not detect the `Workflow` event shape. The result depends on the hook's purpose:

**Three observed severity classes:**

**Hard misfire — blocks legitimate dispatches.** A routing-guard hook that scans the recent transcript for the last `TASK TYPE:` block and validates the current Skill invocation against it. When a workflow runs immediately before a prose-skill invocation, it leaves a `TASK TYPE: planning` residue in the transcript. The next Skill invocation of a different skill — say, process-research — is checked against that residue, reads as a routing mismatch, and is blocked. The hook fires correctly by its own logic; it is blocking the wrong thing. This misfire was reproduced live twice in consecutive sessions, each time blocking a process-research invocation that followed a workflow-based skill run.

**Silent enforcement-gate dropout — the hook simply does not fire.** A step-checker hook that scans for `process-*` skill invocations to trigger mandatory block-presence checks (scope block, QA report block). When the skill runs as a workflow, the `Skill` event is never emitted. The hook's scan returns no hit. No enforcement fires. A workflow-run skill can complete without emitting its mandatory output blocks, and the hook logs no complaint. The drop is entirely silent.

**Benign name-list mention — no behavior change.** Registry-style hooks that maintain allowlists of known skill and agent names. These mention `process-planning` in a list but do not branch on it. Whether the invocation came from a Skill tool or a Workflow tool is irrelevant to their logic. No misfire, no dropout.

## The Audit Method

Find every hook that contains a skill name and classify each hit by its firing condition:

```bash
grep -r "process-planning\|process-build\|process-research\|process-qa\|process-analysis" \
  .claude/hooks/ --include="*.py" -l
```

For each match, read the surrounding code and ask: **does the logic branch on whether the invocation was a `Skill` or a `Workflow` tool use?** If it branches only on `Skill`, classify by what happens when a `Workflow` with the same semantic meaning arrives:

- Does the hook fire on `Skill` only and take a consequential action (block, set a flag, reset state)? → **Misfire or dropout candidate.** Determine which by tracing the action: a block or state-reset on the presence of a matching name produces a misfire; a block or state-set on the *absence* of a matching name produces a dropout.
- Does the hook use the name only as an identifier with no conditional logic? → **Benign name-list.** No fix required.

Two specific patterns produce the hard misfire and the silent dropout respectively:

**Misfire pattern** — state-reset or routing-check keyed on `Skill` invocations:
```python
# fires on Skill tool_use; uses skill name to update routing state
if tool_name == 'Skill' and args.get('skill') in process_skill_names:
    last_process_type = ...  # or: clear routing context
```
When a `Workflow` tool_use carries the same semantic (a process skill running), this branch never executes. If the reset was the correct action, downstream Skill invocations run against stale state — producing the misfire.

**Dropout pattern** — gate-presence check keyed on `Skill` detection:
```python
# fires at Stop; requires a Skill event to have set a flag
for block in transcript:
    if block['tool'] == 'Skill' and block['args']['skill'].startswith('process-'):
        found_skill = True
# later: if not found_skill: return  — no enforcement
```
When the skill runs as a Workflow, `found_skill` is never set. The enforcement path is never entered. The hook silently passes every workflow-run skill invocation.

## The Fix Pattern

Treat a `Workflow` tool_use whose name or scriptPath basename resolves to a known process skill as semantically equivalent to that skill's `Skill` invocation, at every detection point.

For the misfire case — routing and state-reset hooks:
```python
def get_invoked_skill(block):
    """Returns the logical skill name for a Skill or matching Workflow invocation."""
    if block.get('tool') == 'Skill':
        return block['args'].get('skill', '')
    if block.get('tool') == 'Workflow':
        raw = block['args'].get('name', '') or os.path.basename(
            block['args'].get('scriptPath', '')
        ).replace('.js', '')
        if raw in KNOWN_PROCESS_SKILLS:
            return raw
    return ''
```

For the dropout case — gate-presence checks — add a parallel Workflow branch alongside the existing Skill branch. The flag (`found_skill`, `last_process_skill`, etc.) is set from either branch:

```python
skill_name = get_invoked_skill(block)
if skill_name.startswith('process-'):
    found_skill = True
    last_process_skill = skill_name
```

**One constraint that must not be crossed:** a Workflow invocation detected as a process skill must never arm sidecar-contract fallback mechanisms (like the post-compaction sidecar loader described in [Sidecar Files for Post-Compaction Enforcement](sidecar-files-for-post-compaction-enforcement.md)). The sidecar fallback was designed to enforce dispatch contracts when the transcript no longer contains a classification block. A workflow performs its dispatches internally — those dispatches are invisible to the main transcript by construction. Arming the sidecar fallback from a Workflow detection would demand that the workflow's internal agent calls appear in the main transcript, which is structurally impossible. The fix: Workflow invocations count as dispatches (the invocation itself is the dispatch guarantee) but do not set the sidecar-fallback trigger.

## Why This Is a Structural Bug Class

The hooks were written against a single invocation model: skills are invoked via the `Skill` tool. That assumption was valid when it was made. Converting skills to workflows does not change what the hook checks — it changes what the reality is. The gap between the assumption and the reality is the bug.

This is the same structure as [Wrong-Protocol Hooks Silently No-Op](wrong-protocol-hook-silently-noop.md): a hook's internal logic can be entirely correct while producing wrong outcomes because the surrounding context (the event type, the invocation path, the runtime's dispatch model) has changed. The unit tests continue to pass because they test the logic, not the assumptions about invocation shape.

Two properties make this class particularly hard to detect before conversion:

**It requires both a workflow and a subsequent Skill invocation in the same session.** The misfire only surfaces when a workflow runs and then a prose skill runs in the same turn. A session that uses only workflows or only prose skills never hits it. The first sessions after partial adoption — where some skills are workflows and others are not — are the highest-risk window.

**The dropout is self-concealing.** A hook that enforces nothing for workflow-run skills generates no block events, no error output, and no governance log entries that would distinguish it from a session where the hook correctly found nothing to enforce. The governance log looks identical whether the hook correctly passed a compliant session or silently skipped a non-compliant workflow run.

## Evidence

- **Hard misfire reproduced live twice** — process-research blocked by skill-routing-check after process-planning ran as a workflow, on two consecutive sessions before the fix shipped (vault-internal).
- **Silent dropout identified by audit** — process-step-check Skill-detection branch traced; no Workflow branch present before the fix; SCOPE enforcement confirmed absent for workflow-run skills.
- **Fix shipped and tested** — routing-check Workflow-boundary reset, process-step-check Workflow branch with real-user-vs-tool_result-wrapper turn-boundary distinction, work-verification-check parallel Workflow detection; test counts increased across all three hooks; all pre-existing tests remain green.

## Related

- [Sidecar Files for Post-Compaction Enforcement](sidecar-files-for-post-compaction-enforcement.md) — the sidecar mechanism that must NOT be armed from Workflow detection
- [Wrong-Protocol Hooks Silently No-Op](wrong-protocol-hook-silently-noop.md) — the analogous bug class where the hook's wire format, not its invocation detection, is the wrong assumption
- [Procedure Layer as Workflows](../specs/procedure-layer-as-workflows.md) — the conversion program that exposes this class at scale
- [Workflow-Enforcement First-Contact Bugs](workflow-enforcement-first-contact-bugs.md) — the complementary set of harness-level invariants from the same adoption arc
