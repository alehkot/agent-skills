# Agent Skills

Skills for challenging ideas, handing off execution, reviewing completed
work, and designing or auditing AI-agent evaluations. Each skill works alone in
Codex, Claude, or another agent that reads Agent Skills.

## Skills

| Skill | Use for |
| --- | --- |
| `challenge-me` | Persistent hard questions that expose assumptions and resolve ambiguities, with a working Markdown decision log. |
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
