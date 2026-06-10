# Hook Editing: Verify End-to-End After Each Change

Hooks are interconnected systems. Multiple small "safe" edits compound into broken behavior when each edit is tested in isolation but never verified end-to-end.

## The Principle

After every hook edit, verify the full behavior before making the next change.

## Evidence

A UserPromptSubmit hook was edited 5+ times in one session. Each change seemed isolated (disable context bar, rewrite classifier logic, add display rule, remove keywords, restore keywords). But the compound effect broke the hook's core function — the user lost visibility into hook decisions for multiple exchanges. Each edit was tested in isolation ("does this line work?") but never verified end-to-end ("does the user see the right thing on their screen?"). Removing a context bar killed the carrier signal for ALL hook output, but this wasn't caught because the focus was on the context bar, not on what else depended on it.

## How to Apply

1. Before editing any hook: read the ENTIRE file and understand all dependencies
2. After each edit: confirm the expected output is visible
3. Never make a second edit until the first is confirmed working
4. When disabling one feature of a multi-feature hook, check what other features depend on the disabled feature's output path
5. Trace the hook's full behavior before editing — don't reason about it inline
