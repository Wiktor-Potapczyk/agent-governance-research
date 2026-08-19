# A Splice That Doubles a File Ships Green

A publication pipeline merges private working files into their public counterparts, and one helper spliced public-only function bodies into the merged output by extracting them with a regular expression. The extraction pattern's terminator was written as `.*$` with the DOT-ALL flag set. Under DOT-ALL, the dot matches newlines, so `.*$` runs to the last line-end of the file: every extracted "block" was actually definition-through-end-of-file, and every splice appended the public file's entire tail onto itself.

## The Finding

Four published hooks at the public repository's HEAD carried their whole body twice. One 489-line file contained `main()` twice, along with a second copy of every other definition. It parsed, imported, ran, and passed its tests, because Python resolves duplicate top-level definitions by letting the later one win: the second copy of each function shadowed the first, the shadowing copies were the intact originals, and the suite exercised them green. The defect shipped silently and sat on a public default branch for two weeks. It was found only when the next sync wave rebuilt the splice tooling and inspected what the extraction regex actually returned, not by any gate.

The fix was mechanical once seen: the terminator became `[^\n]*`, which cannot cross a line boundary, and blocks were read from the committed HEAD version rather than the working tree, so a previously doubled file could not feed its own duplication forward into the next merge. The four affected files were restored to a known-good state and re-merged single-copy, one body each.

## Why Every Gate Passed

Walk the gate chain and the silence is structural, not sloppy:

- **The parse gate** saw valid Python, because a duplicated module is exactly as syntactically valid as a single one.
- **The test gate** saw identical behavior, because later definitions win and the later copies were correct. There is no assertion a duplicate body can fail unless a test asserts single definition or file shape.
- **The token gate** (the privacy scan) saw the same token set as the original, because duplication introduces nothing new, only more of the same.
- **Human review** saw the top of the file, which was right. Nobody scrolls to line 489 of a file they expect to be 280 lines, because nothing suggested there was a line 489.

Validity-class checks, parses, passes, contains no forbidden strings, are all invariant under duplication. Only a shape-class check breaks the symmetry: a line count compared against the source, or an assertion that each top-level name is defined exactly once.

There is a small regex lesson embedded too: flags rewrite semantics at a distance. `.*$` is a harmless idiom in line mode and an unbounded consumer in DOT-ALL mode, and the flag lives far from the pattern that it detonates. An extraction regex needs a terminator that structurally cannot cross the boundary it is supposed to respect, regardless of flags in force.

## The Rule

Gates that check validity cannot see duplication, because a doubled artifact is exactly as valid as a single one. Any tool that composes files must have its output checked for shape, not just validity: expected size against the inputs, each definition present exactly once, extraction results eyeballed or asserted at build time. And when a composition tool is found defective, re-derive its outputs from committed history, not from the working tree, or the defect's products become the next run's inputs.

## Related

- [A Gate That Cannot Fail Is Not a Gate](a-gate-that-cannot-fail-is-not-a-gate.md), the general class this instance belongs to: green while structurally unable to object
- [A Guarded Optional Import Ships Two Programs](guarded-optional-import-is-two-programs.md), the sibling case of shipping code no test executed
- [A Published Mirror Is a Fork, Not a Copy](a-published-mirror-is-a-fork-not-a-copy.md), the merge model this splice tooling serves
