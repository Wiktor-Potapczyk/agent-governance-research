# Volatile-Source Citation Integrity

## The Finding

A citation-integrity system that binds each citation to a SHA-256 hash of the source's bytes (to prevent LLM-fabricated citations) has a blind spot: sources that **legitimately change often**. For a frequently-edited source the pinned hash drifts on every edit, producing perpetual false `SOURCE_DRIFT`. The naive fix — exempt volatile sources from hashing — is correct for *script-generated* output but **wrong for hand-edited doctrine**, because hand-edited prose is genuinely mis-citable where deterministic script output is not. The resolution is not binary (hash-everything vs exempt) but a **third granularity: enforce that the cited section anchor exists**, dropping only the volatile whole-file hash.

## Evidence

- A wiki page cited a hand-edited governance "constitution" file, pinned to its SHA. The constitution was revised ~1.5×/week; its hash had already drifted (`a9eacd…` → `b7942a…`) within days. Whole-file SHA pinning was structurally unsustainable for it (churn far above the documented `<1/week` viability threshold for hash-pinned sources).
- The same page also exposed two latent citation-parser bugs (zero-indent list items dropped; inline-flow YAML form unreadable) — so it parsed as *sourceless* and produced a false `MISSING_SOURCE`. **A false-positive in an integrity check is not benign: it trains the operator to ignore the check, which destroys the mechanism's value** (the same failure mode that motivates low-false-positive enforcement throughout this framework).
- A four-lens parallel analysis (reframe / decompose / stakeholder / adversarial) converged that "full-hash vs exempt" is a false binary. The decisive lens was adversarial: a blanket SHA-skip is an *escape hatch* — anything mis-citable could be relabeled "volatile" to dodge the gate — and the truly ignored risk is **stale citations** (a hash that passed at ingest stays green forever even after the source changes to contradict the claim).

## The Resolution Space

External provenance practice offers a spectrum, and **fabrication-resistance and maintenance burden move together**:

| Technique | Fabrication-resistance | Maintenance on a volatile source |
|---|---|---|
| Content addressing (IPFS CID) | Maximum | Re-pin every version |
| Immutable snapshot (Perma.cc, Memento RFC 7089) | High (point-in-time) | Delegated to archive |
| Version-ID pinning (git blob/commit SHA, DOI version) | High | Needs source versioning |
| Canonicalize-before-hash (RFC 8785 JCS) | Moderate | One-time canonical form |
| Section/anchor-scoped hashing (Trusty URIs, fragment IDs) | Moderate | Anchor must stay stable |
| Signed attestations (C2PA, in-toto, Sigstore, SLSA) | Highest (discrete assets) | Key management |
| Exempt volatile sources | Low (for that class) | None |

A whole-file hash never actually proved "the cited section supports the claim" — only "bytes unchanged since ingest." So for a mis-citable hand-edited source, dropping the whole-file hash loses less integrity than it appears, *provided* a cheaper check replaces it.

## The Design Principle

**For a volatile, mis-citable source, enforce anchor existence rather than file-content identity.** A source exemption should be graded by *why* the source resists hashing:

- **Script-generated (`type: generated`):** cannot be meaningfully fabricated → enforce path existence only.
- **Hand-edited doctrine (`type: schema-doctrine`):** mis-citable → enforce path existence AND that the cited anchor heading literally exists in the file (missing field → `MISSING_ANCHOR`; absent heading → `ORPHAN_ANCHOR`). Stricter than the generated case.

The semantic "does the section still support the claim" question is left to the periodic lint's noun-overlap check (`WEAK_CITATION`), not the per-write gate — keeping the write path cheap while still catching drift on a schedule. The general lesson: an integrity exemption must be *narrower* than "this source is inconvenient to verify," and the narrowing should restore a proportionate check, not remove verification wholesale.
