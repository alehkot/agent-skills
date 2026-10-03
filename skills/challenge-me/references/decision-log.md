# Decision log and conversation shapes

## Choose a location

Apply this order without making the user choose routine filesystem details:

1. Use the path the user supplied, following its existing format.
2. If the active workspace is a knowledge base, inspect its instructions and a
   few nearby notes for an established scratch or decision-log location. Use
   that convention, including dates, frontmatter, and links where appropriate.
3. Otherwise create a unique directory through the OS temporary-directory
   facility (for example, `mktemp -d`), and use `decisions.md` inside it.

An ordinary code repository defaults to temporary storage even if it has a
`docs/` directory. An unfamiliar vault with no clear scratch convention also
falls back to temporary storage. A plain `.obsidian` directory establishes a
vault, not the right note destination. Do not create a new vault hierarchy.

Keep temporary directories private to the current user when the environment
supports it. Store only task-relevant context; use pointers to sensitive source
material instead of unnecessary copies. Temporary storage is not durable or
encrypted by definition. Disclose the location without promising retention.

Respect an existing file: read it first, append or update the relevant section,
and do not replace unrelated content. Reuse the task's existing log on resume.
If the previous temporary file vanished, reconstruct only supported decisions
from available evidence and identify missing history.

## Working log

Use these fields as a compact scaffold, adapting the workspace's native format:

```markdown
# Decisions: <topic>

Updated: <timestamp with timezone>
Status: interviewing | clear | stopped | blocked
Objective and scope: <outcome, boundaries, intended audience>
Success: <observable criteria, or the unresolved question>

## Current understanding
<Short model of the problem and important terminology.>

## Decisions
- D1 — <choice>; confirmed by <user answer or explicit delegation>.
  Reason: <tradeoff>; evidence: <source/path or user statement>.
  Alternatives: <material rejected options and why>.
  Supersedes: <earlier decision ID, only when applicable>.

## Assumptions
- A1 — <unverified premise>; basis: <why>; status: <proposed or accepted>.

## Open questions
- Q1 — <material uncertainty>; depends on: <decision or missing evidence>.
- Deferred — <nonblocking branch, acceptance and condition for reopening>.

## Change log
- <timestamp> — <decision added, corrected, or superseded, and why>.
```

Record concise conclusions and reasons, not a transcript. Never upgrade a
recommendation to a confirmed decision because the user did not answer it.
If source facts contradict the user's account, preserve both with provenance
until the contradiction is resolved. Distinguish descriptions of current
behavior from decisions about desired behavior.

## Interview turn

Keep the visible turn focused; the file holds the accumulated detail. The first
turn announces the log path; later turns can simply report material updates.

```text
Question: <one difficult question, or up to three independent questions>
Recommendation: <answer and rationale; explicitly open to disagreement>
Decision log: <actual path and update, or conversation-only because ...>
Open questions: <the remaining material branch, without dumping the whole map>
```

## Closing brief

```text
Status: clear | stopped | blocked — <specific reason>
Decisions: <confirmed choices and consequential rationale>
Assumptions: <accepted nonblocking assumptions, or none>
Open questions: <remaining questions/deferrals; none only when supported>
Decision log: <actual path, or conversation-only with persistence limitation>
```

When stopped, do not append a new interview question or resume questioning on
the next automatic continuation. Resume only when the user requests it. When
clear, do not add filler questions merely to display skepticism.
