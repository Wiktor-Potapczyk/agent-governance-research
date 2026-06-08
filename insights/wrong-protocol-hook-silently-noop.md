# Wrong-Protocol Hooks Silently No-Op

A hook can enforce nothing while appearing to enforce everything. The failure mode: the hook emits a block decision using the wrong wire format for its event type. The runtime silently ignores the decision. The hook logs it as a block. Dashboards show it as active. The behavior it was meant to suppress continues undetected.

## The Finding

Hook protocol correctness is invisible to unit tests that check the hook's logic but not its wire format against the actual event contract. A hook that would correctly compute "this should be blocked" can still be a no-op if it sends that decision via a protocol the runtime doesn't honor for that event type.

One specific failure pattern: a PreToolUse hook that emitted a block decision using the SubagentStop block-protocol shape. The runtime's SubagentStop handler honors that shape; the PreToolUse handler does not — it silently ignores any output from a hook that doesn't match the PreToolUse response contract. The hook:

- fired on every matching tool use (correct)
- computed the right blocking condition (correct)
- self-logged a "blocked" event to the governance log (actively misleading)
- was referenced in governance dashboards as an active control (wrong)

The tool use proceeded on every invocation. The hook was a 14-day no-op.

## Why Unit Tests Don't Catch This

A unit test exercises: "given this input, does the hook produce the right decision?" It does not exercise: "does the runtime honor this decision for this event type?" Those are two different questions. The hook can pass all its tests and still be dead in production because the test mocks the runtime's response, not the actual event contract.

The gap is the same gap that [rubber-stamp enforcement](rubber-stamp-enforcement.md) names at the output level — checking the artifact, not checking that the action ran. Here the artifact is the hook's decision output; the action is whether the runtime enforced it.

## The Verification Rule

A blocking hook is only verified when you observe it actually block in a live run — not when its unit tests pass, not when it appears in a governance log, not when it self-reports a block decision.

The practical check: run a deliberate violation of the hook's condition in a real session and confirm the action is rejected. This takes one test execution. Without it, you have evidence the hook fires; you have no evidence the hook enforces.

## The Broader Pattern

This is a specific instance of the [measure-then-gate](measure-then-gate.md) principle: enforcement that isn't verified against real runtime behavior carries cost (it's listed as a control, it occupies governance dashboard space, it creates false confidence about coverage) while contributing zero benefit. A silently-dead blocking hook is worse than no hook — no hook at least doesn't create false assurance.

For any blocking hook: the deployment checklist includes one live-fire test. "Tests pass" is a necessary condition. It is not sufficient.
