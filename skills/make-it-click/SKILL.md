---
name: make-it-click
description: >-
  Explain code, documents, systems, and concepts so the user can understand and
  reason about them. Use for teaching requests, conceptual walkthroughs, help me
  understand, teach me, or confusion that calls for a mental model and worked
  example. Adapt to what the user already knows, ground explanations in relevant
  evidence, and offer optional practice after explaining. A quick factual lookup,
  pure summary, edit, or critique alone is not a learning request.
---

# Make It Click

Help the person connect an idea to something they can reason through. Give a
useful explanation first, then adapt to what they ask or demonstrate. Keep the
conversation natural; the workflow below is guidance, not a response template.

## Find the learning need

Use the conversation to identify the subject, why the person wants to understand
it, and the knowledge they can already use. A developer reviewing a change and
a reader encountering the underlying concept need different starting points.
Skip familiar prerequisites and define unfamiliar terms where they first matter.

Inspect a referenced file, passage, or example before asking about information
it contains. Ask a focused question only when an ambiguity about the target,
purpose, or prerequisite would materially change the explanation. Otherwise
start from a reasonable interpretation and make it easy to correct. An intake
questionnaire or preliminary quiz is not required.

## Establish what the explanation rests on

Read the materials relevant to the actual question. For code, trace the behavior
and inspect relevant tests or history. For a document, separate its claims,
evidence, and assumptions. For a concept, use an accurate model and check facts
that are uncertain, consequential, or liable to have changed against authoritative
sources. Respect any restriction to supplied material and state the resulting
limits. Follow leads that can change the answer; an inventory of every available
tool or connected source is unnecessary.

Explain functional consequences separately from historical intent. Code can
show what happens; a design record may explain why someone chose it. A plausible
benefit is not proof of that choice. Attribute documented reasons, mark an
interpretation as such, and say when the reason remains unknown. When sources
conflict, show the disagreement and explain what the evidence does establish.

Attach source pointers where they support a material claim: relevant file
locations, document passages, or direct web links. Do not invent citations,
source access, test results, or certainty. If access is missing, explain the
supported part and name the gap; request the missing material when it is essential.

## Build a usable explanation

Lead with the answer or central relationship. Develop it with a concrete case,
worked example, or flow that exposes how it works. Tie each new detail to that
case instead of listing disconnected terms or walking through every source line.
Keep important terminology consistent and check the example's facts and results.

Give enough in the first response to address the question: usually the central
idea, a meaningful example, and the limitation needed to avoid a false conclusion.
Scale this to the request instead of enforcing a sentence count or an exhaustive
tour. Honor requests for brevity, a complete walkthrough, or one step at a time.
Use an analogy only when its correspondence helps; identify where it stops
matching the real mechanism.

Use a diagram, comparison, or other visual when relationships are easier to see
than describe. Match the medium to the subject and the host's capabilities. Build
up a complex picture in manageable parts when useful, without a fixed redraw
count. Explain the same essential relationships in text so unavailable rendering
tools do not block understanding. Any generated illustration must remain faithful
to the evidence and should not imply exactness it does not have.

For a subject with several dependent concepts, a persistent misconception, or
optional practice and feedback, read
[learning-patterns.md](references/learning-patterns.md) for approaches to choose
from. A simple explanation need not load that reference.

## Follow the learner's lead

Respond to confusion with a different example, representation, or prerequisite,
not a longer repetition of the same explanation. Follow requests to deepen,
redirect, or stop. In a one-shot setting, deliver a self-contained explanation
instead of withholding essential content for a reply that cannot arrive.

When applying the idea would help, offer a short exercise after explaining.
Practice is optional: begin when the user accepts or has already requested it.
Ask one application or prediction question at a time, then wait for their answer.
Do not reveal its solution in the same turn unless they request self-study
material with answers. Give specific feedback after checking the reasoning,
accept valid alternatives, and honor requests for the answer or to stop practicing.
Agreement, silence, and a fluent explanation do not establish mastery.

Before delivering, check the explanation and worked example against the evidence and their stated limits. Correct confirmed errors once, then recheck the complete explanation; report unresolved evidence gaps. A caller's explicit review budget takes precedence. Keep this check internal unless requested.

Keep outputs in the conversation unless the task calls for an artifact. Teaching
alone does not authorize source edits, state-changing demonstrations, or
publication. If the user also authorized an action, preserve that instruction
and continue under the host's execution rules after the explanation; do not make
practice a gate. Use only the private details needed to explain the subject.
