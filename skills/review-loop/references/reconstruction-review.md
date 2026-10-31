# Reconstruct before critiquing

Use this optional lens when a design document, implementation plan or handoff
must communicate its meaning to a new reader. It is part of an existing review
pass, not a separate workflow. Skip it when it adds no useful evidence, such as a
small code-only correction with an already clear contract.

## Give the reviewer the right material

Provide the artifact, its intended audience and purpose, accepted requirements,
and necessary source references. Do not provide the author's private explanation
of what the artifact was supposed to say, expected paraphrases, or earlier review
answers. Do not withhold safety constraints or accepted task requirements in the
name of isolation. Keep the reviewer read-only under the usual protocol.

## Reconstruct the meaning

Before listing findings, briefly state in the reviewer's own words:

- What outcome or behavior the artifact proposes, or what the handoff asks the
  next agent to do.
- What current state, dependencies and constraints it relies on, according to
  the artifact and its explicit references.

Trace a relevant mechanism or next action, rather than restating headings. Name
what cannot be determined instead of filling gaps from general knowledge. Read
relevant linked material and check the rest of the artifact before declaring an
explanation absent. Keep the reconstruction even if there are no findings; it is
useful evidence of what the reviewer understood. A short, unambiguous artifact
may need only a sentence for each point, not a new report file.

## Reconcile without manufacturing defects

Compare the reconstruction with the accepted task and actual sources. If it
reveals a consequential ambiguity or missing connection, report its location,
competing interpretations and effect on the intended reader or execution.
Defined terms alone do not establish a coherent explanation. Conversely, a
paraphrase that differs in wording but preserves the contract is not a defect.

A mistaken reconstruction may reflect a reviewer error, inaccessible evidence,
or a genuine artifact gap. Establish which before editing; do not automatically
rewrite a correct artifact to match a mistaken reviewer. Relevance and severity
still depend on the user's requirements and audience. Ordinary engineering
terms, future proposals clearly labeled as such, and explicitly delegated
implementation choices do not automatically require more detail or approval.

Record confirmed findings, cleared misunderstandings and unresolved evidence
separately in the existing review log. Do not insert the author's preferred
answer into the next review brief to make it pass. Correct missing legitimate
context when needed, then reassess under the same pass/time accounting. A
reconstruction is not execution evidence, an eligibility decision, or permission
to implement the plan. Preserve the existing final-state review gate.

This independently written lens draws on EGM's
[comprehension reviewer](https://github.com/google/elephant-goldfish-model/blob/403d8881d62022490637d740657b33f01e321ea8/agents/comprehension.md).
It requires no EGM installation and does not adopt its full staged workflow.
