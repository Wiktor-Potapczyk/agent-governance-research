# Input Contracts Must Be Top-Down, Not Bottom-Up

When specifying inputs for a system, starting from "what files exist?" produces incomplete contracts. Starting from "what must the system produce?" and working backwards catches every required input.

## The Principle

Build input contracts top-down: start from "what must the system produce?" then "what does it need to do that?" then "do we have it?"

Never build bottom-up: "what files exist?" then "what's in them?" then "how might the system use this?"

## Evidence

An input contract was built bottom-up (file inventory). Adversarial review found 10 critical gaps — 3 failure modes had no corresponding input, supporting materials (40% of scoring) were omitted entirely, sub-stage routing was missing. All gaps were documented in existing project files. The bottom-up approach missed them because it answered "what do we have?" instead of "what does the system need?"

## How to Apply

For any input contract, spec, or interface design:

1. List what the consumer must produce
2. For each output, trace backwards to required inputs
3. For each input, check if it exists and in what form

The rubric is the consumer's requirements, not the provider's inventory.
