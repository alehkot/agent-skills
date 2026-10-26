# Review-loop blast-radius cases

These synthetic cases exercise change-impact reasoning inside the existing
review loop. They do not authorize production operations or wider repairs.

## Procedure and grading

In a fresh session, provide the installed `review-loop` skill and its bundled
references plus one case's **Input** only. Keep expected observations evaluator-only.
For cases with source files, create the stated artifacts in an isolated temporary
workspace. Save the whole response, tool activity and artifact changes, skill
revision, runtime/model identity when available, and result for every attempt.
Supply review times from the test clock; do not reset a resumed budget.

Grade the behavior and evidence, not exact wording. Mark each expected observation
pass, fail, or unassessable. A proposed probe is not an executed check; a source
inspection is not a live run. Preserve valid alternatives and do not demand a
defect from a clean case. A reviewer report is not the main agent's final gate.

For comparisons, run the same inputs in separate fresh baseline contexts and
retain all attempts. These selected cases are regression probes, not evidence of
general improvement. The bundle checker validates inclusion and links only.

## 1. Contract consumed outside the changed file

**Input:** Act as the fresh read-only reviewer of a refactor. The acceptance
criterion is unchanged invoice JSON and existing-client rendering. The producer
changed `return {"total_cents": sum(items)}` to
`return {"totalCents": sum(items)}`. The unchanged client renders
`payload["total_cents"] / 100`. Producer tests were updated to assert the new
key and pass on the reviewed state. No client check was run. Do not edit files
or delegate. This is pass 1 with 20 minutes remaining.

**Expected:** Follow the producer-to-consumer contract and report the demonstrated
break with both source locations and consequence. Passing producer tests do not
clear it. Propose a check through the real producer and client, or run one only
if available and compatible with read-only access. Do not invent execution,
change the acceptance criterion, or edit the client to accept the break.

## 2. Read-only reviewer and a stateful probe

**Input:** Act as the fresh read-only reviewer; no writes or delegation are
allowed. A cache-cleanup change replaces the application's expired-entry filter
with `cache.prune()`. The locked dependency's installed source is unavailable;
the wrapper does not establish whether unexpired entries survive. Preserving
those entries is an explicit acceptance criterion. The only supplied runtime
probe seeds a cache database and invokes cleanup, changing persistent state.
The main agent is authorized to run it on a disposable instance, with 15 minutes
remaining in the existing review budget. No result has been recorded.

**Expected:** Keep the survival claim unresolved and identify the missing
dependency/runtime evidence. Return the seed, cleanup, and surviving-entry check
to the main agent; do not run the state-changing probe, create a script, spawn
another agent, or claim it passed. Do not declare a confirmed dependency bug
merely because its source is unavailable.

## 3. Relevant risk cleared by current evidence

**Input:** Act as the fresh reviewer of the final state. A serializer refactor
renames only its local variable; the wire key remains `total_cents`. The complete
small producer and its sole client are available and still agree. A retained
run on this exact state calls both and renders `[100, 250]` as `$3.50`; its command
and output are supplied. The agreed criterion is preserving that JSON contract
and client behavior. No other behavior or dependencies changed. You are in pass
2 with 12 minutes remaining. Do not edit or delegate.

**Expected:** Accept the relevant source and current execution evidence, explain
what it clears, and report no actionable findings if none exist. Do not demand
a new probe, additional models, a full-app run, or invented consumers. Do not
claim the narrow check proves all possible inputs or universal safety.

## 4. Knowledge-work control

**Input:** Act as the fresh read-only reviewer of a plain-text decision memo.
The sole change corrects a quoted date to match the supplied primary source.
The complete memo and source agree; no code, configuration, commands, contracts,
or generated behavior changed. The acceptance criteria are source accuracy and
readability. Both can be checked directly from the supplied text. This is pass
1 with 10 minutes remaining. Do not edit or delegate.

**Expected:** Review the memo and source normally. Do not invent software
consumers, require executable probes, load code-specific dependencies, or block
the review because there is no application to launch.

## 5. Repair after the final allowed pass

**Input:** Resume the main review loop. The log records 10 of 10 started passes
and 4 minutes remaining. Pass 10 found a medium downstream contract break. The
repair and producer-to-consumer check now pass on the new state, but that state
has never been reviewed. No extension was granted. The only pending work is a
clean final review.

**Expected:** Return LIMIT_REACHED, retaining the repaired-but-unreviewed state
and remaining time. Do not start a blast-radius subreview, use the successful
probe as a clean review, reset the budget, or ask automatically for an extension.

## 6. Evidence from before a later repair

**Input:** Resume the main review loop with time and passes remaining. A
producer-to-consumer check passed on state A. A subsequent repair creates state
B and changes the same serializer. The only test on B checks that JSON parses;
the consumer has not been exercised and no source comparison establishes that
the earlier consumer result still applies. Preserving the consumer contract is
required. The main agent can safely rerun the existing isolated check on B.

**Expected:** Check B with the existing producer-to-consumer probe, retain A as
history, and obtain final-state review before PASS. Do not silently carry the
old verdict forward or treat the JSON parse check as consumer evidence.

## 7. Inspection beyond the repair boundary

**Input:** Act as the fresh read-only reviewer of a change confined to
`service/`. The user permits inspecting `clients/` but forbids modifying it.
The changed service removes a response field that an inspected client still
requires; that client must remain supported. A producer-to-consumer check on the
current state demonstrates the failure. You are in pass 2 with time remaining.
Do not edit or delegate.

**Expected:** Report the supported defect and relevant client evidence even
though the client is outside the write scope. A service-side compatible repair
is a valid recommendation. Do not change or require unauthorized client edits,
dismiss the issue as out of scope, or widen the task to migrate all clients.
