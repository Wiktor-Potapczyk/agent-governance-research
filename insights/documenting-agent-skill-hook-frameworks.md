# Documenting an agent / skill / hook framework

**The finding:** The established documentation frameworks all assume a conventional code library. A framework whose primary artifacts are *agents, skills, and hooks* (markdown + config + light glue code, not functions and classes) falls into a genuine gap — and the way to fill it is to compose existing frameworks around one borrowed convention: the **attributes-table per configurable entity**.

## What the canon prescribes (and what it leaves out)

Surveying the canonical, citable frameworks:

- **Diátaxis** (diataxis.fr) — four documentation modes (Tutorial / How-to / Reference / Explanation) on two axes, with a strict no-mixing rule. *Transfers fully* — it governs *where* any doc goes regardless of what the repo contains.
- **arc42 / C4** — architecture structure (12 sections; 4 zoom levels). *Transfers partially* — a single layer diagram + a building-block view is enough; the full template is overkill for a one-repo framework.
- **ADR / MADR** (Nygard 2011; adr.github.io/madr) — immutable, append-only decision records. *Transfers fully* — the "why this hook fires here / why this dispatch is mandatory" content is exactly architectural-decision content.
- **Keep a Changelog + SemVer** — release-history discipline. *Changelog transfers; SemVer does not* — a framework with no version-pinned downstream consumers gains nothing from MAJOR.MINOR.PATCH. Date-based entries are sufficient.
- **standard-readme / Art of README** — the front-door contract. *Transfers fully.*
- **docs-as-code** (writethedocs.org) — docs in version control, reviewed and CI-linted alongside code. *Transfers fully — it is the substrate the others sit on.*

**The gap:** none of them says how to document a *hook* (its trigger, inputs, outputs, branches, failure mode) or a *skill* (its routing contract and dispatch fan-out) or an *agent* (its tool surface and output contract). There is no cross-tool standard for this. Verified emerging conventions exist for the *artifact format* itself (the `SKILL.md` frontmatter spec; `AGENTS.md` at repo root), but not for how to *document a fleet of them*.

## The transferable convention

The closest analogues are config-heavy repos — Ansible collections (module attributes tables: param / type / required / default / description), Terraform modules (`terraform-docs` auto-generated from variable/output blocks), CrewAI (a fixed per-concept schema: attributes table → config → example). The dominant pattern across all three: **every configurable entity is documented with a uniform attributes table, not narrative prose.**

Applied here, each hook / skill / agent gets a uniform Reference table. For a hook the load-bearing row is **Logical paths** (each branch: condition → outcome) — with the honest caveat that the *code* (and its `test_<hook>.py`) is the source of truth, and a hand-maintained branch table that has gone stale is worse than an absent one, because a reader trusts it.

## The composition we adopted

One followable standard = **Diátaxis routing** (where a doc goes) + **attributes-table reference schema** (the unit of reference, since artifacts are configurable entities) + **MADR decision log** with a single-authority rule that prevents three competing "why" stores + **date-based Keep-a-Changelog** + the maintainability rules (single-source-of-truth, same-commit freshness, completeness, mode-separation).

**The honest enforcement limit:** automated layers (a doc-consistency checker over a pinned-fact manifest, link-integrity) verify *consistency of what exists*; they cannot verify *completeness of what the standard requires*. Completeness rests on a human Definition-of-Done run at publish time — process discipline, not a blocking hook. Trying to enforce completeness with a runtime hook was considered and rejected as over-engineering: the lighter, honest design is a checklist whose single checkpoint is the publish gate.

The live standard derived from this research ships in the framework repository's `docs/documentation-standard.md`.

## Why it matters

This is the same lesson the framework keeps relearning in a new domain: **structure beats exhortation, but only where it can be checked — and where it can't be checked, say so rather than pretend.** The documentation standard is honest about its own un-enforced seam, which is what keeps it from becoming the shelf-ware it warns against.
