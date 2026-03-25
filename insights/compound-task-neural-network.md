# Compound Task Neural Network

Most AI agent frameworks classify tasks into a single type and route them through one pipeline. This insight proposes that tasks are mixtures of primitive operations, and the routing system should reflect that — diagnosing compound ratios rather than forcing a single label.

## Insight

Tasks are not single types — they are **mixtures of 5 primitive operations**: Research, Analysis, Planning, Building, QA. Each compound activates its own agents and tools.

This is fractal: zoom into the Research sub-compound and it might itself be Research + Analysis. Compounds all the way down until you hit atomic operations (read file, call API, write text).

## Current model (flat classification)

Task → classify → ONE type → process skill → done.

Problem: forces a complex task through a single pipeline. The other compounds get handled ad-hoc or not at all.

## Proposed model (compound diagnosis)

Task → **diagnose compound ratios** → route primary compound → sub-compounds discovered at runtime → each activates its own agents/tools → recursive until pure.

The matrix of task types is not static ("Research usually needs Analysis"). It is a **diagnostic tool** — given THIS specific task, which compounds are present? And compounds are discovered dynamically: a Research agent runs, hits an unknown, discovers it needs Analysis before it can continue.

## The neural network metaphor

- **Nodes** = task types (Research, Analysis, Planning, Build, QA)
- **Weights** = compound ratios for a given task (60/30/10)
- **Edges** = which agents/tools each compound activates
- **Activation** = dynamic — compounds fire during execution, not just at classification time

Each compound knows its agents and tools. The network fires in real-time as the task unfolds.

## Connection to existing systems

- An implication field in classification was reaching toward this — detects depth but still collapses to ONE type
- Compound classification exists in some frameworks but routes to sequential decomposition. This model keeps compounds **parallel and weighted**, not sequential.
- Process definitions already encode some connections implicitly (a build process has mandatory review = Build+Analysis). But never mapped explicitly as a network.

## Academic Context (Novelty Validated 2026-03-23)

**No existing multi-agent routing system classifies tasks as a continuous mixture vector over predefined cognitive primitives** (confirmed via Gemini Deep Research, 3 targeted queries, 20+ papers reviewed).

The closest work:

| Paper | Relation | Gap |
|-------|----------|-----|
| Ye et al., 2022 (EMNLP, Task-level MoE) | Router implicitly learns soft allocation across expert types | Primitives emerge from training, not predefined. Discrete selection, not explicit ratios. |
| Li & Yao, 2024 (AT-MoE) | Grouped routing with multi-dimensional balance across expert groups | Architecturally closest. But expert groups are model parameters, not named cognitive primitives. |
| Jin et al., 2026 (Agent Primitives) | 3 reusable primitives composed per query | Discrete composition, not continuous ratios. |
| Webb et al., 2025 (Nature Comms, MAP) | Brain-inspired modular planner with cognitive modules | Closest conceptually. Still discrete routing through modules, not probabilistic mixture. |
| Fractals (TinyAGI, March 2026) | Recursive self-similar tree of subtasks | Fractal structure exists, but no mixture modeling within nodes. |

**Significance:** While the industry has moved toward dynamic task graphs (Yu et al., 2025) and recursive decomposition (Prasad et al., 2023), the dominant abstraction remains "one specialist agent per sub-task" (Zhang et al., 2025). Frameworks that define "agent primitives" (Jin et al., 2026) still treat them as discrete blocks rather than continuous ratios. No existing system classifies tasks — or their recursive fractal sub-nodes — as a dynamic, simultaneous vector of fixed cognitive operations. By fusing primitives within individual nodes rather than just orchestrating them at the graph level, this framework addresses the rigid delegation bottlenecks present in current SOTA architectures.

## What this changes

The classifier would output compound ratios, not a single label. The routing layer would activate multiple process paths weighted by their ratios. Agents would be able to signal "I need compound X" at runtime, triggering dynamic routing.
