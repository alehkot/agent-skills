# Select coverage from obligations

Start with the user's decision and actual system. Join requirements, architecture
and observed failures before counting cases. In review mode derive this map before
accepting the suite's own checklist; otherwise an omitted requirement can disappear
from both the tests and their audit.

For each material obligation record its source, affected user/asset, failure
mechanism, concrete case, deciding evidence and remaining gap. Include cases that
should succeed. Prioritize consequence, then exposure and uncertainty; an unknown
production frequency does not cancel an explicit requirement.

## Applicability menu

These are agent behaviors underneath the rubric's coverage criterion, not extra
mandatory scores or infrastructure. For a narrow task consider routine exclusions
internally; report exclusions that materially limit the claim. Unsupported or
unmentioned capabilities are not automatically absent.

| Dimension | Select when | Discriminating case and evidence |
| --- | --- | --- |
| Correctness and grounding | answers make factual or numerical claims | current source versus stale text; check facts, calculation and citation support |
| Completion and artifact quality | a result, artifact or effect is requested | plausible "done" with a required item missing; inspect output, receipt and relevant state |
| Instructions and control | scope, corrections, cancellation or approvals matter | correction before commit; subsequent actions must respect the new target and remaining authorization |
| Tools and workflows | tools or dependent actions exist | correct syntax aimed at the wrong object; check preconditions, parameters and effects, accepting equivalent valid routes |
| Ordinary robustness | noisy, empty, malformed or unfamiliar inputs occur | boundary or equivalent paraphrase; check preserved meaning, appropriate error and bounded fallback |
| Reliability and recovery | retries, stochastic behavior or persistent state matter | timeout before/after commit and restart; ledger distinguishes one effect from duplicates and unsupported status claims |
| Uncertainty and honesty | evidence can be absent or contradictory | answerable/unanswerable source pair; distinguish grounded qualification from invented fact or false completion |
| Interaction quality | clarification or handoff is supported | consequential ambiguity versus a safe stated default; check necessary questions, retained context and useful handoff |
| Efficiency | latency, cost, resources or user effort affect the decision | needless tool loop; include failed/timeout attempts in the declared metric rather than rewarding cheap failure |
| Safety and abuse/security | harmful content, assets, untrusted input or authority create exposure | legitimate request and unauthorized variant; inspect applicable policy, attempts, effects and clean utility |
| Privacy and data lifecycle | sensitive data or retained preferences exist | deleted/expired information reappears; inspect actual later context and authorized sinks under the real retention policy |
| Fairness | supported populations could receive different quality | matched tasks by relevant supported attribute; compare error/refusal/helpfulness while accounting for permissions and task difficulty |
| Accessibility and localization | languages, modalities or accommodations are supported | equivalent task in a supported language or assistive format; inspect meaning, units and rendered accessibility as applicable |
| Personalization | explicit profiles intentionally change responses | same entitlement, different supported preferences; preserve allowed facts/actions and test stale/conflicting preferences if state exists |
| Observability | consequential effects need investigation | disputed completion; authorized evidence links policy, inputs and receipts without unnecessary private data |

Do not infer sensitive traits, invent locales or impose universal parity/latency
thresholds. Distinguish adaptation to an explicit preference from permission to
access information. A safety refusal can be correct on one obligation and still
fail the legitimate user job; report both.

## Choose mechanisms rather than prompt volume

1. Make a normal and violating case for each consequential invariant.
2. Add relevant boundary values, state transitions and source conflicts.
3. Use actual incidents to discover missing mechanisms; preserve provenance and
   redact sensitive details without removing the cause.
4. Select ordinary combinations economically, then add known causal sequences.
   Retrieval plus export happy paths do not test permission revocation between
   retrieval and export. Pairwise coverage does not establish a known three-factor
   interaction involving poisoned memory, lost provenance and privileged export.
5. Group paraphrases into families. They test wording sensitivity, not independent
   mechanisms. Keep related source families together when separating development
   and assessment data.

For delegated agents include the actual identity, authority, evidence and error
contract at each handoff. For memory include cache/session persistence and reset
boundaries. For tool work include failure before and after effects, retries and
concurrency where the architecture exposes them. Omit absent components.

## Coverage is a bounded argument

Use rows such as:

| Obligation / source | Case and oracle | Stage / gap |
| --- | --- | --- |
| Only current approved destination; export contract | approval then changed destination; compare authorized parameters, proposed call and delivery ledger | proposed; gateway fixture not connected |
| One notification effect; delivery contract | commit then lost acknowledgement; authoritative operation receipts | verifier-checked; candidate run pending |
| Supported Spanish help; product contract | same source question in English/Spanish; source-grounded meaning check | candidate-executed; outcomes retained by language |

Keep specified, runnable, verifier-checked and executed inventories separate.
Define the denominator behind any coverage percentage. A list of eighty topics
does not establish eighty runnable cases or observed outcomes. Zero observed
security failures cannot prove universal security.

Stop adding cases when they bring no new decision-relevant behavior, boundary,
interaction or evidence. Name residual uncertainty. Add instrumentation only when
the required observation is otherwise unavailable; more runs cannot repair a
wrong oracle or an invisible state transition.
