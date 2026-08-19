# Write the Ignore Rule Before the Artifact

A full-text search index over 5,129 agent-conversation transcripts, 2.4 GB of unscrubbed text including anything any past session pasted, was to live inside a repository that an automated task commits every 30 minutes, staging everything it finds. The interesting design constraint was not the indexer. It was that the environment's own automation is the adversary: any window between "the index exists" and "the index is ignored" is a window in which the sweeper can commit it, and a commit is history, so losing that race once is losing it permanently.

## The Finding

The build made ordering the control. The `.gitignore` entry for the index directory was written and verified before any indexer code existed on disk, so no code capable of creating the artifact predated the rule that contains it. The sequence was ignore rule, verify, code, index, and the property held through a live test nobody scheduled: the 30-minute sweeper fired mid-build and swept none of the index. Containment was then verified structurally, not by absence of complaints: `git check-ignore` exits zero on the index path, `git ls-files` under the path returns nothing, and `git log --all` for the path is empty, meaning no commit in any ref has ever contained it.

Two supporting decisions carried the same discipline:

**No scrubbing at index time, stated loudly.** The owner's ruling places the privacy gate at public push; vault-local storage is unrestricted. So the index deliberately contains unscrubbed transcript text, and the compensating rule is written into the containment contract: anything transcript-derived that moves toward any public repository passes the same pre-push scrub as quoting the transcript directly. A boundary that is explicit about where it is not enforcing is auditable; one that half-scrubs everywhere is not.

**Read-only proof over the corpus.** Indexing must never write to what it reads. Six hash comparisons proved it: full digests on three closed transcripts, including a 401 MB file, byte-identical before and after; prefix digests on three live, still-growing files, unchanged over the originally scanned range. Even the build's one crash modified nothing, and the crash itself was a finding: a JSON escape for half an emoji surrogate pair decodes into text that cannot re-encode to UTF-8 at storage time. The corpus-wide follow-up separated that from real damage: 0 lines of true disk corruption in 5,129 files; 5,896 flagged lines were replacement characters that past sessions had legitimately logged into their own transcripts.

The tool ships its epistemics in its own help text: transcript hits are recall, not evidence, ranking below the live system and current files; a transcript that contradicts the live system is a prompt to re-check the live system, never a citation.

## Ordering as the Control

A protection that depends on remembering to apply it before some other actor acts is not a protection, it is a race with a to-do list. Where an automated committer, publisher, or sync loop shares your working tree, the only reliable form of "this must never be committed" is "the ignore rule existed before the artifact could." The same logic generalizes: create the guard, prove the guard is live, then create the thing it guards. Any other order contains a window, and automation is patient.

## The Rule

When an automated publisher shares your working tree, containment is step zero, not cleanup: write the exclusion rule before writing the code that can create the artifact, verify the rule structurally (ignored, untracked, absent from all history), and if the artifact deliberately holds sensitive content, write down exactly where the enforcement boundary sits so every future consumer inherits the rule instead of rediscovering it.

## Related

- [A Published Mirror Is a Fork, Not a Copy](a-published-mirror-is-a-fork-not-a-copy.md), the publication boundary this containment contract feeds into
- [State Derived From a Transcript Is Not State](state-derived-from-a-transcript-is-not-state.md), why the tool demotes its own results below the live system
