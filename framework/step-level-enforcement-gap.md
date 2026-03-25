# Step-Level Enforcement Gap in Process Skills

Governance frameworks for AI agents typically enforce at the process level ("was the right process invoked?") but not at the step level ("were the right steps followed within that process?"). This document examines the gap and describes a partial resolution.

## The Gap

Enforcement operates at PROCESS level (was the research process invoked?) but NOT at STEP level (was the right agent chosen? was synthesis done?).

## QA Report Evidence

| Claim | Result |
|-------|--------|
| Classifier routes Research to research process | PASS |
| Research process has 4-agent routing table | PASS |
| Synthesis declared mandatory for 2+ agents | PASS |
| Dispatch compliance enforces synthesizer | **FAIL** — only if classifier lists it in MUST DISPATCH |
| Routing check blocks wrong process skill | PASS |
| No hook validates agent selection within process | **CONFIRMED GAP** |

## Three Enforcement Layers

| Layer | Enforced by | Reliability |
|-------|-----------|-------------|
| Right process skill invoked | Pre-tool-use routing check | Deterministic |
| Process skill steps followed | Post-tool-use step reminder | **Soft — ~78.5% compliance** |
| Right agent selected within process | **Nothing** | **Zero enforcement** |

## Resolution

A Stop hook was built to perform process step checks. It applies hard blocks on missing scope blocks and QA reports, with soft logging on synthesis, review, and agent dispatch.

| Layer | Before | After |
|-------|--------|-------|
| Right process skill invoked | Deterministic | Unchanged |
| Process skill steps followed | Soft (~78.5%) | **Hard on scope/QA, soft on rest** |
| Right agent selected within process | Zero enforcement | **Soft logging (data collection)** |

Agent selection within a process remains advisory — tightening requires more data from soft logs.

## How This Was Discovered

This was demonstrated live: a task was classified as Quick, then dispatched a single technical researcher for a multi-source task that needed an orchestrator. The routing table existed in the process skill but nothing enforced it.
