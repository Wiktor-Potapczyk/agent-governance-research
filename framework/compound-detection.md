# Five Primitive Operations and Compound Detection

AI agent governance requires a taxonomy of what agents actually do. This document formalizes five irreducible operations that compose every knowledge work task, and describes the compound detection mechanism that prevents single-primitive misclassification.

## The Five Primitives

1. **Research** — gather information from external sources
2. **Analysis** — reason about information (includes review-as-mode)
3. **Planning** — structure and sequence work
4. **Building** — produce artifacts (includes content as a domain specialization)
5. **QA** — verify claims empirically (does this actually work?)

## Content Is Not a Primitive

Content production is Building with DOMAIN: content. It uses a content specialist as the builder agent but follows the same build process. A separate content process skill was initially built and then removed — content routes through the build process.

## QA Is a Primitive

QA is not just hooks or review steps. "Does this task produce claims needing verification?" is a classifier-time question. QA as a compound primitive has a complementary relationship with exploration:

- **Exploration** (the IMPLIES field) forces investigation at entry — prevents wrong starts
- **QA** forces verification at exit — prevents wrong endings
- Both fight premature convergence. Both need architectural enforcement.

## Compound Detection

The classifier's APPROACH field forces explicit yes/no on all five primitives for every task. This compound detection matrix ensures multi-dimensional tasks are not reduced to a single operation.

**Mandatory compounds (floor rules):**

| Primary TYPE | Always-yes compound | Agent | Why |
|-------------|-------------------|-------|-----|
| Build | Analysis | architecture reviewer | Every build needs post-build quality review |
| Planning | Analysis | adversarial reviewer | Every plan needs challenge before committing |

## Grounding

The five-primitive model is grounded in PM research (8 traditional PM fields map to 5 operations), the framework's architecture document (5 process roles), and the Jules framework (review and QA as separate enforcement points).

## Application

The classifier outputs a compound checklist. The process skill for the primary TYPE handles the main path. Compound agents handle secondary paths. Hooks enforce that all declared agents were actually invoked.
