# Verification recipe

Use this optional recipe when a check needs setup, multiple actions, or evidence
that must survive repairs and cleanup. Keep it beside the review log or at the
user's requested path; do not install a project skill or commit scratch evidence
by default. For a simple check, record the same essentials inline. This adds no
permissions, acceptance criteria, reviewer passes, or time allowance.

## Contents

- [Plan the check](#plan-the-check)
- [Exercise and retain evidence](#exercise-and-retain-evidence)
- [Knowledge-work examples](#knowledge-work-examples)
- [Judge the check, then the review](#judge-the-check-then-the-review)

## Plan the check

Start from the agreed requirement and existing project instructions or harnesses.
Choose the smallest check that observes the claimed outcome at its actual surface:
a user action for a UI, a documented command for a CLI, a request for a service,
or direct inspection, source comparison, and relevant rendered-output inspection
for documents, slides, analyses, or other knowledge work. Do not replace
a required user path with an internal setter, test-only endpoint, or source reading.
Record any mock, dry-run, or stand-in and the boundary it leaves unverified.

Identify the artifact to be exercised or inspected, not just its source material.
Use a commit plus relevant dirty changes, a content hash, a document version, or
another reproducible state identifier. A commit alone does not identify modified
files; source revision alone does not prove which binary or deployment is running.
Record environment, build, data, and configuration where they affect the result.
If identity cannot be established, leave that verification blocked.

For each required check, fill the plan before running it; fill observations only
from actual execution or inspection. Do not turn placeholders into results.

```text
Check ID and acceptance criterion:
Artifact/state to verify and how to confirm it:
User path or inspection surface:
Preconditions: environment, data, access, readiness, isolation
Actions: exact commands, inputs, interactions, or source comparisons
Expected outcome:
Expected and forbidden side effects; how each will be observed:
Evidence to retain and location outside disposable run state:
Cleanup: owned resources to remove and evidence to preserve

Run time and artifact/state actually verified:
Actions actually performed:
Observed outcome and side effects:
Evidence locations and what each demonstrates:
Cleanup result and evidence availability afterward:
Verdict: PASS | FAIL | BLOCKED
Missing coverage, blocker, and next action:
```

Use "not applicable" with a reason for irrelevant fields. Missing evidence is
not "not applicable." A proposed recipe remains unexecuted until run; it cannot
close a finding. Check remaining review time before setup, execution, and cleanup.

## Exercise and retain evidence

Confirm preconditions and target identity before exercising or inspecting the
artifact. Process health, successful startup, and a ready screen are setup
evidence, not feature evidence.
Use isolated data or an owned instance where possible. Stop before unapproved
external actions or data changes; a recipe cannot authorize them. A label such
as "dry-run" is not evidence that a command has no side effects.

Capture enough to connect the action to the observed outcome: commands and their
outputs, a request and response, an interaction trace and resulting state, or
specific artifact passages, supporting sources, and relevant rendered pages or
slides. Inspect the actual required output and relevant side effects, including
forbidden changes. Exit zero alone, a final screenshot without the required
interaction, and an author's statement that a check passed do not establish
the claimed behavior.

Keep evidence from failed attempts too. Clean up only resources this run owns,
including after failed attempts, and record unresolved residue. Keep proof outside
disposable directories and confirm it remains readable after cleanup. Redact
secrets or unnecessary personal data without destroying the evidence's meaning.
Do not publish private evidence merely to make it easier to link.

## Knowledge-work examples

These are illustrative check plans, not executed results. Use only the concerns
required by the task; a short direct inspection can remain inline in the log.

- **Decision memo:** For a memo comparing three options, record its version and
  the supplied source versions. Map each requested option to a section, compare
  material claims with their sources, and check that the recommendation follows
  from the evidence and answers the intended reader's decision. Retain the
  section/source locations and any reasoning gaps. Inspect rendered pages if
  pagination or layout matters. A contradicted material claim is FAIL; an
  unavailable necessary source is BLOCKED, even if the prose reads well.
- **Slide deck:** For an eight-slide briefing, identify both the final deck and
  its rendered export. Check the narrative and required content against the
  audience and purpose, trace material chart figures to their sources, and
  inspect every rendered slide at its intended viewing size for readable labels,
  clipping, overlap, and layout. Retain slide-specific observations and images
  plus source checks. Text extraction alone cannot pass a required visual check;
  unavailable rendered evidence leaves that check BLOCKED. After a repair,
  render the changed deck again and verify the affected output before final-state
  review.

## Judge the check, then the review

- **PASS:** the identified state was actually exercised or inspected, the
  requirement and expected side effects were observed, forbidden effects were
  checked and absent, and the necessary evidence survives cleanup.
- **FAIL:** an observation demonstrates a mismatch with the requirement, including
  an incorrect output or a forbidden side effect. Preserve that finding even if
  another part of verification is blocked.
- **BLOCKED:** a prerequisite, permission, target identity, or necessary evidence
  is missing, stale, or inaccessible, so the outcome cannot be established.
  Record what was attempted and the precise gap; do not infer a product defect
  solely from unavailable verification.

Report checks separately so a passing subset cannot hide failures or gaps. A FAIL
or BLOCKED required check prevents overall review PASS. Continue or stop using
the review loop's existing gates and budget; these check verdicts do not replace
its final result statuses or its mandatory final-state review.

After a repair, rebuild or reload the target as needed, confirm its new identity,
and rerun affected checks. Retain earlier results as history, not proof of the new
state. Explain why any carried-forward evidence still applies to unchanged scope.
Recheck a corrected recipe or harness by exercising the affected path; editing
verification instructions alone does not verify either the harness or the artifact.
