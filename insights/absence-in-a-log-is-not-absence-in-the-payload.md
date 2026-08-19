# Absence in a Log Is Not Absence in the Payload

A governance suite needed to know whether the tool-call events its hooks intercept carry an agent-identity field, so that a guard could tell a sub-agent's write from the main session's. It had almost thirty thousand archived log records bearing on the question, and they gave a clean, well-evidenced, wrong answer.

## The Finding

A careful read-only research pass examined the one hook in the suite that logged the field at that event type: 29,445 archived records. Every record carried the identity field, but with only one value, the single reviewer agent that hook watched. The session-id field was absent in 100 percent of the sample. A second id, needed to correlate the event with its dispatch, appeared in zero records at that event type across the whole log. The research verdict, stated with appropriate hedging and an explicit UNVERIFIED list: reliable discrimination is not possible at this event type today; the field's presence outside the one observed case is an assumption, not a fact.

The next day, a metadata-only probe, roughly thirty lines, logging just the payload's key list, one field's value or an explicit ABSENT marker, and the tool name, was registered on the same event. It took effect on the very next tool call, no restart, and settled the question within hours: sub-agent tool calls carry the identity field populated with the agent's own name, for every dispatch shape observed, workflow workers and directly dispatched agents alike. Main-session calls carry no such key at all. The payload even carried both ids the archive had shown as absent or never-present. The platform discriminated better than the archive suggested was possible.

## Why the Archive Misled

The archive was not wrong about itself. It was wrong about the world, because a log is a projection: it records the fields its writers chose to write, at the moments the writers' own conditions fired. Every one of those 29,445 records came from one hook that logged only when it was about to block, and only for the three agent names it watched. The uniform field values were the hook's filter, not the payload's shape. Absence of a field across N records proves the writers never wrote it, never that the events never carried it.

Volume makes this worse, not better. Thirty thousand records feel like evidence about the platform, but sample size multiplies confidence, not coverage. The research pass did everything right short of new instrumentation: it read the writer sources, counted the records, refused to over-claim, and flagged the gap explicitly. The conclusion still under-claimed the platform, because no amount of archived data can answer a question its writers never asked.

## What Worked

A probe with three properties: metadata only (key names, one value-or-ABSENT marker, no content, no prompts, no file bodies), registered directly on the event in question, and left in place until each distinct call shape had produced a real record of itself. Each shape was answered by an actual event of that shape, not by inference from a neighboring one. Total cost: about thirty lines and one day of an extra process start per matching tool call.

## The Rule

Treat archived telemetry as evidence about its writers, and only its writers. When the question is "what does the event carry," instrument the event: a field absent from every log record is a fact about the loggers, and the thirty-line probe that asks the payload directly is cheaper than the carefully hedged wrong verdict built on the archive.

## Related

- [State Derived From a Transcript Is Not State](state-derived-from-a-transcript-is-not-state.md), a check reading a surface that structurally cannot show it the answer
- [A Safety Gate's Own Audit Log Is Mostly Its Test Suite](safety-gate-logs-are-mostly-your-own-tests.md), the sibling failure where the log misrepresents the world in the other direction
- [Research Gatherers Reconstruct From Training Memory Unless a Live-Citation Gate Catches It](research-gatherers-reconstruct-from-training-memory.md), the same "absence of recognition is not absence" confusion inside a single forward pass
