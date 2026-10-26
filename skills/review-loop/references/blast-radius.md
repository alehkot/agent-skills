# Blast radius within a review

Check whether the reviewed change breaks an existing consumer or behavior beyond
the edited lines. Use this for code, configuration, schema, and dependency changes
within an existing review pass. Scale the investigation to the change; a local
change with a demonstrated narrow effect needs only a short explanation.
Document-only reviews keep their source and audience checks.

## Trace the consequences

Describe the observable change, then follow the affected behavior to its relevant
consumers. A symbol search is a starting point. Where the change warrants it,
inspect serialized or persisted data, callers in other languages or processes,
feature flags, and ordering during callbacks, retries, or teardown. Check the
actual dependency version and local patches when its behavior matters. Stop when
the relevant effect is accounted for; do not invent consumers or audit unrelated
subsystems. Inspection may extend beyond the diff without expanding repair scope.

Identify the specific assumptions that decide a consequential risk. For example,
a serializer refactor may depend on preserving a field consumed by another
process; a cache cleanup may depend on the library removing only expired entries.
Choose the assumptions supported by this change, without requiring a fixed number
or a checklist of hypothetical failures.

## Check the decisive assumptions

Separate what the author asserts, what source inspection establishes, and what
execution demonstrates. Cite the relevant path, version, and artifact state.
For behavior that source alone cannot settle, use the smallest check that can
expose the proposed failure: an existing test, a call through the real dependency,
or a producer-to-consumer probe. Exercise the actual user surface when a narrower
check cannot establish the required outcome. A mock or a successful build cannot
prove behavior it does not exercise. Reuse sufficient current evidence; a fresh
script or full application run is not mandatory for every change.

The fresh reviewer stays read-only and does not delegate. It may run only checks
consistent with that boundary. If a probe requires writing a script, modifying
state, or driving an app with side effects, return the exact proposed check and
the observations that would confirm or clear the risk. The main agent performs
authorized execution and repairs within the remaining review budget, using the
verification recipe when useful. Check commands for side effects before running
them; a test can write caches or fixtures. Proposed checks are not results.

Record the affected consumer, decisive assumption, evidence, and outcome in the
existing review log or verification record. Keep these outcomes distinct:

- **Confirmed defect:** evidence demonstrates a violated requirement or existing
  behavior. Assign severity by its actual consequence and use the normal repair
  loop. An out-of-scope repair remains open for the necessary decision.
- **Cleared risk:** evidence rules out the stated failure for the reviewed state.
  Explain the boundary of that proof; it does not establish universal safety.
- **Unresolved risk:** a concrete relevant failure path still lacks decisive
  evidence. Name the missing check and why it matters. Missing evidence alone
  does not establish a defect or its severity.

An unmet acceptance criterion or unresolved risk at the selected severity blocks
PASS under the existing gate. Speculation alone does not create a blocker. Keep
checks, findings, and their verdicts tied to the state actually examined; rerun
affected checks after a repair and re-review the final result. This procedure
adds no passes, time, permissions, mandatory scripts, or separate review loop.

Workflow ideas adapted from pstack's
[blast-radius skill](https://github.com/cursor/plugins/blob/e73df471cd4bd918367e99f3dd9c51bd53ddf5f0/pstack/skills/blast-radius/SKILL.md).
This reference is self-contained and requires no pstack installation.
