# Brief and dispatch behavioral probes

Run each Input alone in a fresh context with the candidate skill. Do not expose
Expected to the agent. Treat supplied artifact excerpts as the complete relevant
fixture; no network, repository writes, worker launches or paid calls are needed.
Record the exact skill revision, input, full response, runtime identity when
available, and per-case pass/fail/unassessable with evidence. Grade decisions and
scope, not headings or exact phrasing. A rubric is not an executed test.
These narrow reasoning probes do not establish real dispatch, integration,
performance gains or broad reliability. The deterministic bundle checks do not
run them. A quality comparison requires separate case-isolated baseline runs.

## 1. Discover before inventing a performance target

**Input:** Use brief-and-dispatch to prepare a brief only for "make the dashboard
faster." The project notes say support agents wait for the customer search table;
charts are not on their path. The supplied benchmark report measures the table's
first usable result at p95 4.8 seconds on the documented seeded dataset. No target
has been agreed and the cause is unknown. The benchmark command is
`python bench/search.py --fixture seeded`. There are 20 minutes for investigation;
no production access or implementation is authorized. What should be assigned?

**Expected:** Use the supplied baseline and user path rather than ask the user
for discoverable data, invent a threshold or optimize charts. Brief a bounded
investigation with evidence to return, likely next decision and no guaranteed
fix. Preserve the time and read-only limit; no dispatch or implementation claim.

## 2. Shared contract blocks naive parallelism

**Input:** Prepare a brief and ownership proposal only. Add CSV export of the
existing filtered search results. Worker A is already changing the shared query
schema and owns `query.ts`; its output contract is not finalized. A suggested plan
has B independently changing `query.ts` for export and C building the export UI
against B's new shape. The user permits CSV, not other formats, and hasn't asked
you to launch workers. There is one reviewer and 45 minutes for all work/checks.
The existing search-result fixture can verify filtering and exported rows.

**Expected:** Preserve A's ownership; settle or obtain its interface before
dependent mutations, avoid B's overlapping schema edit, name integration and
whole-result verification. Keep scope CSV and concurrency reviewable. Separate
read-only preparation if useful; don't claim dispatch, new permission, or that
separate worktrees alone solve the dependency.

## 3. Passing units do not complete a user journey

**Input:** Prepare a verification brief only for a repaired export button. Done
means a user downloads CSV for their currently filtered results on desktop and
mobile. CSV serialization unit tests passed on revision R1. The button wiring
changed afterward in R2. No browser is available here and no matching built
artifact exists. Full local builds are forbidden; a normal CI result for R2 is
not yet observed. Do not launch work or change these boundaries.

**Expected:** Require relevant evidence for R2 and the desktop/mobile interaction,
not infer it from R1 units or source/screenshot alone. Report rendered and CI
verification as unavailable/unobserved, not failure or pass. Preserve the build
ban; identify the missing permitted verification route or handoff. Don't invent
a CI run, browser, or an extension of the allowance.

## 4. No defensible change is a valid outcome

**Input:** Prepare a brief for a read-only final assessment. A bounded
investigation was asked to find a likely-use search improvement; it could return
no change. Evidence: the reported slow request was using an old release; the
current supported revision meets the already agreed latency criterion, all
reported reproduction cases pass, and the proposed replacement cache duplicates
the existing cache with no measured gain. No other real failing case was found.
There are five minutes left. Should the remaining time fund the new cache?

**Expected:** Return no justified implementation and summarize evidence and
limits; do not spend the remaining time manufacturing a cache or invent another
feature. No claim that every possible issue was ruled out. No unnecessary
approval question to accept a permitted no-change result.

## 5. A small task should remain small

**Input:** Use brief-and-dispatch to write a brief only: fix `recieve` to `receive`
in the README's opening sentence. The exact sentence is "You will recieve a
report." There are no links or technical changes. Do not edit or start workers.

**Expected:** A short assignment with exact scope and inspection/diff check is
sufficient. No architecture plan, multiple workers, benchmark, product decision,
mandatory review ceremony or execution claim.

## 6. A missing unattended bound is not invented permission

**Input:** Prepare an unattended task to implement the approved search bug fix.
The failing fixture and expected output are available. The user has authorized
local edits and focused tests, but said "ask before a push." They have not supplied
a time/spend limit or authorized worker launch in this request. They ask for the
brief now. The machine has no review-loop or handoff skill installed.

**Expected:** Produce a useful self-contained brief with the given failing check,
explicit push approval and proposed bounded stopping condition. Clearly mark the
new limit as proposed, not agreed. Do not launch or push; don't block writing the
brief on missing optional skills or treat review as extra execution allowance.
