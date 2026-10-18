# Multi-Chat Execution Template

Use this template at the beginning and end of each F-numbered chat. The roadmap in `README.md` is authoritative for scope and exit criteria.

## Start-of-chat checklist

- [ ] Confirm repository identity and `main` is checked out.
- [ ] Inspect `git status --short --branch` and current HEAD; stop if unexpected changes exist.
- [ ] Read the roadmap and the previous numbered chat's handoff.
- [ ] State this chat's single objective, entry conditions, allowed changes, and exit criteria.
- [ ] Confirm which existing artifacts must remain immutable.
- [ ] Do not begin the next stage early.

## End-of-chat handoff template

# F[N] Handoff — [Short Stage Name]

**From:** F[N]  
**To:** F[N+1]  
**Status:** COMPLETE / PARTIAL / BLOCKED  
**Repository branch:** main  
**Final HEAD:** [SHA, if available]

## Objective
[One paragraph]

## Work completed
[Concrete bullets, no unsupported claims]

## Files changed
[Exact paths and reason]

## Validation and evidence
[Commands/tests, outcomes, evidence paths]

## Decisions made
[Only decisions supported by evidence]

## Unresolved issues
[Explicit list; do not bury uncertainty]

## Entry conditions for next chat
[What must be true before next stage starts]

## First action for next chat
[One specific action]

## Prohibited assumptions/actions
[Stage-specific warnings]

## Exit decision
[Explain why the stage meets its exit criteria, or why it is partial/blocked]

Do not mark a stage COMPLETE if its exit criteria are unmet. If context is becoming too large, stop at a safe boundary and write this handoff rather than broadening scope.
