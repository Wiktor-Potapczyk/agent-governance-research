# Test Ground Truth Must Be Independent of Model Output

When testing AI agent behaviors, deriving test assertions from prior model outputs creates circular validation. The test framework cannot distinguish regression from correction because the "expected" values were never independently verified.

## The Principle

Model output from any version is NEVER ground truth for test assertions. The system automates human judgment — to test it, the human judgment must exist first, recorded per test case before the model runs.

## Evidence

Test assertions for a scoring system (v5) were derived from v4 outputs. When v5 diverged on a test case (score 5 to 2), it was impossible to tell if v5 regressed or v4 was wrong. The test framework was circular. Checking the original source data showed v4 was roughly right and v5 was wrong — but this was only discovered by going to the actual source, not by comparing model versions.

## How to Apply

- For each test case, derive expected output from: (1) source documents, (2) verified data, (3) human domain expertise, (4) human judgment applying 1-3
- Delegate this derivation to a BLIND agent — no hypothesis, no prior model output in the prompt
- Record the expected output BEFORE running the model
- Test assertions compare model output to human-derived expectations, not to prior model output
- Score deltas between versions are signals to investigate, not automatic pass/fail criteria
