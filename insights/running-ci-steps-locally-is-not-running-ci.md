# Running CI's Steps Locally Is Not Running CI

Re-running a workflow's commands in your own shell verifies the **commands**. It does not verify the **environment**. Those are different claims, and only the first one is yours to make from a local terminal.

## The Finding

A previously-disabled continuous-integration step was enabled. All of the workflow's steps were then run locally, in order, and they passed. The result was reported as "full local CI reproduction green on all steps."

Two pushes later the runner had failed both times, on the step that had just been enabled.

**The first cause was that the workflow never installed the test runner.** It used a setup action that provides a clean interpreter. The other steps passed precisely because they were standard-library only, and that contrast is exactly the signal that isolates the problem. The local machine had the runner installed years ago, so the local "reproduction" was structurally incapable of seeing the gap.

**The second cause was platform-specific.** A fresh clone of the pushed remote passed locally, every file was committed with consistent line endings, and the sole optional import was guarded. The failing environment was a different operating system, and the machine doing the verifying could not run it: hardware virtualization was disabled at the firmware level, so no container runtime and no virtual machine of the target platform was available at all.

## What a Local Pass Cannot See

- **Packages the runner does not have.** The workflow file is the dependency manifest. Your machine is not.
- **The operating system,** and everything that follows from it: path semantics, case sensitivity, line endings, available shells.
- **A clean checkout,** if your working tree carries untracked artifacts, caches, or state files that the code quietly depends on.
- **Environment variables** set in your shell profile and nowhere else.

Each of these is invisible from inside the environment that has them. That is what makes the false confidence so easy: nothing looks wrong, because everything that is missing is present.

## The Rule

Say "the steps pass locally." Do not say "CI reproduces green." The second is a claim about a machine you did not run.

**When the target platform is unreachable, CI is not a formality. It is the only oracle.** Treat its first red as the verification step rather than as a surprise, and do not claim green on its behalf beforehand.

## Practical Consequences

- **Before enabling a CI step that needs a package, read the workflow and confirm it installs it.** This is a five-second check that would have caught the first cause outright.
- **Reproduce against a fresh clone of the remote, not your working tree.** That catches the clean-checkout class even when it cannot catch the platform class.
- **Budget for the round trip.** Each blind guess costs a push and a full run. When the failing output is not readable from your environment (log endpoints commonly require authentication that a local script does not have), ask for it to be pasted rather than iterating on hypotheses. One paste resolved in a single step what several tool calls of elimination had not.

## The Broader Pattern

This is the environment-level instance of a general rule about verification: **a check performed inside the conditions being questioned cannot question them.** The local run assumes the local environment; that assumption is the thing under test, so the test is circular.

The same shape appears whenever a verifier shares state with the thing verified: a hook that validates its own output format, a test that mocks the interface it is meant to exercise, an agent that grades its own work. Independence is not a nicety in any of these. It is the property that makes the result mean anything.

## Related

- [A Guarded Optional Import Ships Two Programs](guarded-optional-import-is-two-programs.md), the branch-level instance, and the defect this exact failure uncovered
- [A Gate That Cannot Fail Is Not a Gate](a-gate-that-cannot-fail-is-not-a-gate.md)
- [Test Ground Truth](../patterns/test-ground-truth.md)
