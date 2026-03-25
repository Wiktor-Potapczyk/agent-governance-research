# Lifecycle First Validation: The Proving Ground

## The Plan

The PM lifecycle + three-tier QA model needs validation on a real project before the framework can be considered production-ready. The first validation target is the Awards Automation project (S3: Context File Builder).

## Why This Project

- **Non-trivial scope:** S3 involves data assembly, template logic, and multi-category support
- **Clear success criteria:** Context files are either correct (match the data) or wrong (missing fields, wrong values)
- **Existing work:** S1 and S2 are already built. S3 is the next increment.
- **Testable outputs:** Context files can be validated against the verified data library
- **Human stakeholder:** [REDACTED] can evaluate output quality — providing the Layer 4 human judgment

## What to Observe

| Question | Success indicator |
|----------|-------------------|
| Does the classifier correctly route S3 tasks? | TYPE matches the actual work needed |
| Does TaskCreate define coherent increments? | Task lists map to meaningful work units |
| Does per-task QA catch real issues? | QA REPORT finds at least one genuine problem (not rubber-stamp) |
| Does per-increment pentest add value? | Pentest finds issues QA missed (integration, boundary, adversarial) |
| Does /pm fire at useful moments? | Checkpoint protocol catches stale state or missed blockers |
| Does the lifecycle prevent scope drift? | No-gos are respected; appetite is checked |

## What Would Falsify the Framework

- QA rubber-stamps everything (never finds issues) → QA enforcement is performative, not substantive
- Pentest finds nothing that QA didn't → Tier 2 adds overhead without value
- Classifier consistently misroutes S3 tasks → Classification system needs fundamental revision
- The lifecycle ceremony slows work without catching problems → Process overhead exceeds value

## Status

Not yet started. Prerequisite: S3 manual test with [REDACTED] on IBA Stevies (pending from Awards project). The lifecycle validation begins when S3 build starts.
