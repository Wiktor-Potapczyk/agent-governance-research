# Governance Framework Effectiveness Assessment

An evidence-based assessment of a 28-agent, 33-skill, multi-hook AI governance framework after two major work sessions (~50MB of conversation transcripts, ~14 hours of real work). This document measures what was actually used, what produced value, and what should be cut.

---

## Executive Summary

1. **46% of agents and 73% of skills have never been invoked.** 13 of 28 agents and 24 of 33 skills saw zero usage across both transcript sessions.
2. **The framework-building session spent ~100% of output on meta-work.** Of ~86 files produced, all were about improving the framework itself. Zero external project deliverables.
3. **The domain project session was productive.** 24 tangible deliverables (data files, schemas, specs, reports) from 73 agent dispatches with 97% specialist agent usage. The framework works when applied to real domain work.
4. **The general-purpose agent did 84% of framework session work.** 175 of 209 dispatches. The elaborate specialist routing infrastructure was largely unused in the meta-work session.
5. **The task classifier was invoked 62 times across both sessions.** It is the single most-used skill and the most expensive in terms of overhead per message. Whether this overhead improves output quality is unproven.

---

## What Is Actually Used?

### Agent Usage

| Agent | Session A (Framework) | Session B (Domain) | Total |
|-------|:---------------------:|:------------------:|:-----:|
| general-purpose (built-in) | 175 | 2 | 177 |
| adversarial-reviewer | 7 | 6 | 13 |
| data-engineer | 0 | 9 | 9 |
| technical-researcher | 9 | 0 | 9 |
| prompt-engineer | 5 | 1 | 6 |
| Explore (built-in) | 3 | 1 | 4 |
| content-marketer | 2 | 1 | 3 |
| report-generator | 0 | 3 | 3 |
| research-analyst | 2 | 0 | 2 |
| architect-reviewer | 1 | 0 | 1 |
| blueprint-mode | 0 | 1 | 1 |
| competitive-analyst | 1 | 0 | 1 |
| implementation-plan | 1 | 0 | 1 |
| llm-architect | 0 | 1 | 1 |
| research-synthesizer | 1 | 0 | 1 |
| vault-keeper | 1 | 0 | 1 |
| workflow-orchestrator | 1 | 0 | 1 |

**Custom agents used:** 15 of 28 (54%)
**Total custom agent dispatches:** 34 (Framework) + 71 (Domain) = 105
**Total built-in agent dispatches:** 177 general-purpose + 4 Explore

### Agents NEVER Invoked (13 of 28 = 46%)

| Agent | Assessment |
|-------|-----------|
| api-designer | Relevant -- not triggered because sessions were data/meta-focused |
| api-security-audit | Niche -- no security audit tasks occurred |
| debugger | Should be used -- likely substituted by general-purpose |
| git-flow-manager | **Genuinely useless** -- no git in this environment |
| mcp-developer | Niche -- no MCP building tasks occurred |
| mcp-registry-navigator | Niche -- no MCP discovery tasks occurred |
| mcp-server-architect | Niche -- no MCP design tasks occurred |
| nosql-specialist | **Not in stack** -- no NoSQL databases used |
| postgres-pro | **Not in stack** -- no PostgreSQL databases used |
| powershell-7-expert | Borderline -- hooks are PS1 but this agent was never dispatched |
| research-orchestrator | Redundant -- general-purpose + research-analyst covered research needs |
| research-coordinator | Redundant -- same as above |
| query-clarifier | Redundant -- never needed; queries were always clear enough |

### Skill Usage

| Skill | Session A | Session B | Total |
|-------|:---------:|:---------:|:-----:|
| task-classifier | 48 | 14 | 62 |
| save | 8 | 6 | 14 |
| architect-loop | 5 | 0 | 5 |
| ensemble | 2 | 1 | 3 |
| process-research | 1 | 1 | 2 |
| process-analysis | 0 | 1 | 1 |
| process-build | 1 | 0 | 1 |
| process-planning | 1 | 0 | 1 |
| maintain | 0 | 1 | 1 |
| loop | 0 | 1 | 1 |

