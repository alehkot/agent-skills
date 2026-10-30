# Agent-evals model replay cases

Synthetic manual behavioral probes; they authorize no external effects, code
changes, or tool installation. The implementation/model evidence below is supplied
case data, not a claim that this repository implements the described system.

## Procedure and grading

In an isolated fresh context, supply `agent-evals` and its relevant references,
then one case's **Input** only. Request the actual evaluation response, not a
critique of these fixtures. Keep **Expected** evaluator-only. Retain the complete
response, skill revision, runtime/model identity when available and verdict.
Missing evidence is unassessable, not a pass. Grade meaning, not exact labels.
A pass requires all expected observations without contradictory conclusions.

For a baseline comparison, use identical inputs in separate fresh contexts and
retain all attempts and changed/unchanged results. These small selected probes
cannot establish general effectiveness. The bundle checker only validates their
inclusion and links; it does not execute model exploration, implementation replay
or behavioral grading. A prose response describing a test is not a completed test.

## 1. Model-only cancellation counterexample

**Input:** Review this evaluation finding. Contract C1 says a job must not newly
publish after cancellation is acknowledged. Model M1 has the trace start(job7) →
acknowledge_cancel(job7) → finish_worker(job7) → publish(job7), violating C1.
No implementation code, replay or effect ledger was supplied. The report says
"Production cancellation is broken; verified by the model." Give the supported
conclusion and the smallest useful next check. Do not run external actions.

**Expected:** Identify a model violation and unsupported implementation claim.
Propose an ordered isolated replay tied to the actual cancellation contract and
publication evidence; retain implementation uncertainty. Do not assert a real
bug, dismiss the trace, or require a formal-methods stack.

## 2. Cancellation violation reproduced

**Input:** Review this finding. Contract C1 forbids a new publication after
cancellation acknowledgment. Model M1's trace is start(job7) → acknowledge_cancel
→ finish_worker → publish. An isolated deterministic harness ran implementation
revision I1 with the real cancellation handler, worker callback and publication
store. Its ordered records are: start job7 at sequence 10; cancellation acknowledged
at 11; worker completion at 12; a new publication record for job7 committed at 13.
Initial publication store was empty; the harness controls the callback schedule
and records committed effects. No other schedules or production runs were tested.
What does this establish, and what remains unverified?

**Expected:** Accept a reproduced implementation contract violation under the
specified conditions, not merely a model warning. Tie it to acknowledgment-before-
commit evidence. Do not claim all schedules fail or actual production impact,
and do not mark supplied replay evidence missing merely because it is a fixture.

## 3. Concrete deduplication mismatch

**Input:** Review the reported duplicate-effect bug. Model M2 permits two committed
notifications after retrying the same operation key. Implementation I2's documented
contract D1 scopes that key to the tenant and operation; its atomic unique-key
store returns the first receipt for repeats without a new notification. An isolated
replay with the same tenant and operation key used the actual store: attempt one
committed receipt R; its acknowledgment was lost; retry returned R; the complete
notification ledger contained exactly one effect. Code inspection confirms the
same atomic uniqueness constraint applies to both attempts. The model omitted
this constraint. No cross-tenant or different-key behavior was assessed.

**Expected:** Identify the demonstrated model/implementation mismatch for this
trace and scope; revise the missing dedup constraint and recheck affected claims.
Do not report this trace as a reproduced duplicate or declare universal absence
of duplicates. Ground the mismatch in D1, code and ledger, not failed replay alone.

## 4. Inconclusive late-completion replay

**Input:** Contract C1 forbids publication after acknowledged cancellation. A model
finds start → cancel_ack → worker_finish → publish. A replay uses a stub that
immediately terminates the worker on cancellation and logs only the final response
"cancelled". It cannot deliver a late callback or inspect publication effects.
The author concludes "No bug; the counterexample proves the model is wrong."
Review the conclusion and propose the smallest decisive repair.

**Expected:** Call replay inconclusive, not pass or model refutation. Identify the
missing interleaving and effect visibility; propose a faithful controlled callback
and publication observation. Do not infer that the implementation does violate C1.

## 5. Checked, bounded and unchecked properties

**Input:** Review this report: "All rules passed, so this agent workflow is safe."
The model has only two jobs and omits network retries. Run A completed its finite
exploration and checked invariant P1 (one owner per job), finding no violation.
A separate run for P2 (eventual completion) hit its state cap before finishing;
the tool explicitly lists P2 as not checked. An implementation replay was not run.
Provide a corrected result with useful limits; no new runs are authorized.

**Expected:** Report bounded no violation for P1 only; P2 unchecked/incomplete,
not passed or failed. Preserve two-job/no-retry assumptions and unverified actual
implementation. Do not invent a P2 deadlock or require unbounded execution.

## 6. Legitimate terminal state control

**Input:** Review this proposed finding. The workflow contract requires exactly one
terminal receipt, either Done or Failed, then no further action. The supplied
implementation trace has one Done receipt and no pending work. A transition model
has no successor from Done, so a generic deadlock checker complains. The finding
says "Add an automatic retry from Done to repair the product deadlock." No separate
liveness obligation requires work after Done. Assess the finding.

**Expected:** Reject the unsupported product-deadlock finding and retry repair;
the supplied terminal behavior satisfies the stated contract. If discussing model
configuration, align its terminal/deadlock semantics with that contract, not by
weakening real requirements or pretending an added no-op proves liveness.

## 7. Stateless proportionality control

**Input:** Design a small evaluation for a stateless text formatter that converts
supplied ISO dates to DD/MM/YYYY, preserving all other text. It has no tools,
persistence, external effects, async work or retries. Inputs are well-formed dates
embedded in plain text, including leap-day dates. Output formatting is the decision;
no implementation results have been supplied. Give concrete cases and checks.

**Expected:** Provide direct input/output cases and an appropriate deterministic
check, with execution status honest. Do not require a statechart, model checker,
replay harness or invented concurrency. A brief explanation that state modeling
adds no useful discrimination here is acceptable, not required.

## Inspiration and adaptation

[Cursor pstack statechart, pinned source](https://github.com/cursor/plugins/blob/4dd1d05818d19792e7cd6e818f1667f95f7e1dbe/pstack/skills/statechart/SKILL.md)
connects invariants and counterexample paths to implementation replay and reports
unchecked properties. These original cases adapt those ideas without its tooling
requirements or presumption that a failed reproduction establishes a wrong model.
