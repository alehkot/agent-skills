# Review evidence and accounting

## Severity

Use impact under the task's actual requirements and environment. The following
mapping is this skill's convention, not an assumption about another tool's labels.

| Severity | Priority alias | Meaning |
| --- | --- | --- |
| Critical | P0 | Fundamental failure or immediate serious harm, such as destructive data loss or exposed credentials. |
| High | P1 | A core requirement fails or a substantial security, privacy, or reliability defect blocks the intended use. |
| Medium | P2 | A concrete, consequential error, missing requirement, or supported failure path needs correction before this task is complete. |
| Low | P3 | A minor issue or improvement that does not materially prevent the agreed outcome. |

"Medium and above" means P0, P1, and P2, not numerically larger priority values.
Style preferences and speculative future requirements are not medium defects.
For source-based writing, a materially unsupported claim can be medium or higher;
code is not required for the rubric to apply. Explain severity through impact.

## Persistent review log

Keep a compact current state plus an append-only record of passes and changes:

```markdown
# Review: <task>
Run: <stable local identifier>
Scope: <full task, artifact paths, baseline/revision and acceptance criteria>
Threshold: medium and above
Limits: 10 started passes; 30 elapsed minutes
Started: <timestamp with timezone, set immediately before first review>
Deadline: <absolute timestamp, derived once from Started and the time allowance>
Passes started: 0
Status: ready | running | PASS | LIMIT_REACHED | BLOCKED | STOPPED
Reviewer mode: fresh-context | self-review fallback, with reason
Latest reviewed state: <revision or identifiable artifact state>

## Findings
| ID | Severity | Location and evidence | Disposition | Closure evidence |
| --- | --- | --- | --- | --- |

## Pass history
- <pass, start/end times, reviewed state, result, relevant coverage and limits>
- <repair, checks and outcomes; note that the final state needs another review>

## Overrides and restart
- <explicit user override, old/new limits or criterion, when it was supplied>
- <remaining findings, incomplete verification, next action and required input>
```

Use actual clock readings, not an estimate of model tokens. Start time and pass
count belong to the run, not the conversation. Record each attempted reviewer
invocation before starting it; a timeout or fallback retry is another pass.
Only the orchestrator writes this log. Preserve prior evidence when correcting it.

A pass admitted before the limit may finish within the remaining allowance.
Reaching pass ten prevents pass eleven; pass ten can still yield PASS if the
clean review and all required checks finish before the deadline. If pass ten
finds issues, fixes alone cannot satisfy the mandatory subsequent clean review.
Return LIMIT_REACHED, listing any repairs not yet re-reviewed. A result arriving
at or after the deadline is too late to establish a within-budget pass.

On explicit extension, retain Started and used passes. Translate "five more
passes" into a new total cap of used passes plus five; "ten more minutes" into
a deadline ten minutes from the actual extension time. A replacement total
budget is measured from the original start. Record the user's wording and
effective new deadline/cap; never reset historical usage. Recheck both limits.

If an active log or its timing evidence is missing or corrupt, do not invent a
fresh zero budget. Recover from reliable artifacts or return BLOCKED with the
missing evidence. If writing is prohibited, keep the same accounting in the
conversation and disclose it; if reliable accounting cannot be maintained, stop.

## Fresh reviewer prompt

Supply real task data in this shape, without importing the author's rationale:

```text
Review the complete task result against the supplied requirements and evidence.
You are read-only: do not edit files, run modifying commands, or spawn agents.
Read applicable instructions and enough source context to assess the whole scope.

Task and acceptance criteria: <user requirements and accepted decisions>
Scope and baseline: <all relevant changes/artifacts, not only the last fix>
Sources and checks: <paths and commands; verify their meaning and current results>
Severity threshold: <effective threshold and definitions>
Time available: <remaining allowance; stop before it expires>

Return findings with a stable description, severity, location, consequence,
evidence, and required correction. Separate demonstrated defects from unresolved
risks. Report covered scope and missing evidence. If there are no actionable
findings, say so; do not invent issues to satisfy the review request.
```

The main agent independently reconciles the findings. Closure of a confirmed
issue requires a verified repair or evidence that disproves the finding.
An unresolved relevant risk cannot be erased by renaming it an assumption.
When the original reviewer is unavailable, a self-review may satisfy this
skill's gate if equally complete, but never label it independent or fresh-context.

## Result

```text
Status: PASS | LIMIT_REACHED — not passed | BLOCKED — not passed | STOPPED — not passed
Scope: <task and actual final artifact state covered>
Threshold: <effective severity threshold>
Budget: <started passes/cap, elapsed time, deadline, and explicit overrides>
Findings: <open blockers, closed issues with evidence, and lower-severity notes>
Verification: <actual commands/source checks and outcomes; missing evidence>
Reviewer mode: <fresh-context or disclosed self-review fallback>
Review log: <actual path or conversation-only limitation>
Next: <none for a pass, otherwise concrete restart action and necessary input>
```

An extension is optional and user initiated. The final report should make it
possible without pretending the old criterion passed. A failed verifier, a
partial review, or a review that cannot access required evidence has a non-pass
result even if no new issues were discovered.

Report only the observed reviewer mode. If a supplied checkpoint omits it,
label it unknown; do not infer fresh or independent context from the default
workflow. Keep reviewer activity separate from verification process activity.
