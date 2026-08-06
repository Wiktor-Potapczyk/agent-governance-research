# Token Scans Cannot See Infrastructure Disclosure

A pre-publication scanner built around a list of forbidden strings will find every forbidden string and nothing else. That sounds tautological until you notice what is not on the list: an IP address, a `root@` login, a hostname, a container name, a deployment path, a product name. **Every one of those is a zero-token string.** They match no secret pattern, contain no credential, and pass a clean scan by construction.

## The Finding

A repository published under a personal account carried, for over a week and across a passing gate on every commit, a line containing a production server's IP address with a root login, plus eighteen occurrences of an internal product name spread across three files.

The scanner was working correctly. So was a second, independently written gate applied during the same publication. **Neither could see any of it,** because the material was not a token from any denylist. It was ordinary-looking test fixture data that happened to describe real infrastructure.

The same publication pass also admitted, into the working tree, a file containing an SSH key path, a container name, a deployed hostname, and a set of absolute deployment paths. It was caught by a human reading the diff, not by either gate.

## Why the Category Is Systematically Missed

A denylist scanner asks: **does this text contain a known-bad string?** Disclosure of this kind is not a string, it is a **shape**:

| Shape | Example form | Why a token list misses it |
|---|---|---|
| Network address | four dotted integers | matches no keyword; appears legitimately in tests |
| Privileged login | `root@`, `admin@` followed by a host | ordinary syntax |
| Internal hostname | a subdomain of a domain you own | the domain may not be on the list, and often should not be |
| Deployment path | an absolute path under a service root | paths are everywhere in a codebase |
| Product or project name | a plain English word | on no list, and probably unlistable |

Some of these cannot be listed even in principle. **Putting the sensitive identifiers into the scanner's own configuration would publish them the moment the scanner ships**, which is why the scanner in this case was itself unpublishable: it *is* the denylist. A gate whose contents are the secret cannot be distributed with the artifact it guards.

## The Rule

**Grep the shape, not the token.** A structural sweep over added lines, run alongside the token scan rather than instead of it:

```
(\b\d{1,3}(\.\d{1,3}){3}\b)      # bare IPv4
|((root|admin|deploy)@[\w.-]+)    # privileged login targets
|(\b/(opt|srv|var/www)/[\w./-]+)  # deployment paths
|(ssh\s+[\w.-]+@)                 # remote shell invocations
```

This produces false positives. `127.0.0.1`, `0.0.0.0`, and documentation ranges will match, and they should be allowlisted explicitly rather than by loosening the pattern, because [narrowing a deny pattern silently opens floor holes](narrowing-a-deny-pattern-opens-floor-holes.md). A structural sweep that fires on a handful of benign lines per release is doing its job; one that never fires is back to being [a gate that cannot fail](a-gate-that-cannot-fail-is-not-a-gate.md).

Product and project names cannot be pattern-matched. They need a maintained list, and the honest position is that this part of the check is a human diff review with a checklist, not an automated gate.

## A Complication Worth Anticipating

In this case the internal product name could not simply be renamed everywhere, because one occurrence was the literal key of a safety-rule exemption. The string was **matching logic, not a comment**: renaming it changed behaviour. Genericization of this class is therefore a code change requiring test coverage, not a find-and-replace.

Design consequence: **avoid putting real internal identifiers into positions where they become semantics.** An exemption keyed to a configurable value, read from settings, would have made the rename free.

## The Standing Caveat

A clean token scan is **necessary and never sufficient.** Treating it as sufficient is the actual defect here, and it is a reasoning error rather than a tooling one: the gate's passing was read as "this artifact is safe" when it only ever meant "this artifact contains no listed token."

And once published, **remediation does not retract.** Rewriting history removes the material from the branch; it does not remove it from forks, from caches, or from an object store that keeps unreachable objects addressable by hash for a period. If the disclosed infrastructure matters, the fix on the host side matters more than the fix in the repository.

## Related

- [A Gate That Cannot Fail Is Not a Gate](a-gate-that-cannot-fail-is-not-a-gate.md)
- [Narrowing a Deny Pattern Opens Floor Holes](narrowing-a-deny-pattern-opens-floor-holes.md)
- [Untested Surface Inventory](../patterns/untested-surface-inventory.md), the same discipline applied to what a check does not cover
