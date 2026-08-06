# Deny Patterns Fail on Command Spelling, Not on Command Meaning

A safety rule written as a regular expression over a command line blocks a **spelling**. The operation it is meant to prevent usually has several, and the ones your rule misses are invisible until someone uses them.

## The Finding

A hard block existed on rewriting published history. Its pattern required the program name and the subcommand to be adjacent:

```
\bgit\s+push\s+.*--force
```

The same operation, run from another directory, is spelled:

```
git -C /path/to/repo push --force
```

The `-C` option sits between `git` and `push`, so the pattern does not match, and **the block does not fire**. The operation is identical. The protection is absent.

This was not found by review. It was found by predicting out loud that the guard would stop an imminent action, running the action, and watching it succeed. The prediction was wrong in the direction that matters.

Two details make it worse rather than merely unlucky:

- **The correct pattern already existed ten lines away.** A neighbouring rule covering ordinary pushes was written with an optional-options allowance. The weaker rule was guarding the more dangerous action, purely because the two lines were authored at different times by different reasoning.
- **The project's own documentation recommended the evading spelling.** A prior operational note advised using the `-C` form for reliability reasons in a different context. The guidance and the guard were in direct, silent conflict, and the guidance won because it was the one people read.

## Why This Class Recurs

Command-line tools are deliberately generous about surface form. For a single operation you routinely have:

- **Option placement.** Global options before the subcommand, subcommand options after, and often both accepted in either position.
- **Short and long forms.** `-f` and `--force`, `-C` and a `cd` beforehand.
- **Equivalent constructions.** `--force-with-lease` for a related and also-destructive operation; a `cd` in a compound statement instead of a directory option; an alias; a wrapper script; a variable holding the binary path.
- **Configuration reaching the same end.** A push rule set in configuration rather than passed on the command line.

A regular expression enumerates a subset of these and silently permits the rest. **The set of spellings is open; your pattern is closed.**

## The Rule

**Write the deny against the invariant part, and prove the variants.**

1. **Anchor on what cannot vary.** For this case the subcommand and the dangerous flag are the invariant; the program name, its global options, and the working directory are not. Requiring adjacency of two tokens that the tool explicitly permits separating is the bug.
2. **Enumerate the equivalent spellings you know of, and test each one against the live guard.** Not against your reading of the pattern: against the guard, executed. This is [arming the control](a-gate-that-cannot-fail-is-not-a-gate.md), applied per-variant.
3. **When you add a rule, audit its siblings.** These patterns accumulate one incident at a time and drift apart. The neighbouring rule here was correct; the divergence was never noticed because nothing compared them.
4. **Diff the guidance against the guard.** Any documentation recommending a command form should be checked against the rules that are supposed to constrain it. A recommended bypass is worse than an undocumented one, because it is the form people will actually type.

## The Structural Limit

Pattern-matching a command string is fundamentally an approximation of intent, and it will always be one. A wrapper, an alias, an environment variable holding the binary, or a script invoked by name can express the operation with none of your tokens present.

This is a reason to place the real floor where the operation happens rather than where it is typed, when that option exists: a server-side rule rejecting non-fast-forward updates cannot be spelled around by any client. The command-line guard is then a fast local warning, not the last line, which is a far more honest description of what a regular expression over a shell string can actually deliver.

## Related

- [Narrowing a Deny Pattern Opens Floor Holes](narrowing-a-deny-pattern-opens-floor-holes.md), the sibling failure: relaxing a pattern to cut false positives un-blocks things nobody intended
- [A Gate That Cannot Fail Is Not a Gate](a-gate-that-cannot-fail-is-not-a-gate.md)
- [Regex Hardening](../specs/regex-hardening.md)
- [Hook Signal vs Cause](../patterns/hook-signal-vs-cause.md)
