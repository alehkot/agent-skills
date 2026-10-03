# Evidence-based evaluation rubric

Assess the evaluation artifact for its stated purpose and stage. Do not confuse
its quality with the candidate's task success. Set the scope before scoring; never
shrink it after discovering a consequential failure to obtain a better rating.

## Rating rules

- **0 — deficient:** inspected evidence demonstrates a material error or a known
  required element is absent from a sufficiently complete inspected artifact.
- **1 — partial:** evidence establishes a useful part and a specific unfinished
  part. Name both. This is not a compromise rating for uncertainty.
- **2 — adequate:** checked evidence satisfies the criterion for the stated
  decision and stage. Name the check and its scope; adequacy is not perfection.
- **Unknown:** unavailable or conflicting evidence prevents assessment. An
  unattached manifest does not prove cases are missing. Request only the evidence
  necessary to resolve the decision.
- **N/A:** the criterion or subdimension is irrelevant to this bounded request,
  with a reason. Unknown capability is not absent capability.

Use the criterion-specific anchors below. Explain legitimate deviations when
the task has a different evidence standard; do not invent new product requirements.

| Criterion | 0: demonstrated deficiency | 1: partial | 2: adequate evidence for the stated scope |
| --- | --- | --- | --- |
| Purpose | The eval rewards a proxy that can contradict the required outcome, or answers a different decision. | The job is identified but the candidate, outcome or decision rule still has a consequential unresolved branch. | The decision, intended behavior and scope follow the inspected request or contract; any consequential threshold is justified. |
| Coverage | An inspected inventory omits a required consequential behavior or known causal sequence. | Some relevant obligations have discriminating cases; named obligations or boundaries remain unfinished. | Applicable obligations map to concrete cases and oracles; legitimate use, meaningful boundaries and known causal interactions are represented, with bounded exclusions. |
| Reference correctness | A decisive label, fact, policy interpretation, formula or expected state is demonstrably wrong or imports an unstated premise. | A supported basis exists, with specifically identified derivations or labels still to check. | Decisive results are traced to actual facts or verified derivations; alternatives and unresolved semantics are preserved. |
| Discrimination | A check accepts a consequential defect or rejects behavior allowed by the contract. | Some contrasts are sound; identified valid alternatives or important defects have not been checked. | The actual check distinguishes relevant good/bad and alternative-valid cases. An inspectable deterministic predicate can be proved on inputs at design stage; a predicted LLM verdict is not executed validation. |
| Realism | Required information/capabilities are inaccessible to the candidate, observations cannot establish the outcome, or the environment contradicts the claim. | Relevant environment pieces are represented but specific dependencies, state or observation paths remain provisional. | Inputs, permissions, state, reset and observations fit the bounded claim; modeled dependencies and omitted surfaces are explicit. Design adequacy does not establish live fidelity. |
| Measurement integrity | A known confound, leaked label, altered rubric, omitted outcome or invalid denominator defeats the claimed comparison/conclusion. | An appropriate protocol or traceable result exists with named implementation/accounting gaps. | Versions, comparable evidence, controls and planned outcomes support the actual metric and inference. For a proposal, this rates the specified protocol; future adherence remains unverified. |
| Proportionality | Mandatory work has no relevant obligation, or omission of necessary checks leaves the decision unsupported. | The core is relevant but some required work lacks a clear decision benefit or scope remains unresolved. | Existing sufficient checks are reused; each additional case/check resolves a material uncertainty, and the stopping point matches the decision. |

Do not supply generic scores for unseen artifacts. Treat a reported result as a
report until its supporting evidence is inspected. A single confirmed defect can
justify 0 in its bounded criterion even when other evidence is unavailable.
For coverage, distinguish a confirmed omitted obligation from a merely incomplete
inspection. Materiality comes from the actual decision and consequence, not from
every desirable feature mentioned in a checklist.

## Record evidence and execution separately

A row can use `criterion | rating | evidence/check | gap or limit | next action`.
Add execution status once for the artifact, or per case when stages differ:

- **Proposed:** a case or protocol is described.
- **Implemented:** a runnable artifact/check exists.
- **Verifier-checked:** the relevant check has been exercised or independently
  established on appropriate controls; record how and for which assertions.
- **Candidate-executed:** candidate evidence exists; report its passes, failures,
  invalid outputs and unresolved results separately.

Stages describe evidence, not an automatic increasing numeric score. A logically
checked predicate can support a design judgment without candidate execution.
An implemented semantic judge with only proposed controls has not been validated.
The same supplied evidence must yield the same assessment in design and review.

Use a profile of ratings and blockers, not a default sum. Ordinal ratings are not
equal-distance measurements. If the user explicitly needs a composite, expose
its purpose, weights, applicability denominator and Unknown treatment; retain
critical blockers separately and do not turn it into release authorization.
N/A and Unknown are never converted to favorable scores or silently dropped to
inflate a percentage. No universal passing score is implied.

## Short examples

**Proposed duration conversion checks.** Contract says "2 hours" maps to
`{"minutes":120}`. The proposed check parses JSON, requires exactly the key
`minutes`, requires a number, and compares the value to 120. Inspection shows
it accepts the required output and equivalent whitespace, rejects 121 and a
missing key. Reference correctness: **2**, because 2 × 60 = 120 was checked.
Discrimination: **2 for this deterministic case**, based on the inspected
predicate and contrasts. Execution status: **proposed; not run on a candidate**.
Broader parsing coverage is not established by this single case. This does not
require accounts, a security platform or a paid judge.

**A misleading report.** Supplied records show eight passes, two failures and
two timeouts among twelve planned attempts; the report says "80%, complete".
Measurement integrity: **0**: 8/10 describes completed attempts, and 10/12
completed, so completeness is false. Inspect timeout causes before assigning
them to agent or infrastructure failure. Repair the denominator and status;
do not invent model-answer controls for an arithmetic finding. Raw logs absent
from a summary remain uninspected even when its arithmetic can be checked.

**A good check finds a bad answer.** Inspected comparator requires `total=15`,
accepts the reference 15 and rejects 14; the candidate produces 14. Discrimination:
**2 for that value check**. Candidate outcome: **fail**. Do not downgrade the
evaluation because it detected the defect, or increase its rating just because
a different candidate passed.
