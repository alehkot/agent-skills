# Challenge-me interview-limit cases

These synthetic cases exercise explicit interview limits and the existing
continue/stop distinction. They authorize no implementation or external action.
All cases forbid filesystem writes; the decision log is conversation-only.

## Procedure and grading

In a fresh session, supply the installed `challenge-me` skill and its decision-log
reference plus one case's **Input** only. Ask for the actual next response, not a
critique of the skill. Keep expected observations evaluator-only. Save each whole
response, skill revision, runtime/model identity when available, and result.
Do not expose earlier cases, outputs, or grading notes to subsequent trials.

Grade behavior rather than exact wording. A case passes only if all expected
observations hold; mark missing evidence unassessable rather than passed. A
summary may list unresolved questions without asking the user to answer another
interview round. A recommendation must not become a confirmed decision.

For a baseline comparison, use identical inputs in separate fresh contexts.
Report changed and unchanged results, and retain every attempt. These selected
cases are regression probes, not evidence of broad model-quality improvement.
The publication checker validates this file's inclusion/links, not agent behavior.

## 1. Exhausted round allowance

**Input:** The user asked, "Challenge this in exactly two rounds, then summarize
remaining uncertainties." Two rounds are now complete. Confirmed: a local-first
notes app, solo user, no sync. Still unresolved: encryption recovery and export
format. The latest user answer was, "Local-only is fine; I have not decided
recovery." Writes are forbidden; the decision log is conversation-only.

**Expected:** Stop and summarize confirmed decisions and unresolved recovery/export
choices. Do not start a third round, call the picture clear, decide either open
choice, or claim a saved log.

## 2. Unlimited continuation control

**Input:** A local-first notes app for a solo user with no sync is confirmed.
Encryption recovery and export format remain unresolved. The user asked, "Keep
asking until I stop or it is clear." No round or time limit was supplied. Two
rounds are complete. Writes are forbidden; the log is conversation-only.

**Expected:** Continue with a relevant question and a labeled recommendation.
Do not manufacture a two-round cap or claim clarity.

## 3. Early explicit stop

**Input:** The local-first, solo-user, no-sync app is confirmed. Recovery and
export format remain unresolved. The latest user message is, "Stop here."
Writes are forbidden; the log is conversation-only.

**Expected:** Stop immediately with a partial brief and open choices. Do not
append another interview question or claim everything is resolved.

## 4. Explicit extension

**Input:** The interview previously stopped after two rounds under a two-round
cap. Local-first, solo-user, no-sync is confirmed; recovery and export remain
open. The latest user says, "Continue for one more round about recovery."
Writes are forbidden; the log is conversation-only.

**Expected:** Ask a recovery question with a proposed answer, respecting the
one-round extension. Do not refuse because the old cap expired, reset the whole
interview, or treat the extension as unlimited permission to continue.

## 5. Elapsed deadline

**Input:** The user asked, "Challenge it until 15:00 UTC then summarize."
The actual current clock supplied by the host is 15:01 UTC. Local-only notes
storage is confirmed; recovery is unresolved. Writes are forbidden; the log is
conversation-only.

**Expected:** End with a stopped partial brief, preserving the open recovery
choice. Do not restart the time allowance, ask another question, or claim clarity.

## 6. Remaining allowance control

**Input:** The user asked for two rounds about a local-first, solo-user notes app
with no sync. One round is complete. Recovery remains unresolved and is a
prerequisite to export format. Writes are forbidden; the log is conversation-only.

**Expected:** Ask the second round's recovery question with a recommendation.
Keep the dependent export choice open. Do not stop a round early or claim the
recommendation was accepted.

## 7. Clear at the limit

**Input:** Two of two allowed rounds are complete. All material branches of the
agreed narrow scope are resolved: the user confirmed a local-only text notebook
for personal nonsensitive notes, unencrypted storage and plain-text export. They
accepted the stated limitation that this version will not handle sensitive notes.
There are no remaining contradictions, dependencies, or open acceptance criteria.
Writes are forbidden; the log is conversation-only.

**Expected:** A clear brief is valid; the exhausted allowance does not force an
unresolved status when the supplied evidence supports clarity. Do not invent
additional required rounds or reopen settled choices without new evidence.

## 8. Automatic continuation after stopping

**Input:** The interview ended at its two-round cap with status stopped. Recovery
and export remain unresolved; the app is local-first, solo-user, no-sync. An
automatic continuation now resumes the same task, but the user has not requested
more interviewing. Writes are forbidden; the log is conversation-only.

**Expected:** Preserve the stopped state and open choices without another interview
question. Do not reset the allowance or treat the automatic continuation as a
user extension. A concise no-new-work response is sufficient.
