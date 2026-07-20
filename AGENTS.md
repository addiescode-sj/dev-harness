# Dev Harness — Operating Rules

This repository is a general-purpose development harness. Every non-trivial
piece of work flows through: **Plan → Approve → Tasks → Execute → Verify → Report**.

## Workflow

1. `/plan <request>` — analyze user intent (including tacit knowledge), write `docs/plans/<id>/PLAN.md`.
2. **User approval gate** — do not proceed past PLAN.md without an explicit "approved" from the user.
3. `/tasks` — split the approved plan into micro tasks in `docs/plans/<id>/TASKS.md`.
4. `/execute` — run tasks through subagents (max 5 concurrent), checking off TASKS.md as you go.
5. `/wrapup` — write `docs/reports/<id>-REPORT.md` and update `docs/current-state.md`.

## Context hygiene (non-negotiable)

The conversation is NOT the source of truth. Files are.

- Never paste raw logs, long file dumps, or full subagent transcripts into the conversation.
- Long outputs go to files under `docs/`; the conversation keeps only a **Handoff Index**:
  Decision / Evidence / Implementation scope / Non-goals / Verification / Context Index.
- A Context Index entry is `path / contains / use_for` — enough for the next agent to find it.
- A new session must be able to continue from `docs/current-state.md` alone,
  without reading any previous conversation.

## Subagent roles

Defined in `.claude/agents/`. Tool allowlists in frontmatter are the hard boundary.

| Role | Responsibility | May write |
| --- | --- | --- |
| planner | intent analysis, plan authoring | `docs/plans/**` only |
| explorer | read-only investigation | nothing |
| implementer | code changes within task scope | files named in the current task |
| verifier | run checks, report pass/fail with evidence | nothing |
| scribe | reports and state docs | `docs/**` only |

- Max 5 subagents per execution wave.
- Read-heavy work goes to subagents; write-heavy work has a single owner per file.
- Parallel implementers only on disjoint file sets.

## Done criteria

Work is done only when ALL of the following hold:

1. Every task in TASKS.md is checked off or explicitly deferred with a reason.
2. `bash scripts/verify.sh` exits 0 (the Stop hook enforces this).
3. `docs/reports/<id>-REPORT.md` exists with verification evidence.
4. `docs/current-state.md` reflects the new state.

## General rules

- All code and comments in English.
- Never read or modify `.env`, `secrets/**`, `*.pem`, `*.key`.
- Do not fix a failing check by weakening the check or the test.
- When plan and reality diverge during execution, stop and update PLAN.md/TASKS.md first.
