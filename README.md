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
to three independent questions per round. There is no default interview round or
time limit; explicit user limits are honored and retained on resume. It follows
implications and revisits contradictions instead of stopping at the first
plausible answer. A user stop or an exhausted allowance with unresolved branches
produces a partial brief with open questions; a clear result requires the material
branches to be resolved.

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

Attempts with unknown outcomes and operations still running are preserved as
such, with known request/job references and recovery routes. The restart checks
existing effects before repeating an operation; a timeout is not proof of failure.
This is continuation guidance, not an exactly-once execution mechanism.

## Review until the gate passes

Use the same gate for code, documents, slide decks, analyses, knowledge bases,
and other knowledge work. Choose checks that fit the artifact and task.

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

Code, configuration, schema, and dependency reviews include
[blast-radius checks](skills/review-loop/references/blast-radius.md): trace
relevant downstream effects, identify the assumptions that determine safety,
and check them against source or execution evidence. The reviewer remains
read-only; the main agent runs probes that require writes or side effects under
the task's existing authorization. Confirmed defects, cleared risks, and missing
evidence stay distinct. These checks use the same scope, severity gate, and budget;
they add no pstack dependency or mandatory full-app run.

For checks with setup or several steps, an optional
[verification recipe](skills/review-loop/references/verification-recipe.md)
ties the actual artifact to a user path or inspection surface, preconditions,
expected and observed outcomes, side effects, and evidence retained after cleanup.
Each check records PASS, FAIL, or BLOCKED separately from the overall review
result. A plan, an
old run, or a successful exit code alone cannot establish that a changed result
works. Documents, slides, and other knowledge work can use direct inspection,
source checks, and rendered-output checks where relevant. The recipe includes
memo and slide-deck examples; simple checks need no separate recipe file.

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
python3 scripts/test_validate_public.py
```

It checks the tracked file inventory, skill metadata, and bundled inline Markdown
links, including quoted link titles and ATX-heading fragments. Local destinations
must be tracked bundle files; links within a skill must stay in that standalone
skill. Fenced examples and same-line code spans are not treated as live links.
The checker handles the bundle's Markdown conventions, not all CommonMark syntax
(such as reference-style links, HTML links, or Setext headings). The regression
tests run with the same standard-library-only requirements.
It also requires each skill's bundled `LICENSE` to match the repository license
exactly, so the copyright and permission notice survives a standalone install.

For `SKILL.md` frontmatter, the checker recognizes the entire header using a
small repository convention: exactly one unquoted `name` and `description` field,
with `name: <directory-name>`. Descriptions use either `>-` followed by a single
paragraph of nonblank lines indented exactly two spaces, or a single-line
JSON-compatible double-quoted string. Folded lines join with one space; decoded
descriptions must be nonblank, 1–1024 characters, and contain no controls or
Unicode line/paragraph separators. Field order, blank lines, and whole-line
column-zero comments outside the folded paragraph may vary. Comments within a folded
paragraph are literal description text. Unsupported YAML forms (including plain
or single-quoted descriptions, other block styles, and quoted keys) are rejected;
this is not a general YAML parser. Extend the checker and tests before changing
that convention. All published skill descriptions use the folded form.

For `agents/openai.yaml`, this bundle uses a deliberately small format: one
`interface:` mapping containing exactly `display_name`, `short_description`, and
`default_prompt`, each indented two spaces with a nonblank, single-line
JSON-compatible double-quoted string. Blank lines, whole-line comments, and any
field order are allowed. The decoded default prompt must name its own `$skill-name`
as a complete token; a mention in another field or a longer skill name does not
count. Duplicate fields, invalid escapes, control characters, and raw Unicode
line/paragraph separators are rejected. Blank/comment indentation uses spaces or
tabs; other Unicode whitespace is not silently discarded.
This is a repository convention, not the full Codex/YAML schema. Extend the
checker and its tests before adding other metadata fields or YAML forms.
A clean check confirms these structural properties; it does not measure an
agent's behavior or guarantee task outcomes.

Targeted synthetic [handoff recovery cases](evals/handoff-recovery.md) cover
uncertain outcomes, running work, supported retries, and ordinary continuation.
They are manual behavioral fixtures with expected observations, not tests run by
the bundle checker. Use isolated fresh sessions and retain the generated prompts
when evaluating them; passing structural checks alone does not pass these cases.

[Challenge-me interview-limit cases](evals/challenge-me-limits.md) cover explicit
round/time limits and continuation controls. They are also manual behavioral
fixtures, not automated checks of agent behavior.

[Review-loop blast-radius cases](evals/review-loop-blast-radius.md) cover downstream
contracts, evidence limits, read-only reviewers, clean changes, and existing
review-budget boundaries. These are manual behavioral fixtures too.

[Agent-evals model replay cases](evals/agent-evals-model-replay.md) distinguish
model counterexamples, observed implementation failures, inconclusive replay and
bounded or unchecked properties, with terminal-state and stateless controls.
They are manual behavioral probes, not execution by the bundle validator.

## License

MIT. See [LICENSE](LICENSE). Each skill includes an unchanged copy of this
license for standalone distribution. Keep all five copies synchronized when
updating the repository license.
