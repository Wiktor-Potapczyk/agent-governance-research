# Claude Code Statusline Known Bugs and Workarounds

A comprehensive catalog of Claude Code statusline JSON payload bugs, community workarounds, and fix approaches. The statusline JSON payload has systemic reliability problems: 20+ open bugs with zero confirmed official staff responses. Several closed as NOT_PLANNED without fixes.

---

## Critical Bugs

| Issue | Bug | Status |
|-------|-----|--------|
| #19570 (13+ dupes) | Cross-session model contamination -- `/model` in one session corrupts all others | OPEN |
| #31640 | context_window_size not updating on `/model` switch | OPEN |
| #36434 | remaining_percentage leaks across concurrent sessions (denominator shared globally) | OPEN |
| #34143 / #35059 | Opus shows 200K instead of 1M in context_window_size | OPEN |
| #36014 | Autocompact fires at 17% on 1M model -- internal effective window capped at 200K | OPEN |
| #33146 | cost.total_cost_usd accumulates permanently across `/clear` -- never resets | OPEN |
| #19669 / #35816 | Post-`/compact` statusline data stale until next API response | OPEN |

## Other Bugs

| Issue | Bug |
|-------|-----|
| #18781 | current_usage flickers to null on `/` and `@` keypress (NOT_PLANNED) |
| #19724 | current_usage all zeros in certain versions (NOT_PLANNED) |
| #22643 | output_style.name stale after `/output-style` |
| #35279 | Bedrock ARN in model.display_name |
| #26769 | Windows inline command broken (use .js or .ps1 file) |

## Community Workarounds

### 1. Transcript Reading (most robust)

Read transcript_path JSONL directly. Parse last non-sidechain assistant message usage fields. Bypasses ALL JSON payload bugs. Limitation: stale post-`/compact` until next API call.

### 2. Environment Variable Override

Set `ANTHROPIC_DEFAULT_OPUS_MODEL` to force correct 1M context window. Does NOT fix cross-session contamination.

### 3. Hardcoded Model-to-Window Mapping

Pattern-match model.id, apply known window sizes. Used by multiple community scripts. No script trusts context_window_size unconditionally.

### 4. Three-Strategy Fallback

Try used_percentage -> total_input_tokens -> current_usage.input_tokens. Guards against all known zero/null scenarios.

### 5. Null Guards

current_usage flickers to null on keypress. Always guard before dividing.

## Community Scripts

| Script | Approach |
|--------|----------|
| levz0r/claude-code-statusline (Bash) | Transcript-reading, most robust |
| shrwnsan/claude-statusline (TS) | Three-strategy fallback, fastest (5ms Bun) |
| sirmalloc/ccstatusline (TS/React) | Most feature-complete, usage API support |
| kyllian330/claude-statusline | Cross-platform including Windows .exe |

## Recommended Approach

Transcript reading (levz0r pattern) is the robust multi-session fix. Needs: tail-seek on transcript JSONL, model extraction from last API response, token calculation from current_usage fields, null/zero guards, acceptance of post-`/compact` staleness.