### Skills NEVER Invoked (24 of 33 = 73%)

| Category | Skills (count) |
|----------|---------------|
| Vault utilities | inbox, daily, standup (3) |
| n8n domain | All 7 n8n-* skills (7) |
| Apify domain | All 12 apify-* skills (12) |
| Process routing | process-content (1) |
| Quality mechanism | verify (1) |

**Note on domain skills:** These are domain-specific reference skills (triggered when coding in specific platforms). Neither session involved that coding. Zero usage does not mean zero value -- it means the triggering context has not occurred yet.

**Note on verify:** Built as part of the CoVe quality mechanism. Never invoked despite being wired into the MECHANISM field of the classifier. The ensemble skill was used 3 times; verify, 0 times.

---

## What Did the User Actually DO?

### File Output by Session

**Session A (Framework) -- ~86 files produced:**

| Category | Count | % |
|----------|:-----:|:-:|
| Framework infrastructure | ~35 | 41% |
| Research/analysis artifacts | ~43 | 50% |
| State management | ~5 | 6% |
| Cross-project | ~3 | 3% |

**All 86 files are meta-work about the governance framework itself.** Zero files that would exist in a world without the framework.

**Session B (Domain) -- ~32 files produced:**

| Category | Count | % |
|----------|:-----:|:-:|
| Project deliverables | ~24 | 75% |
| Memory/feedback | ~5 | 16% |
| State management | ~3 | 9% |

**24 of 32 files (75%) are tangible deliverables.** These would exist regardless of whether the framework existed.

### Key Ratio: Specialist vs General-Purpose Agent Usage

| Session | Specialist dispatches | General-purpose dispatches | Specialist % |
|---------|:---------------------:|:--------------------------:|:------------:|
| Framework (A) | 34 | 175 | **16%** |
| Domain (B) | 71 | 2 | **97%** |

The domain session used the specialist routing infrastructure effectively. The framework session barely used it -- general-purpose handled 84% of dispatches.

---

## Comparison with Addy Osmani's Workflow

### What the Framework Does That Osmani Would Likely Cut

1. **Mandatory classification on every message** -- 62 invocations of a 159-line classifier. Osmani manually assesses in seconds.
2. **13 never-used specialist agents** -- Osmani uses models directly, not a catalog of 28 named specialists.
3. **24 never-used skills** -- Osmani mentions skills as "potential" not as an inventory of 33.
4. **Epistemic-check hook** -- Built, deployed, never blocked anything, disabled. Dead weight.
5. **Verify skill** -- Built (159+ lines), wired into classifier, never invoked. Theoretical value only.
6. **Process skills as routing layer** -- 5 skills that add an indirection step between classification and work. 5 total uses.
7. **Memory files about thinking patterns** -- 10+ files about how to think (reconsideration science, epistemic honesty gap, ensemble thinking, etc.). Osmani has zero metacognitive infrastructure.

### Verdict: Is the Complexity Proportional to Value?

**No.** The system has a 28-agent, 33-skill, multi-hook infrastructure that is ~5-10x more complex than Osmani's approach, but the domain session (where real work happened) used only 9 unique agents and 7 skills. The remaining infrastructure is either unused (46% of agents, 73% of skills), theoretical (verify, process-content), or self-referential (meta-work about the meta-work system).

The **domain session demonstrates the system works when applied to real problems.** The specialist routing (97% specialist usage) produced tangible deliverables efficiently. The problem is not the concept -- it is the ratio of infrastructure to usage.

---

## What to Keep, Modify, or Remove

### Top 5 Highest-Value Components

1. **adversarial-reviewer** -- 13 uses, both sessions. Catches problems before they ship. Direct Osmani parallel ("second AI to critique").
2. **save skill** -- 14 uses. Enables cross-session persistence. Essential infrastructure.
3. **data-engineer agent** -- 9 uses in domain session. Domain specialist that produced tangible deliverables.
4. **delegation-check hook** -- Only governance mechanism that actually blocks bad behavior. Prevents inline work when specialists should be used.
5. **architect-loop skill** -- 5 uses. Structures complex research into independent loops. Unique capability.

