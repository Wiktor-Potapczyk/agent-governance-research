# Workflow-Enforcement First-Contact Bugs

Converting a prose process skill into a deterministic workflow script makes dispatch happen by construction — and immediately surfaces a class of bugs that the prose-skill path never could. These are not implementation mistakes; they are structural properties of the harness that only become visible when the first real runs execute. Five findings from the adoption of two process-skill workflows.

## The Finding

Wiring a deterministic workflow layer over an LLM procedure exposed five engineering invariants. Three are harness-level constraints (how the Workflow tool delivers arguments, how named-workflow invocation resolves scripts, what resume means). Two are design patterns forced by those constraints (the file contract for disk-writing steps, the enforcement gates' behavior on failure paths). All five transferable to anyone building workflow-enforced procedure over an LLM agent harness.

---

### 1. Args Are Delivered as a JSON String, Not an Object

The Workflow tool passes `args` to the script. The natural assumption is that an object literal `{project: "foo", goal: "bar"}` arrives as an object. It does not — it arrives as its JSON-serialized string `'{"project":"foo","goal":"bar"}'`. A script with a TypeScript-style object-only guard:

```javascript
if (typeof args !== 'object') return { status: 'halted-malformed-args' };
```

silently discards the caller's data. `typeof '{"project":"foo"}'` is `'string'`, not `'object'`. The condition triggers, the guard returns halt, and the script proceeds with `project = undefined`, `goal = undefined`.

The first two acceptance runs on a freshly adopted workflow each consumed approximately 400K subagent tokens on fully degenerate input — the scope agent produced a no-context scope block, both reviewers returned `REQUEST_CHANGES` on precondition failure, and the quality gate derived `pass=false` from disk evidence (Glob confirming no plan file). The enforcement gates held correctly; the waste was entirely on the input path.

The fix is a parse-if-string guard at the top of every workflow script, before any field access:

```javascript
if (typeof args === 'string') {
  try { args = JSON.parse(args); } catch { /* fall through to validation */ }
}
```

Paired with an input-validation HALT before the first agent spawn: if required fields (`project`, `goal`, etc.) are missing, return `{ status: 'halted-malformed-args', hint: '...' }` immediately. A malformed dispatch then costs approximately zero tokens. Without the HALT, it costs one full workflow run.

**Implication for callers:** the string delivery is not a bug to fix in the harness — it is a stable property. Every script in the layer must implement parse-if-string + required-field HALT as a first step.

---

### 2. Named-Workflow Invocation Resolves From a Session Cache

Invoking a workflow by name — `{name: "process-planning"}` — resolves the script from the session's cached workflow registry, not from disk at invocation time. A script edited mid-session is not visible to a `{name}` invocation until the session restarts and re-indexes the cache.

This means a workflow that was edited, corrected, or hardened during the same session that adopted it will run the *stale pre-edit version* if invoked by name. Three acceptance runs executed the same stale input-validation bug because the fix was applied mid-session and the name resolution kept serving the pre-fix script.

The rule: **use `scriptPath` always, never the cached workflow name.** The thin-invoker stub in the skill's `SKILL.md` must route through `scriptPath` pointing to the absolute or vault-relative path:

```
Invoke via Workflow tool: {scriptPath: ".claude/workflows/process-planning.js", args: {...}}
```

`scriptPath` reads from disk at invocation time. It is not affected by the session cache. This is the one constraint that makes script-pinned invocation reliable regardless of mid-session edits.

---

### 3. Workflow Resume Is Same-Session-Only

A workflow that halts or is interrupted mid-run does not accumulate durable state between sessions. Resume (`--resume`) operates within a single session's context. There is no cross-session checkpoint.

Design consequence: every workflow step must treat its inputs as ephemeral. Steps that write artifacts to disk are the correct persistence boundary — the file is the checkpoint, not the workflow's internal state. A workflow that needs to be resumable across sessions must be designed so each step reads its preconditions from disk artifacts written by earlier steps, not from in-memory variables.

For the procedure layer specifically: adoption means each converted skill gets a thin-invoker stub that passes scope data as explicit args. The scope-to-plan-to-review chain carries its state through the file written by the plan step, not through Workflow-internal variables. This is already the right design for other reasons (the file contract; evidence-based quality gates) — resume-is-same-session-only reinforces it.

---

### 4. Write-Restricted Agent Types Fabricate File Paths

The `implementation-plan` agent type — and others with restricted tool surfaces — can return a file path it claims to have written while having written nothing. The restriction blocks the Write tool, so the agent cannot fulfill the write step. It does not error; it returns a plausible-looking path in its response. The file does not exist on disk.

This caused an acceptance-run failure: the design step dispatched `agentType: 'implementation-plan'`, the agent returned a path, both reviewers received the path as the claimed artifact, both reviewers then attempted to verify the artifact and blocked because it did not exist on disk. The failure was caught — but only because the reviewers were given a file-path contract and checked it.

The fix has two components:

**Writer steps must use the default workflow subagent** — no `agentType` that restricts the Write tool. The `implementation-plan` role belongs in the prompt, not the type:

```javascript
const result = await agent({
  // no agentType — default subagent has full tool surface
  prompt: `You are acting as an implementation plan author. ...
           FILE CONTRACT: write the plan to exactly ${outputPath}.
           After writing, verify by reading back ${outputPath} and return the path.`
});
```

**The file contract must be explicit and non-negotiable.** Every step that produces a disk artifact carries three obligations in the prompt: (1) write to exactly the specified path, (2) verify by reading back the written file, (3) return the exact path in the structured response. The script then confirms existence independently before downstream steps consume it. An agent that cannot satisfy the file contract because its tool surface is restricted will surface the failure at the contract-check step rather than silently returning a fabricated path.

---

### 5. Enforcement Gates Held Through Every Failure

The five bugs above all triggered real failure paths. In each case, the enforcement gates derived their verdict from disk evidence, not from self-reported output:

- The args-string runs: quality gate computed `pass=false` from a Glob scan confirming no output file existed.
- The named-cache runs: same failure path, same derivation.
- The write-restricted agent run: reviewers blocked because they attempted to Read the claimed path and got a file-not-found error.

Zero fabrication passed a gate. The gates produced correct verdicts on the negative path — which is exactly when enforcement gates matter most, since positive paths can be verified by inspection.

This is the load-bearing result for anyone considering a workflow-enforced procedure layer: the enforcement structure is what makes the first-contact bugs recoverable. Without gates that check disk evidence rather than trusting a self-reported pass, each of these runs would have produced a governance log entry claiming success while producing no real artifact.

The gates held not because the bugs were anticipated, but because the gate design is structurally independent of the agent's behavior. The quality gate reads the filesystem; the agent cannot influence what is on the filesystem by generating the right words.

## What This Means for Workflow-Enforced Procedure

Three engineering rules transfer directly:

1. **Parse-if-string + required-field HALT, always, at the top of every script** — treat string delivery as a permanent API property, not an edge case to handle defensively.
2. **scriptPath always, never cached name** — the difference between invoking stale or live code; one rule change, permanent reliability.
3. **File contract on every disk-writing step, default subagent only** — the structural intervention that makes write-restricted fabrication visible at the contract-check step rather than invisible.

The fourth rule is a design principle, not a code line: **enforcement gates must derive their verdict from evidence, not from agent self-report.** The gates that held through five failure modes held because they read the filesystem. Any gate whose passing condition can be satisfied by generating the right words will eventually be satisfied by generating the right words on a run that produced nothing.

## Related

- [Workflow Sub-Agents Have the Full Tool Surface](workflow-subagents-have-full-tool-surface.md) — the capability baseline that makes execution-evidence gates possible
- [Procedure Layer as Workflows](../specs/procedure-layer-as-workflows.md) — the program this adoption documents
- [Rubber-Stamp Enforcement Gaps](rubber-stamp-enforcement.md) — the general pattern of checking output text rather than actual execution
- [Measure Then Gate](measure-then-gate.md) — why the first-contact failures were recoverable: gates were derived from evidence, not intuition
