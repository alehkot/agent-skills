---
name: brief-and-dispatch
description: >-
  Turn an intended task into a concise execution brief with observable completion,
  verification, boundaries, and ownership. Use before delegating work or preparing
  an unattended run, especially when success or task boundaries are unclear.
  Dispatch only when execution is requested and authorized; a brief alone does
  not launch workers. Use handoff for continuing already-started work instead.
---

# Brief and Dispatch

Make the smallest useful assignment that another agent can execute and check
without reconstructing the request. A simple, clear task needs only a few lines,
not a planning ceremony or mandatory parallel workers.

## Ground the assignment

Read the request, accepted decisions, available artifacts, and current work.
Inspect discoverable facts before asking the user to describe them. Point to
repository conventions and commands instead of copying them into the brief.
Spend words on context the executor cannot infer: who needs the outcome, why now,
accepted tradeoffs, and relevant decisions outside the artifacts.

Separate requirements, observed facts, delegated choices, and unresolved
assumptions. Ask only for missing information that changes the scope, success
criterion, or a consequential decision and cannot be discovered. If the objective
is still exploratory, make evidence gathering the bounded task rather than invent
an implementation target. Recommend a decision when useful, but do not treat the
recommendation as approval. Continue independent authorized work when blocked.

## Write the brief

Include only decision-changing information, grouped as suits the task:

- **Outcome:** intended user and observable result; smallest useful slice and
  explicit non-goals. Do not invent a performance target or feature requirement.
- **Evidence of done:** the check, artifact or user path that establishes each
  important acceptance condition, with known commands/source pointers and the
  result to inspect. For a behavior change, include a relevant regression check.
  Separate mechanical checks from judgment that needs review. A passing unit
  test does not establish an untested user journey; a screenshot alone does not
  establish an interaction. State required checks that are unavailable, not a
  promise they will pass. For discovery, define the evidence and decision to
  return rather than a guaranteed fix.
- **Boundaries:** authorized scope and side effects, protected work, supplied
  time/spend limits, and decisions reserved for the user. Preserve actual limits;
  if a new unattended run lacks a meaningful bound, propose one before launching
  rather than silently treating it as agreed. Review and verification consume
  the same task allowance, not an additional budget.
- **Stop and return:** stop at the agreed completion condition, exhausted limit,
  unresolved blocker, or evidence that the proposed change has no justified
  benefit. Return useful findings or a no-change outcome instead of manufacturing
  work. Identify deliverables, where evidence belongs, and any approval needed
  before publication or irreversible action.

Keep planned checks distinct from executed results. Do not fill empty headings,
create permanent planning files by default, or expand permissions to satisfy a
check. A brief is not permission to deploy, spend, publish, or change policy.

## Assign ownership, then dispatch if requested

Check existing owners and work before assigning mutations. Prefer one owner for
one bounded task. Parallelize only independent slices with clear interfaces;
name each slice's owned artifacts, inputs, outputs, dependency order, and who
integrates and verifies the whole. Shared-interface decisions precede dependent
edits; do not send two workers to change the same contract independently.
Separate worktrees alone do not resolve semantic overlap.

Limit active work to what can be integrated and checked within the allowance.
Give each worker the relevant brief, exact available sources and boundaries,
not the whole planning history. Workers return evidence, uncertainty, and decisions
needed, not merely a completion claim. If dispatch is unavailable or not requested,
return the brief and proposed ownership without pretending execution started.

When available and appropriate, use **review-loop** for the completed result's
review and repair, within the original task's remaining allowance. Use **handoff**
for a continuation prompt when work must stop or change owners; preserve consumed
limits, pending operations and actual verification. These skills are optional,
not installation prerequisites. Without them, return the result with evidence,
review limitations and a precise continuation point; do not claim an unperformed
review or introduce a new approval stage for ordinary delegated choices.