### Top 5 Candidates for Removal

1. **git-flow-manager** -- No git. Zero uses. Will never be used.
2. **nosql-specialist** -- Not in tech stack. Zero uses.
3. **postgres-pro** -- Not in tech stack. Zero uses.
4. **epistemic-check.py** -- Disabled. Never blocked. Failed experiment.
5. **research-orchestrator + research-coordinator + query-clarifier** (3 agents) -- Zero uses each. Research is handled by general-purpose + research-analyst.

### Top 3 Things to BUILD (Gaps)

1. **Actual test infrastructure** -- Osmani's #1 force multiplier. No tests, no test runner, no way to validate outputs. Even simple assertions on generated files would be valuable.
2. **Output quality measurement** -- We track what was used (this assessment) but not whether outputs improved. A simple "did the deliverable meet the requirement" check.
3. **Lightweight pre-flight check** -- Instead of a 159-line classifier, a 10-line "before you act, is this the right action?" check.

### Recommended Targets

| Component | Current | Recommended | Reduction |
|-----------|:-------:|:-----------:|:---------:|
| Custom agents | 28 | 15-18 | 36-46% |
| Skills | 33 | 28-30 | 9-15% |
| Active hooks | 3 | 3 | 0% |
| Config file lines | ~188 | ~120 | 36% |
| Task classifier lines | 159 | ~50 | 69% |

---

## Minimal Effective System (From-Scratch Design)

### Design Principles (derived from evidence)

1. Specialist agents provide value when matched to domain work (domain session: 97% specialist, high output)
2. General-purpose handles meta-work and research naturally -- do not fight this
3. The task classifier adds overhead proportional to its complexity -- keep it minimal
4. Governance hooks that actually block are more valuable than thinking tools that advise
5. Domain reference skills are cheap when dormant -- keep them
6. The save/state management system compensates for no version control -- keep it

### Minimal Agent List (15 agents)

| Agent | Rationale |
|-------|-----------|
| adversarial-reviewer | Highest-value specialist (13 uses). Catches blind spots. |
| data-engineer | Domain specialist for data work (9 uses) |
| technical-researcher | Primary research agent (9 uses) |
| prompt-engineer | LLM prompt specialist (6 uses) |
| content-marketer | Content production (3 uses) |
| report-generator | Structured output production (3 uses) |
| research-analyst | General web research (2 uses) |
| blueprint-mode | Code/workflow implementation (1 use, will grow) |
| llm-architect | LLM system design (1 use) |
| architect-reviewer | Post-build quality review (1 use) |
| implementation-plan | Multi-step planning (1 use) |
| api-designer | Dormant -- relevant to API work |
| debugger | Dormant -- essential when debugging occurs |
| powershell-7-expert | Dormant -- relevant for hook/automation work |
| vault-keeper | File operations |

### Comparison: Minimal vs Current

| Metric | Current | Minimal | Reduction |
|--------|:-------:|:-------:|:---------:|
| Custom agents | 28 | 15 | 46% |
| Skills | 33 | 28 | 15% |
| Active hooks | 3 | 3 | 0% |
| Config file lines | ~188 | ~100 | 47% |
| Task classifier lines | 159 | ~50 | 69% |
| Total infrastructure files | ~65 | ~46 | 29% |

---

## Open Questions

1. **Does the task classifier actually improve output quality?** No A/B test exists. It was invoked 62 times -- but we do not know if outputs were better than with manual routing.
2. **Are the 19 dormant domain skills truly zero-cost?** They appear in the skill list presented to the model on every message, consuming context tokens.
3. **Would the domain session have been equally productive without the framework?** The 97% specialist usage suggests routing works, but Osmani achieves similar results with manual selection.
4. **Is the memory system earning its keep?** 30+ memory files were created in the framework session. No evidence they were read and acted upon in the domain session.
5. **Does the adversarial-reviewer actually change outcomes?** 13 invocations, but we do not know how often its feedback was incorporated vs acknowledged and ignored.
