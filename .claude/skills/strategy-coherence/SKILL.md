---
name: strategy-coherence
description: Audits a portfolio of strategic intents and active initiatives for Rumelt-style coherence failures — pairs of bets that pull in opposite directions on resources, capabilities, or market posture. Use when running /audit-portfolio-coherence or when reviewing a proposed new initiative against the existing portfolio.
license: MIT
---

# strategy-coherence

Rumelt's third pillar of good strategy is **coherent action** — multiple actions that reinforce each other to address the diagnosed challenge. Incoherence is the second-most-named strategy-execution failure mode after "list of goals." This skill provides the rule library that detects it.

## When to use this skill

- `/audit-portfolio-coherence` calls this skill to apply rules pairwise across active artifacts
- When a new initiative is proposed, audit it against every existing active artifact
- During quarterly `/strategy-refresh`, check the candidate 3–5 coherent actions for internal contradiction

## The three axes of coherence

Two bets are *coherent* if they reinforce each other on all three axes, *adjacent* if neutral, *incoherent* if they contradict.

### Axis 1: Resources
What does the bet commit? What does it foreclose? Most common failure: two bets claiming the same scarce resource (eng time, capital, attention, brand bandwidth) without either acknowledging the trade-off.

Detect: scan frontmatter `coherent_actions:` and body for resource claims. Flag pairs where:
- Both claim the same scarce resource as primary input
- One *cuts* a resource the other *invests in*
- Both implicitly assume more team capacity than realistic

### Axis 2: Capabilities
What organizational muscle does the bet build? What does it atrophy by neglect? Most common failure: building two opposing muscles simultaneously (self-serve onboarding AND high-touch implementation services on the same segment).

Flag pairs where:
- One builds a muscle that requires atrophying what the other needs
- The implied operating model is fundamentally different
- One builds for scale, the other for depth, on the same customer

### Axis 3: Market posture
What identity does the bet signal? Most common failure: trying to be innovator AND price leader AND integrator simultaneously.

Flag pairs where:
- One signals premium, the other signals price-leader to the same segment
- One signals open ecosystem, the other signals lock-in
- One signals horizontal platform, the other signals vertical specialization

## Classification rules

```
coherent     = reinforces on ≥2 axes, neutral on the third
adjacent     = neutral on all axes (orthogonal bets; not a problem)
drifting     = contradicts on 1 axis, neutral on others
incoherent   = contradicts on ≥2 axes
```

Action threshold: `incoherent` requires immediate remediation; `drifting` requires a decision (often: sequence them). `coherent` and `adjacent` are fine.

## Don't auto-conclude on weak evidence

If an artifact doesn't make its claims on an axis explicit, mark that axis as `unknown` rather than guessing. An audit firing on guesses is worse than no audit. The output should say "Cannot audit on axis X — Artifact A doesn't declare its market posture explicitly" and recommend the author add it.

## Caveat

Strategy is judgment. This rule library catches mechanical contradictions; it does not catch deep ones that require domain knowledge. Use as a screening tool, not a verdict. The audit report should end with "leadership decision required" rather than auto-resolving.
