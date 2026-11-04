# Trace collection

This directory preserves development traces that help later observers
reconstruct how the current project state became possible.

It is a collection, not a single authoritative narrative and not a
specification. A trace is a positioned record: it identifies the observer
position, external anchor, observations, distinctions, decisions, assumptions,
evidence, unresolved questions and resulting project-state change.

## Collection

| Trace | Preserved movement |
|---|---|
| [0001 — Seed and runtime bridge](0001-seed-and-runtime-bridge.md) | Initial executable seed, hardware constraint and transition toward a live ephemeris runtime |
| [0002 — Astronomical core baseline](0002-astronomical-core-baseline.md) | Baseline development, evidence, conventions, branch state and next re-entry boundary |

New traces should be added when a material observer-position change, decision,
implementation increment, verification result or unresolved tension would
otherwise be difficult to reconstruct.

## Trace discipline

Preserve different kinds of statements as different kinds of traces:

- **Observation:** what was present in a repository state, test result or
  external system at a specified point.
- **Claim:** what an observer concluded from those observations.
- **Assumption:** a convention adopted to make an operation possible.
- **Decision:** a choice made, including its authority and scope.
- **Rejected alternative:** a considered path and the reason it was not taken.
- **Unresolved question:** a distinction not yet settled.
- **Re-entry position:** the point from which subsequent work can proceed.

Do not omit assumptions merely because they are assumptions. Their status
must remain visible. Do not omit conclusions merely because they are
conclusions. Preserve their provenance and do not present them as independent
observations.

A trace may contain chronology, but chronology alone is not a trace. Preserve
the distinctions and relationships needed to understand why the project moved
from one state to another.

The collection does not itself declare a recurrent pattern. Any candidate
locus or pattern inferred from multiple traces must remain distinguishable
from the source traces and retain links to them.
