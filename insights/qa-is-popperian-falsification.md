# QA Is Popperian Falsification

In AI agent systems, QA steps are often treated as correctness guarantees. This insight reframes QA through the lens of Popperian falsification: QA proves the absence of found bugs, not the absence of bugs. Understanding this asymmetry is essential for designing honest quality mechanisms.

## The Finding

QA proves absence of found bugs, not absence of bugs. A PASS means "could not break it during the test window." It does not mean "correct." This asymmetry is fundamental — it applies to every testing mechanism at every tier.

This is not a limitation to work around. It IS the nature of empirical verification. The best QA can do is make failures visible. It cannot prove correctness.

## Evidence

- **Karl Popper (1934):** Scientific theories can be falsified but never verified. A hypothesis survives testing — it is not proven true.
- **Same pattern in security testing:** A pentest that finds no vulnerabilities does not prove the system is secure. It proves the tester ran out of ideas.
- **The QA-on-QA problem:** Who verifies the QA was thorough? The answer is: no one can, definitively. An untested surface list makes the gap visible but doesn't close it. This residual is irreducibly human.
- **Adversarial review finding (2026-03-22):** "The pass gate is as reliable as the agent's severity calibration, which has no ground truth." A PASS with bad tests is worse than no PASS — it creates false confidence.

## What It Changes

Three-tier testing model follows directly:

| Tier | Scope | What falsification means |
|------|-------|------------------------|
| Tier 1 (QA) | Single task claims | "I tested my claims and couldn't break them" |
| Tier 2 (Pentest) | Whole increment | "I tried to break everything built and couldn't" |
| Tier 3 (Eval) | Whole component | "Systematic trap cases couldn't break it" |

Each tier increases the surface area of attempted falsification. None proves correctness. The value is cumulative confidence, not proof.

## The Design Principle

Every QA artifact must state what was tested AND what was not tested. An untested surface list is mandatory — it shifts the irreducible human judgment from "is this correct?" to "is what we didn't test acceptable?"

## Connection to Other Insights

- **Two-layer hook purpose:** QA hooks maximize autonomous run length by forcing falsification before escalating. This insight explains WHY that works — falsification is the only empirical operation available.
- **Hooks over prompts:** Hooks verify the process ran, not that the answer is correct. Falsification is the process.
- **Mandatory exploration backfires:** Forcing "verify everything" produces rubber-stamping. Falsification must be targeted and honest about its limits.
