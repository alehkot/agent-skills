# Check the decisions inside the change

Use this optional lens when implementation or a plan fills a material gap in the
request. A correct implementation can still choose a storage policy, public API
behavior, dependency, or responsibility boundary the task did not settle. Review
those choices within the existing scope, pass count and time budget. This does
not replace code review, execution checks or the user's decision authority.

## Recover the contract before judging a choice

Read the accepted request, relevant decisions, current source and whole change.
An implementer's summary helps locate choices but is not proof of their origin.
Use available authorized records; do not require private transcripts or invent
missing history. Separate a new choice from a pre-existing contract, a required
choice, and implementation discretion already delegated to the agent. Missing
text in one document does not by itself prove a choice was unauthorized.

Trace choices that constrain observable behavior or later work. Relevant examples
include where data is retained, what an error response promises, which component
owns retries, or whether new infrastructure is required. Skip cosmetic naming and
routine equivalent implementations unless they change a real contract. An empty
list is valid when the scoped change introduces no material choice.

## Keep permission and technical merit separate

For each material choice, record a short entry in the existing review log:

- **Choice and origin:** what changed, its location/revision, and the request or
  evidence it follows. Mark it required, delegated, existing, or unresolved;
  preserve uncertainty about origin rather than claiming an approval.
- **Consequence:** a concrete use case showing what happens with this choice,
  the meaningful alternative if one exists, and what later work depends on it.
- **Reason and evidence:** why it was selected, what supports the behavior, and
  what remains unknown. An inferred rationale stays labeled as an inference.
- **Disposition:** supported within scope, a confirmed defect with its violated
  criterion and severity, or a decision/evidence gap with the exact next step.

A delegated choice can still be technically wrong. A technically attractive
choice can still require user approval. Passing tests establish only the
behavior they exercise, not agreement with a product or retention policy. Do not
rank permission by confidence that the user would probably agree.

## Reconcile proportionately

Check apparent gaps against the whole task and existing delegation first. Do not
ask for approval of every unspecified implementation detail. When a consequential
choice is genuinely unresolved, explain the alternatives and recommendation;
leave the dependent work blocked until the required decision is obtained. A
reversible proposal, silence, or a recorded recommendation is not approval.
Continue independent authorized work without silently choosing that policy.

Use the normal review gate for defects and missing required evidence. The lens
is read-only for a reviewer: record the finding, then let the main agent reconcile
and repair within its authority. Do not change code or settle a choice just to
make the ledger look complete. Preserve accepted decisions, but reopen one when
new evidence contradicts it or the task materially changes; record what changed
instead of treating a previous entry as permanent authority.

Keep the entry only as detailed as needed to understand the consequence. Reuse
the established review log or project decision record where authorized; this
lens does not require a new permanent repository file or a second approval stage.
A ledger is evidence about the reviewed choices, not proof that all choices were
found or that the complete result passes.

Original guidance informed by David Zhang's
[audit-decisions](https://github.com/dzhng/skills/blob/a4076b71188eb7801df26b31e9d8fab1908c4654/skills/engineering/audit-decisions/SKILL.md).
This adaptation keeps decisions inside the existing review and permission rules;
it does not adopt automatic provisional decisions or replace diff review.
