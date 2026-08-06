# Commit Identity Is Two Fields, and Clone Copies Neither

Every commit carries **two** identities: an author and a committer. Most tooling shows you the first. A check that validates only the first will pass a commit whose second field is wrong, and the second field is the one that quietly inherits whatever the machine is configured with.

## The Finding

A commit was amended to remove sensitive content from a published repository. The amend explicitly preserved the author and both timestamps. It set nothing else.

The result was pushed with the **committer** field reading a work email address, on a public commit, in a repository maintained under a personal identity. The operation intended to remove a disclosure created a different one in the same step.

It was caught by a human opening the commit on the hosting site. **No gate caught it**, because the pre-push identity check inspected the author field, which had been preserved correctly and looked right.

## The Two Mechanisms

**First: the fields are independent, and the defaults are asymmetric.** Amending or rewriting with an explicit author does not set the committer. The committer is filled from configuration at write time, silently, every time.

```bash
# insufficient: sets one field
git commit --amend --author="Name <personal@example.com>"

# sufficient: sets both
GIT_AUTHOR_NAME="Name"  GIT_AUTHOR_EMAIL="personal@example.com" \
GIT_COMMITTER_NAME="Name" GIT_COMMITTER_EMAIL="personal@example.com" \
git commit --amend --no-edit
```

**Second: a clone does not carry per-repository configuration.** If the global identity is a work address and each sensitive repository is protected by a local override, then that protection exists only in the working copies where somebody set it. A fresh clone, made to do a history rewrite safely in isolation, inherits the **global** value and none of the overrides. The very act taken to reduce risk was the act that removed the protection.

This is the trap in compressed form: **the safety measure lived in the copy, not in the repository.** Anything reproduced from the remote starts unprotected.

## The Rule

**Verify both fields, across every commit, and make the check fail hard rather than warn.**

```bash
git log --format='%ae|%ce' | sort -u
```

One line of output, and it is the address you expect. More than one line, or the wrong address, is a defect. Run it after any history operation and before any push. It is cheap enough to run unconditionally.

For the clone problem, the durable fixes in increasing order of reliability:

1. Set the local override immediately after cloning, as part of whatever procedure creates clones.
2. Remove the risky value from the global configuration entirely, so the failure mode becomes a missing identity (which halts loudly) rather than a wrong identity (which proceeds silently). Configuration exists for exactly this: refusing to guess an identity is a supported setting.
3. Where the hosting platform supports it, reject pushes whose commits carry addresses outside an allowed set. This is the only version that survives a machine you did not configure.

Option 2 is the one to reach for. **Prefer a configuration whose failure mode is a stop over one whose failure mode is a plausible wrong answer.**

## The Naming Trap

A check existed in this system named for credential scope. Its name reads as though it covers identity. It contains zero references to identity, and the two concerns are genuinely distinct: which credential authenticates the push, and which name is written into the commit object.

**A check's name is a claim about coverage, and readers will act on the claim.** This one produced a reasonable belief that identity was guarded when nothing guarded it. Where a check's scope is narrower than its name suggests, the name is the bug.

## Related

- [Token Scans Cannot See Infrastructure Disclosure](token-scans-cannot-see-infrastructure-disclosure.md), the same publication pass, a different blind spot
- [A Gate That Cannot Fail Is Not a Gate](a-gate-that-cannot-fail-is-not-a-gate.md)
- [Deny Patterns Fail on Command Spelling](deny-patterns-fail-on-command-spelling.md)
