# Follow Your Own Skills Exactly

When invoking a skill, agents improvise labels, rename components, or modify the output format to sound better in context. This erodes consistency and breaks the contract between the skill definition and its output.

## The Principle

When a skill defines a format, use that exact format. The skill is the spec. If the format needs changing, change the skill file first, THEN use the new format.

## Evidence

An ensemble skill defined lens labels as "LENS A (reframe)", "LENS B (decompose)", etc. During execution, the agent renamed them to "ARCHITECT", "ENGINEER", etc. because it sounded better in context. The skill and the output disagreed, eroding trust in the system's consistency.

## How to Apply

- Read the skill format before producing output — don't rely on memory of what it says
- Agent dispatch descriptions can be brief but the PROMPT content and OUTPUT format must match the skill exactly
- If the format needs changing, change the skill file first, THEN use the new format
