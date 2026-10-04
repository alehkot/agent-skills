# Agent Skills

Skills for challenging ideas, explaining unfamiliar subjects, handing off
execution, reviewing completed work, and designing or auditing AI-agent
evaluations. Each skill works alone in Codex, Claude, or another agent that
reads Agent Skills.

## Skills

| Skill | Use for |
| --- | --- |
| `challenge-me` | Persistent hard questions that expose assumptions and resolve ambiguities, with a working Markdown decision log. |
| `make-it-click` | Explanations of code, documents, systems, and concepts, with concrete examples, relevant evidence, and optional practice. |
| `handoff` | A paste-ready execution prompt for a fresh agent, preserving compacted context, pitfalls, verification, and the restart point. |
| `review-loop` | Review, repair, and re-review until no findings at the selected severity remain, within a bounded review budget. |
| `agent-evals` | Design or review AI-agent evaluations using an evidence-based rubric for purpose, coverage, references, discrimination, realism, measurement integrity, and proportionality. |

Use each skill independently. All required instructions and reference files are
included in its directory.

## Challenge an idea

```text
Use $challenge-me on this idea. Keep asking hard questions until I tell you to
stop or the overall picture is clear. Recommend answers, explain your reasoning,
and keep the decisions in a working Markdown log.

I want a personal resource finder, but I am not sure which problem it should solve.
```

The skill reads discoverable facts first, then asks one difficult question or up
to three independent questions per round. There is no interview round or time
limit. It follows implications and revisits contradictions instead of stopping
at the first plausible answer. A user stop produces a partial brief with open
questions; a clear result requires the material branches to be resolved.

An explicit output path wins. In a file-based knowledge base, the skill follows
an established scratch-note or decision-log convention. Otherwise it uses a
unique OS temporary directory, such as `/tmp`. Ordinary repositories do not get
permanent scratch documentation by default. If writes are unavailable, the
conversation holds the log and the persistence limitation is disclosed.

## Understand an unfamiliar subject

```text
Use $make-it-click to help me understand how requests pass through this service.
I know Python, but I am unfamiliar with queues. Trace a concrete request and
explain which reasons for the design are actually documented.
```

The skill also works outside code:

```text
Help me understand the argument in this report. Explain its assumptions with
an example, without a quiz.

Teach me the difference between probability and likelihood. Start with an
example, then offer a small application problem if it would help.
```

It gives a useful first explanation, adapts to what you already know, and uses
visuals when they clarify the subject. Historical reasons stay separate from
inferences. Practice starts when you request or accept it, and you can ask for
more detail, a direct answer, or a different pace at any time.

Learning requests can select the skill automatically. A quick factual lookup,
pure summary, edit, or critique alone does not need a teaching session. Outputs
stay in the conversation unless you request an artifact; if you also authorize
an action, such as explaining a change and then implementing it, the explanation
does not replace that action or make an exercise a prerequisite.

## Hand off execution

```text
Use $handoff to give me a prompt for another agent to continue this work with
fresh context. Include decisions, current state, pitfalls, failed approaches,
verification results, and exactly where to restart.
```

The prompt appears in chat. Add `Save it to /tmp/export-handoff.md` to request a
file too; a save request without a destination uses a unique temporary folder.
The next agent is assumed to have the same files and system, but no conversation
history. The prompt preserves essential decisions even if a temporary note is
lost, and directs the receiving agent to verify current state before acting.
It does not launch an agent or transfer a runtime's goal object.

## Review until the gate passes

```text
/goal Implement the requested export change until $review-loop passes.
```

Or use the skill directly in Claude or another runtime:

```text
Use $review-loop on the completed report. Fix confirmed medium-or-higher issues
and re-review the final result within 10 passes and 30 minutes.
```

Defaults are medium and above (P0/P1/P2), 10 started review passes, and 30 elapsed
minutes starting at the first review. Implementation before review is outside
that clock; reviews, repairs, checks, and waits are inside it. User overrides
can change the threshold and either bound, for example `high and above, at most
3 passes and 5 minutes`.

A fresh read-only reviewer examines the complete task result when available;
otherwise the executing agent performs a disclosed self-review. The main agent
checks findings, fixes confirmed issues, and reruns appropriate verification.
A passing result requires a clean review of the final state and current evidence
for the original acceptance criteria. Repeated unresolved issues still block.

Every reviewer attempt, including failures and the final clean pass, counts.
A fix after pass ten cannot pass without an authorized extra review. At either
limit the skill reports **not passed**, preserves the log and restart action,
and does no more review work without an explicit extension. A fresh session or
handoff does not reset the budget. The skill checks the clock and bounds tool
calls where supported; it is not a process supervisor or a global runtime hook.

## Design or review agent evaluations

Use design mode to turn a decision and task requirements into concrete cases,
expected outcomes, and checks:

```text
Use $agent-evals to design evaluations for our document-search assistant.
We want to know whether a new prompt improves answers grounded in the supplied
documents. Define cases, acceptable answers, graders, and a comparison with the
current prompt. Identify missing evidence before making a release claim.
```

Use review mode to examine an existing evaluation and the conclusions drawn from
its results:

```text
Use $agent-evals to review these test cases, graders, and saved agent results.
Check the expected answers, coverage, and conclusions against the requirements.
Report supported defects or a supported clean assessment. Explain the repairs
needed and which saved results would need regrading or new execution.
```

Both modes use the same seven-criterion rubric. Design produces an evaluation
specification with concrete inputs and expected outcomes; review produces findings
with source evidence, consequences, and precise repairs. Missing evidence remains
explicit, and critical defects cannot be hidden by favorable ratings elsewhere.

Evaluation quality, execution status, and candidate outcomes are reported
separately. A sound evaluation can expose a failing agent. Proposed checks are
not reported as executed, and rubric ratings are not pass rates or release approval.

## Installing

Preview the published bundle:

```bash
npx skills add https://github.com/alehkot/agent-skills --list
```

Install all skills for a runtime, or select one independently:

```bash
npx skills add https://github.com/alehkot/agent-skills -g -a codex --skill '*' -y
npx skills add https://github.com/alehkot/agent-skills -g -a claude-code --skill '*' -y
npx skills add https://github.com/alehkot/agent-skills -g -a codex --skill challenge-me
```

From the current local checkout, substitute `.` for the URL:

```bash
npx skills add . --list
npx skills add . -g -a codex --skill '*' -y
npx skills add . -g -a claude-code --skill '*' -y
```

Omit `-g` to install for the current project. The CLI uses `claude-code` as the
agent identifier for Claude Code. Refresh or restart your agent after installing.

Inspect or update installed skills:

```bash
npx skills list -g
npx skills update
```

## Check a checkout

The bundle checker requires Python 3.11 or newer and Git, with no Python packages
to install:

```bash
python3 scripts/validate_public.py
```

It checks the tracked file inventory, skill metadata, and bundled Markdown links.
A clean check confirms these structural properties; it does not measure an
agent's behavior or guarantee task outcomes.

## License

MIT. See [LICENSE](LICENSE).
