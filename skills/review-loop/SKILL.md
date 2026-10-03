---
name: review-loop
description: >-
  Review completed work, fix confirmed issues, and repeat until a severity-based
  completion gate passes or the review budget is exhausted. Use for iterative
  self-review, a final quality gate, or a goal that must finish with no medium-or-
  higher issues. Defaults to 10 review passes and 30 minutes, with user overrides.
  Supports code, documents, and knowledge bases; uses a fresh reviewer when available.
---

# Review Loop

Make completion depend on reviewed, verified work. This skill orchestrates a
bounded review-and-repair process; it installs no hooks or background services.

## Establish the gate

When included in the original task, record the gate before execution, then do
the authorized work. Start the review clock only when the first review begins.
For an already completed artifact, begin there. Read applicable instructions,
the task's acceptance criteria, and the current artifact before fixing scope.

Defaults: **medium and above**, **10 started review passes**, **30 elapsed
minutes** from the first pass, including review, repairs, checks, and waits.
Honor explicit user overrides and record them. Do not silently remove a bound;
ambiguous overrides need clarification. The earlier limit stops review work.

Read [review-protocol.md](references/review-protocol.md) for severity definitions,
the review log, reviewer instructions, budget handling, and result shape.
Create a private, unique OS temporary directory and a Markdown review log, or
use the user's requested path. Announce it. Preserve existing log state on
resume; new turns, compaction, and handoffs do not reset the clock or counters.

Fix the review scope to the whole requested result and its relevant context.
For code, record the task baseline and include staged, unstaged, and relevant
untracked work; do not use only the latest commit or last repair diff. For
documents or knowledge bases, identify the complete changed artifacts and
source obligations. Protect unrelated changes.

## Review, reconcile, repair

1. Read the log and actual clock. Before starting a pass, check both limits,
   increment the started-pass count, and persist it. Failed or interrupted
   reviewer attempts consume a pass too.
2. Use a **fresh-context, read-only reviewer** when the runtime permits it. Give
   it the task contract, scope/baseline, applicable instructions, and access to
   the artifacts and evidence; do not fork the author's conversation or feed
   it a defense of the implementation. The reviewer must not edit or delegate.
   If unavailable, perform an explicit self-review and disclose the fallback.
   Do not call an external model/provider without applicable authorization.
3. Review the whole scope for requirements, correctness, relevant failure paths,
   source fidelity, and regressions. Select relevant concerns rather than
   inventing absent features or demanding findings. Require location, impact,
   and evidence for each issue. Missing necessary evidence is a limitation,
   not a clean review.
4. Verify findings against the artifacts. Record confirmed issues, demonstrated
   false positives, and unresolved claims separately. Maintain stable finding
   IDs so a repeated unresolved issue cannot disappear as "nothing new."
5. Fix confirmed findings at or above the threshold within the authorized
   scope, then run appropriate verification. Report lower-severity suggestions
   without default polishing loops. New product decisions or external actions
   still need the authorization required by the task; stop blocked work while
   completing independent authorized work within the budget.
6. Review the updated whole result again. Any repair after the last review
   invalidates that review as final proof. The clean final pass also counts
   toward the limit. Never add an uncounted "quick final check" as pass eleven.

Check remaining time before every review, repair, and verification operation;
use timeouts bounded by the remaining allowance when supported. Stop scheduling
work at the deadline. Cancel owned review/check processes safely when possible;
if an uninterruptible operation returns late, record the overrun and do not pass.
Perform only necessary safe shutdown and status recording after the limit.

## Pass or stop

Return **PASS** only when all of these hold within the budget:

- The original acceptance criteria are satisfied with current evidence.
- A completed review covers the final state of the entire agreed scope.
- No confirmed or unresolved finding at or above the threshold remains.
- Required checks pass on that state; missing checks or evidence are not passes.

Repeated issues, accepted-but-unfixed medium issues, and dismissed findings
without evidence still block. Do not lower severity, weaken tests, narrow the
scope, or count an author's confidence as proof. A user-authorized change to
the criterion must be recorded as a changed criterion, not success on the old one.

If either limit is reached without a pass, return **LIMIT_REACHED — not passed**
with remaining findings, unverified repairs, and restart instructions. Do not
automatically ask for an extension or restart the loop. Further review requires
the user's explicit extension. If a missing permission, decision, or environment
prevents progress, return **BLOCKED — not passed**. On a user stop, return
**STOPPED — not passed** and preserve the checkpoint.

These are review results, not host goal lifecycle states. When running inside
an existing `/goal`, do not create a nested goal, mark an unmet goal complete,
or pause/cancel it without the required user instruction. Follow the host's
lifecycle rules. An automatic continuation after a terminal non-pass must read
and honor that result without spending another review budget.

Finish with the result, scope, threshold, actual time/passes used, findings,
verification evidence, reviewer mode, log path, and next action. A pass states
the review's scope and limitations; it is not a claim that no defects can exist.
