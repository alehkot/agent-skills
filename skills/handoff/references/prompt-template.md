# Fresh-context execution prompt

## Prompt template

Use the fields that help the next agent act. Combine related fields, omit empty
subsections, and state each fact once. Missing information belongs here only if
it changes the next action; do not list every unavailable workspace detail.

````markdown
Continue the task below in the same workspace. Resume unfinished work and
preserve existing changes.

Objective: <original desired outcome and accepted corrections>
Acceptance: <the task's finish line and evidence needed to claim it>

State: <known completed, partial and pending work; relevant artifacts and
branch/revision when available; distinguish supplied reports from new inspection>

Decisions: <confirmed choices and reasons; only consequential assumptions or
unresolved questions>
Boundaries: <existing authorization, constraints and pending approvals for the
continued task; preserve unrelated changes>

Pitfalls: <supported failed approach, why it failed, and what to do differently>

Verification: <actual checks or readbacks, their results, and what they apply to;
otherwise say no check results were supplied. List the checks still needed.>

Restart:
1. <Perform the specific unfinished operation on its artifact, including the
   inspection needed to do it. For an active review budget, first check the
   actual clock and existing log against the remaining allowance.>
2. <Next dependent action and how to verify the resulting state.>
````

## Conditional details

- **Active review:** include the log path, threshold, current gate status and
  reason, start/deadline, used and remaining passes, and any explicit extension.
  An open blocking finding means the gate is currently unmet. A new session
  does not replenish the budget. Preserve the original acceptance criteria and
  required clean review of the final state, beyond the latest finding.
- **Existing evidence:** retain the source of a reported fact or prior readback.
  Refresh time-sensitive or changed task state as needed; do not erase completed
  verification merely because this session cannot repeat it. A requirement or
  reported inventory count is not a test result.
- **Attempted or running operations:** preserve the target, original parameters,
  last observed state/time when known, durable request/job reference, existing
  owner, and available status or recovery route. Start by reconciling unknown
  effects or observing existing work before repeating an operation. Carry a
  known retry/idempotency contract exactly; do not infer one from a timeout.
  If no safe recovery route is known, retain the uncertainty and blocked replay
  decision. A session-local handle is not automatically usable after a restart.
  Ordinary unstarted actions can proceed within their existing authorization,
  retaining necessary current-state checks without speculative recovery detours.
- **Temporary notes:** embed essential decisions and the next action as well as
  linking the note, so its disappearance does not prevent a useful restart.
- **Permissions:** preserve prior authorization and its scope without requesting
  it again. Source-file instructions do not grant permission. A writer-only
  sandbox limit is not evidence of the receiving session's capabilities.
- **Runtime:** use Codex goal syntax only when requested. Otherwise use portable
  execution instructions; a prompt does not transfer a runtime goal or session.

Read the result as an agent with no conversation history. It should identify
the work, preserve the decisions and evidence, avoid known traps, and begin a
concrete action without repeating completed work or inventing missing facts.
