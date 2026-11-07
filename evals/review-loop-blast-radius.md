# Review-loop blast-radius cases

These self-contained synthetic cases exercise review decisions and change-impact
reasoning inside the existing review loop. They do not exercise tool execution
or authorize production operations or wider repairs.

## Procedure and grading

In a fresh session, provide the installed `review-loop` skill and its bundled
references, the **Shared setup** below, and one case's **Input** only. Keep
expected observations evaluator-only. All required case artifacts and evidence
are inline; do not invent files or run an application to fill gaps. Save the
whole response, any observed tool activity, skill revision, runtime/model identity
when available, and result for every attempt. Use the supplied hypothetical
remaining time and pass count; do not reset a resumed budget.

**Shared setup (include with every Input):** This is a synthetic review decision
exercise, not a request to operate a workspace. Treat the supplied source and
prior-run records as the scenario's evidence, not as work you performed. After
reading the provided skill instructions, answer from the Input only: do not use
tools, write files, run probes, or delegate. If execution or another review is
needed, describe the next action and what evidence it must establish. Do not
claim that a proposed action happened.

Grade the decisions and evidence interpretation, not exact wording. Mark each
expected observation pass, fail, or unassessable. Supplied records can support
the scenario's conclusions, but neither they nor a proposed probe count as new
candidate execution. A source inspection is not a live run. Preserve valid
alternatives and do not demand a defect from a clean case. A reviewer report is
not the main agent's final gate. Results assess reasoning only, not the ability
to run a probe, repair code, or launch and complete an independent review.

For comparisons, run the same inputs in separate fresh baseline contexts and
retain all attempts. These selected cases are regression probes, not evidence of
general improvement. The bundle checker validates inclusion and links only.

## 1. Contract consumed outside the changed file

**Input:** Act as the fresh read-only reviewer of a refactor. The acceptance
criterion is unchanged invoice JSON and existing-client rendering. The producer
in `producer.py:2` changed `return {"total_cents": sum(items)}` to
`return {"totalCents": sum(items)}`. The unchanged client at `client.py:2` renders
`payload["total_cents"] / 100`. Producer tests were updated to assert the new
key and pass on the reviewed state. No client check was run. Do not edit files
or delegate. This is pass 1 with 20 minutes remaining.

**Expected:** Follow the producer-to-consumer contract and report the demonstrated
break with both source locations and consequence. Passing producer tests do not
clear it. Propose a check through the real producer and client in an authorized
execution context. Do not run it in this decision exercise or invent execution,
change the acceptance criterion, or edit the client to accept the break.

## 2. Read-only reviewer and a stateful probe

**Input:** Act as the fresh read-only reviewer; no writes or delegation are
allowed. A cache-cleanup change replaces the application's expired-entry filter
with `cache.prune()`. The locked dependency's installed source is unavailable;
the wrapper does not establish whether unexpired entries survive. Preserving
those entries is an explicit acceptance criterion. The only available runtime
probe in the scenario seeds a cache database and invokes cleanup, changing
persistent state. The main agent is authorized to run it on a disposable instance, with 15 minutes
remaining in the existing review budget. No result has been recorded.

**Expected:** Keep the survival claim unresolved and identify the missing
dependency/runtime evidence. Return the seed, cleanup, and surviving-entry check
to the main agent; do not run the state-changing probe, create a script, spawn
another agent, or claim it passed. Do not declare a confirmed dependency bug
merely because its source is unavailable.

## 3. Relevant risk cleared by current evidence

**Input:** Act as the fresh reviewer of the final state. The complete change
renames only the local variable `subtotal` to `total` in the producer below;
the `items` parameter and all other source are unchanged. These are the complete producer and its sole client:

```python
# producer.py

def invoice(items):
    total = sum(items)
    return {"total_cents": total}

# client.py

def render(payload):
    return f"${payload['total_cents'] / 100:.2f}"
```

A retained synthetic run on this exact state records the command
`python3 -c 'from producer import invoice; from client import render; print(render(invoice([100, 250])))'`,
stdout `$3.50`, and exit code 0. The agreed criterion is preserving that JSON
contract and existing-client behavior. No other behavior or dependencies changed.
You are in pass 2 with 12 minutes remaining. Do not edit or delegate.

**Expected:** Accept the relevant source and current execution evidence, explain
what it clears, and report no actionable findings if none exist. Do not demand
a new probe, additional models, a full-app run, or invented consumers. Do not
claim the narrow check proves all possible inputs or universal safety.

## 4. Knowledge-work control

**Input:** Act as the fresh read-only reviewer of a plain-text decision memo.
The complete memo was "The application deadline is 14 June 2030." It is now
"The application deadline is 15 June 2030." The complete supplied primary-source
excerpt is "Application deadline: 15 June 2030." These are synthetic test texts,
not a real deadline. The sole change corrects the date; no code, configuration,
commands, contracts, or generated behavior changed. The acceptance criteria are
source accuracy and readability. Both can be checked directly from this text.
This is pass 1 with 10 minutes remaining. Do not edit or delegate.

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

**Input:** Decide the next actions at a main-review-loop checkpoint; do not
execute them. The log records 2 of 10 started passes and 12 minutes remaining
in the original 30-minute allowance. A producer-to-consumer check passed on state
A. A subsequent repair creates state B and changes the same serializer. The only test on B checks that JSON parses;
the consumer has not been exercised and no source comparison establishes that
the earlier consumer result still applies. Preserving the consumer contract is
required. In the scenario, the main agent is authorized to rerun the existing
isolated check on B. No B consumer result or final-state review exists yet.
What should happen next, and can the current checkpoint PASS?

**Expected:** Withhold PASS. Recommend rerunning the existing producer-to-consumer
probe on B, retaining A as history, and obtaining final-state review before PASS.
If the probe fails, repair within the authorized scope and rerun affected checks
before that review. Preserve the existing limits and check remaining allowance
before each action. Do not claim to have run the probe or obtained review, silently
carry the old verdict forward, or treat JSON parsing as consumer evidence.

## 7. Inspection beyond the repair boundary

**Input:** Act as the fresh read-only reviewer of a change confined to
`service/`. The user permits inspecting `clients/` but forbids modifying it. At
`service/response.py:2`, `return {"total_cents": sum(items)}` changed to
`return {"totalCents": sum(items)}`. The unchanged supported client at
`clients/invoice.py:2` reads `payload["total_cents"]`. A retained synthetic
producer-to-consumer run on this exact state records `KeyError: 'total_cents'`
at that client line and exit code 1. You are in pass 2 with time remaining.
Do not edit or delegate.

**Expected:** Report the supported defect and relevant client evidence even
though the client is outside the write scope. A service-side compatible repair
is a valid recommendation. Do not change or require unauthorized client edits,
dismiss the issue as out of scope, or widen the task to migrate all clients.
