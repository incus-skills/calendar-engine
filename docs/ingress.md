# Ingress surfaces

Ingress is access to the project's preserved traces. The entry points below
are parallel ways into the same developing ecology. They are not stages and
do not impose a reading sequence.

## Entry positions

| Ingress | Observer purpose | Initial access | Further traversal |
|---|---|---|---|
| **Operational** | Establish what the executable project currently does | [Core capability](astronomical-core.md#current-capability) | [Demo](../demo.py), [workflow](../.github/workflows/test.yml), [tests](../test_ephemeris.py) |
| **Provenance** | Establish how the present state came about | [Trace collection](traces/README.md) | [Origin trace](traces/0001-seed-and-runtime-bridge.md), [baseline trace](traces/0002-astronomical-core-baseline.md), [Git history](https://github.com/incus-skills/calendar-engine/commits/master/) |
| **Methodology** | Inspect distinctions, conventions and limits in the current astronomical model | [Astronomical core](astronomical-core.md) | [Observation implementation](../calendar_engine.py), [comparison tests](../test_calendar_engine_comparison.py) |
| **Reconstruction** | Re-establish an executable observation and its evidence | [Reconstruction procedure](astronomical-core.md#reconstructing-the-baseline) | [Dependencies](../pyproject.toml), [requirements](../requirements.txt), [tests](../test_calendar_engine_observe.py), [CI workflow](../.github/workflows/test.yml) |
| **Continuation** | Enter from the latest recorded development position | [Latest development trace](traces/0002-astronomical-core-baseline.md#re-entry-position) | [Current core](astronomical-core.md), [open boundaries](astronomical-core.md#not-yet-represented) |

An ingress is not a claim that its initial link contains everything required.
It identifies a useful observer position and exposes paths into the relevant
traces. A continuation route should be updated when the project's operative
position changes.

## Relationship map

The Mermaid source below is the maintained representation of this ingress
relationship. The rendered diagram is a view of the source; the labelled
nodes and edges are the semantic record.

~~~mermaid
flowchart LR
    subgraph IN[Parallel ingress positions]
        OP[Operational]
        PR[Provenance]
        ME[Methodology]
        RE[Reconstruction]
        CO[Continuation]
    end

    subgraph TR[Preserved traces and artifacts]
        ST[Source and runtime]
        TE[Tests and verification]
        HI[Git history]
        DT[Development traces]
        RC[Core conventions and boundaries]
        CI[CI workflow and dependencies]
    end

    OP -->|current behaviour| ST
    OP -->|execution evidence| TE
    OP -->|validation path| CI

    PR -->|sequence and changes| HI
    PR -->|observer positions| DT

    ME -->|definitions and limits| RC
    ME -->|implemented relations| ST
    ME -->|behavioural evidence| TE

    RE -->|reproduce runtime| ST
    RE -->|reproduce environment| CI
    RE -->|check outcomes| TE

    CO -->|current position| DT
    CO -->|current capability| RC
    CO -->|next open boundary| DT
~~~

## Navigation discipline

- Follow links according to the question being reconstructed, not the order
  in which they appear here.
- Move between claims and their supporting source, tests, history or trace.
- Preserve contradictions and unresolved questions as visible distinctions.
  Do not silently harmonize them to make the map look complete.
- A changed project state requires a new trace or an explicit update to an
  existing trace, together with a new continuation position.
