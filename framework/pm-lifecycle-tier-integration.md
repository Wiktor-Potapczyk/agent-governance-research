# QA Tiers Mapped to PM Lifecycle Phases

## The Integration

The three-tier QA model maps directly onto the PM lifecycle phases. Each tier fires at a specific lifecycle moment.

| PM Phase | Lifecycle Moment | QA Tier | What Fires |
|----------|-----------------|---------|------------|
| Phase 2: Build | Task completion | Tier 1 | QA REPORT per task — falsify claims before marking done |
| Phase 2: Build | Increment completion (all shaped items done) | Tier 2 | PENTEST REPORT — exhaustively try to break the increment |
| Phase 3: Review | Milestone review | Tier 3 | Eval suite (promptfoo or equivalent) — systematic trap cases |

## Where in the Build Loop

The Phase 2 increment loop with QA tiers integrated:

```
1. Pull shaped item
2. Delegate to agent
3. Build
4. Review (quality assessment by different agent)
5. Tier 1 QA (test claims, produce QA REPORT)
6. Mark done
7. IF all items done → Tier 2 Pentest (try to break everything)
8. Checkpoint
9. STOP — evaluate before next item
```

Tier 2 fires between "all items done" and "checkpoint." It is the integration testing step that the original lifecycle lacked.

## Where in the Review Phase

Phase 3 Review with Tier 3:

```
1. Compare output vs original pitch
2. Quality review (architecture reviewer / prompt engineer)
3. Tier 3 Eval (human runs eval suite against milestone output)
4. Capture lessons
5. Decide: ship / polish / extend / kill
```

Tier 3 fires between "quality review" and "capture lessons." It is the systematic regression testing step. Human-triggered because eval suite design requires judgment about which trap cases matter.

## The Composition Note

QA tiers compose upward. A missing Tier 1 on any task makes Tier 2 incomplete. Tier 2 artifacts feed Tier 3. No tier is skippable.
