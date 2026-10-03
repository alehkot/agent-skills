# Experiments and coverage maintenance

## Freeze before looking at candidate results

Record task families and splits, raw inputs and policies, agent-visible versus
evaluator-only evidence, instructions and references, environment/tools/state,
model/provider versions, decoding/budgets, grader criteria, expected run IDs,
repeats, ordering/seeds when supported, and stopping rules.

Separate the primary comparison from diagnostic ablations. Vary the intended
factor while holding relevant evidence, tools and budgets constant. If comparing
whole products with different budgets, state that estimand and report the tradeoff
instead of claiming an isolated component effect. Same seeds do not guarantee
identical randomness across providers.

For skill comparisons, isolate the baseline from installed skills, ambient
instructions, memory, repository reads and prior transcripts. Inline any task
artifacts unavailable through tools for both arms. Reset independent trials, while
preserving state deliberately within a persistent-session test.

## Plan counts and failures

Use the planned inventory, not surviving result directories, to determine
completeness. Preserve all attempts and classify separately:

- Agent task failure, including harmful intermediate effects.
- Invalid model output or exhausted agent budget.
- Tool/provider/harness infrastructure error.
- Judge execution error or genuinely unassessable assertion.
- Planned but missing execution.

A failed tool call can be an intentional resilience stimulus, not a harness error.
A malformed action produced by the agent is not automatically infrastructure.
Name the layer and the evidence. Declare how these outcomes enter semantic and
operational metrics; report both without silent deletion or relabeling.

Specify which infrastructure failures can retry, the cap, and whether the final
metric reflects first attempt or the deployed retry policy. Do not retry semantic
failures until success and overwrite earlier evidence. A timeout records observed
duration and incomplete status, not a fabricated completion time. Latency-to-success
is censored only when that interpretation fits the termination mechanism; otherwise
report the timeout/abort separately.

Bound spending before requests, including controls, judges, retries and unknown
charges. Record actual usage when available; retain conservative reservations for
ambiguous billed calls. Stop rather than silently changing models or buying
unapproved capacity.

## Report metrics for the actual decision

For outcomes A=PFF, B=PPP, C=FPF, D=FFP:

- Six of twelve attempts pass: empirical per-attempt success = 50%.
- Every task passes at least once: empirical any-of-three = 4/4.
- Only B passes every time: empirical all-of-three = 1/4.

These are different questions. None is universally "true production reliability."
An any-of-k score presumes a way to select or verify a successful attempt; retries
with side effects may not be safe. An all-of-k score concerns consistency over k
attempts. Keep the task population, k, trial independence assumptions and aggregation
explicit; do not estimate all-of-k by casually raising a pooled mean to a power.

Report per-family and relevant user/security slices, critical violations, valid
execution coverage, paired deltas and within-task variation. Repeats are not extra
independent tasks. Pooling across tasks mixes difficulty with stochastic variation.

Use uncertainty methods only with defensible sampling/dependence assumptions.
A tiny synthetic pilot can provide exact counts, failure examples and tentative
paired observations without a generalization interval. More bootstrap resamples
do not create more independent task families; a binomial interval does not repair
unrepresentative or dependent data. Predeclare fixed or valid sequential stopping;
do not repeatedly peek and stop when a preferred significance claim appears.

## Gates and continued learning

Separate coverage readiness, critical policy invariants, task usefulness,
operational requirements and release approval. State decision-specific thresholds,
their basis and unresolved risk choices. Do not average away a breached critical
boundary. Report attacks attempted/exposed, effects observed and clean utility
separately; finite clean results do not prove absence of exploitable behavior.

Keep originals when a defective rubric is corrected. Version the correction and
identify what needs regrading versus fresh generation. Failure-only rechecks are
diagnostic, not an unbiased judge comparison.

Retain exposed cases as regression checks. Add fresh assessment families and new
trace-derived mechanisms when models, tools, policies, users or environments change.
Before increasing run volume, identify whether the weakest link is missing cases,
an invalid oracle, poor environment fidelity, incomplete execution or actual agent
quality. More runs fix sampling uncertainty; they do not fix the other defects.
