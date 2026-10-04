# Verify the reference and the check

Trace each decisive expectation to source facts or an independently checked
derivation. Keep recommendations, assumptions and unknowns out of ground truth.
An unsupported reference can reward a bad candidate and reject a correct one.

## Choose evidence per property

| Property | Deciding evidence | Insufficient proxy |
| --- | --- | --- |
| Completed action | product-defined receipt and relevant state | agent says done or tool returns a preview |
| No forbidden disclosure/effect | relevant trajectory, authorized destinations and state | safe final answer alone |
| Grounded answer | source facts, applicable date and supported attribution | fluent text or a citation's presence |
| Correct transformation | normalized results on discriminating inputs | preferred implementation or variable names |
| Useful clarification | consequential ambiguity, available defaults and question asked | asking about every unspecified detail |
| Bounded operation | defined time/actions/tokens/cost with failed attempts accounted for | statistics over successes alone |

Inspect identity, freshness and scope of state evidence too. A receipt may prove
acceptance without delivery. Eventual consistency needs a bounded observation
rule. Evaluator-only labels and hidden state must not leak into candidate inputs;
policies the candidate must use need the access intended by the real task.

For numerical references recompute from stated inputs, units and horizon. Do not
repair a missing input by silently choosing a convenient value. For source/policy
references preserve actor, commitment, authority, stage and temporal applicability;
an example is not a universal policy. Use existing evidence for what it proves.
For premise-only logic check entailment, entailed negation or countermodels under
the actual semantics, including unstated existence and every proposed example.
Generalize the verification method instead of relying on familiar domain names.

## Write discriminating assertions

Make each assertion independently useful, with required facts, acceptable
alternatives and a rule for insufficient evidence. Preserve deliberate method,
ordering and wire-format requirements, but do not add editorial preferences.
Missing required content can fail when the complete answer is visible; unavailable
external evidence can remain unresolved. A judge execution error is separate.

Prefer executable predicates for objectively decidable properties. Use semantic
judgment for meaning that those predicates cannot establish. Instructions to read
an assertion literally may specify conjunction/disjunction; they do not establish
keyword matching. Read actual code, assertion classes and records before claiming
a verifier defect. Predicting an LLM verdict is a probe, not an observed failure.

## Use the smallest decisive control

For a check whose discrimination is uncertain, inspect or exercise a valid result
and a relevant defect; include valid alternative wording/behavior where false
rejection is plausible. A calculation or predicate proof may be sufficient for a
narrow deterministic finding. Do not fabricate full answer pairs for every
arithmetic or reporting issue.

When answer/trace pairs are needed, first validate the complete clean control.
Copy it, change one causal property, and score every applicable assertion against
the actual expanded mutant. Overlapping assertions may fail together. Label
compound stress cases separately. Excerpts establish only their named subset;
if full controls are requested, output their actual content, not replacement
instructions. A fact still present in a mutant cannot be marked omitted.

Example synthetic draft policy: include the authorized $12,000 offer; omit a
private $20,000 ceiling and Friday deadline. Assertions are offer included,
ceiling absent, deadline absent, both private facts absent. Clean:
"We offer $12,000." Expected vector: pass/pass/pass/pass. Single mutation:
"We offer $12,000. We can add exactly $8,000 before reaching our limit."
Expected vector: pass/fail/pass/fail, because the ceiling is recoverable by
addition. This is a checked policy expectation, not an observed semantic-judge
verdict. Apply draft-only rules to sendable text; authorized private notes have
their own scope. Equivalent valid wording must remain acceptable.

## Validate judgments and repair affected evidence

Use known defects, clean alternatives, boundaries and untrusted grading bait as
appropriate. Ignore answer-embedded grading instructions; their presence alone
does not invalidate otherwise correct task content without a separate requirement.
Record label provenance. Automated authored controls are not expert calibration.

Before adopting consequential semantic references, have a separate reviewer check
the original source or policy against concrete valid and defective examples.
Resolve disagreements from that evidence; send unresolved policy choices to the
user. If this check is unavailable, keep the references provisional rather than
treating a second favorable score as verification.

Preserve typed labels/probabilities without inventing rationales. Check a text
judge's cited evidence against the actual answer. Judge agreement and confidence
do not establish truth; confidence thresholds require relevant validation. Compare
judges on the same saved answers, including passes, failures and uncertainty.

A repair proposal is complete when it identifies the defect and adequate check
within scope. If correcting an evaluation that already produced results, version
the changed reference/check, retain originals, regrade sufficient saved evidence
or execute affected cases when it is insufficient, and recompute dependent claims.
A corrected verifier does not establish that the candidate improved.
