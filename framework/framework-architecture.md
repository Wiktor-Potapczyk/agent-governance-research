# Framework Architecture: Iterative Incremental with Connected-Network Vision

This document describes the organizational architecture of the governance framework — how its components connect, how work flows through the system, and how it evolves from a simple pipeline toward a fully connected process network.

## Framework Principle

Iterative incremental development. "Big picture → sequence → build → repeat with extended capability."

## Vision (v-infinity)

A 5-node fully connected network. Every phase (Research, Analysis, Planning, Build, QA) can activate any other. The activation pattern emerges from input, not a hardcoded sequence. The classifier acts as the activation function, running after every node.

## Implementation (v1)

Linear pipeline — Research → Analysis → Planning → Build → Review. Hardened with mandatory dispatch enforcement at each link. The human operator manages phase transitions.

**Why pipeline first:** The system cannot enforce the network reliably. Early testing proved it could barely enforce linear steps (enforcement drops, soft links skipped). Simple and working beats complex and theoretical.

## Two Enforcement Levels

1. **Global:** Lifecycle awareness — project state files and the classifier track which phase the system is in, preventing drift
2. **Detail:** Within process skills — mandatory dispatch of specific agents at review/synthesis steps

## Inner Processes Are Compound, Not Recursive

- Research does not spawn separate Planning and Analysis processes
- Research has its own fused planning+analysis inner loop
- Each process skill handles its compound nature internally
- Process skills do not call each other — they have domain-specific steps

This is a critical design constraint. If inner compound processes were allowed to recurse, the system would face infinite depth with no enforcement boundary.

## Versioning Roadmap

| Version | Architecture | Status |
|---------|-------------|--------|
| v1 | Linear pipeline, hardened | Build now |
| v2 | Pipeline with documented "when to break sequence" patterns | Future |
| v3 | Selective cross-connections for proven patterns | Future |
| v-infinity | Fully connected network (requires enforcement capabilities not yet available) | Vision |
