# Safety-Gate Logs Are Mostly Your Own Tests

A governance system that logs every blocked action produces exactly the dataset you want for calibration: which rules fire, how often, and against what. That dataset turned out to be roughly 98.7% synthetic. Of approximately 8,000 recorded deny events from the Gate-1 shell guard, only about 105 came from a real agent session.

The rest were the hook's own test suite, running against the same log the production hook writes to.

## The Finding

Any enforcement hook worth having gets a test suite, and a test suite for a deny-gate works by triggering denials. If the hook writes its audit record unconditionally, every test run deposits synthetic events into the same file that production events land in. Run the suite in CI, in pre-commit, and locally while iterating, and the synthetic events outnumber the real ones by roughly two orders of magnitude within weeks.

The failure is not that the log is noisy. It is that the log is *confidently* noisy: the synthetic entries have the same schema, the same fields, and the same apparent authority as real ones. Nothing about an individual record announces which kind it is.

## Why This Is Worse Than Ordinary Noise

Calibration questions are exactly the questions this log should answer:

- Is this deny pattern too broad? Look at how often it fires.
- Which rules never fire and could be retired? Look at the zero-count rules.
- Is the operator bypassing constantly, meaning the gate is miscalibrated? Look at the bypass rate.

Every one of those questions returns a number dominated by test data. Worse, test data is *systematically unrepresentative*: tests deliberately exercise edge cases and rare patterns, precisely the patterns whose real-world frequency you are trying to estimate. Using such a log for calibration does not add random error. It biases the estimate toward whatever the test author found interesting.

## The Partial Fix, and Why It Was Not Enough

The first mitigation was to filter out records whose session identifier was the literal string `session`, the placeholder that subprocess-based hook tests produce when no real session is in scope.

That filter was necessary and insufficient. Some test harnesses supply a plausible-looking session value, and those records survive the filter while remaining synthetic.

The reliable discriminator turned out to be structural rather than value-based: **real agent sessions carry a UUID session identifier.** Filtering to UUID-shaped session IDs, rather than merely excluding a known placeholder, is what separated the roughly 105 genuine events from the rest.

## Generalisation

The rule this yields is not "filter your logs." It is:

> **If a hook writes an audit record, its test suite writes audit records too. Decide at design time how a reader will tell them apart, and make that distinction structural rather than a value you happen to recognise.**

Three concrete forms, in ascending order of robustness:

1. **Separate sink.** Tests set an environment variable that redirects the audit path. Clean, but fails silently the moment a test forgets to set it.
2. **Explicit provenance field.** Every record carries an origin marker. Better, but a test that constructs a record by copying production code inherits the production value.
3. **Structural discriminator.** Real events carry something tests structurally cannot forge without effort, such as a genuine session UUID issued by the harness. This is what worked here.

## What It Cost

The number that matters is not 8,000 or 105. It is the interval during which deny-rate figures were quoted from this log and treated as measurements of real agent behaviour. Any conclusion drawn about whether Gate-1 was too aggressive, during that interval, was drawn from a dataset that was almost entirely the test suite describing itself.

The framework's own principle applies to its instrumentation, not just its outputs: a measurement you have not tried to falsify is not evidence. The falsification here was cheap, count the distinct session identifiers, and it was not run until the number looked surprising.

## Related

- [wrong-protocol-hook-silently-noop](wrong-protocol-hook-silently-noop.md) — the sibling failure, where a hook produced no signal at all rather than a misleading one
- [enforcement-layer-needs-meta-verification](enforcement-layer-needs-meta-verification.md) — the enforcement layer requires its own verification layer
