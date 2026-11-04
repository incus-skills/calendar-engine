# Calendar Engine

The Calendar Engine is a developing computational ecology for establishing
observer position within recurring astronomical and environmental cycles.
The repository contains executable behaviour, tests, development traces and
multiple routes into that material.

This README is a **landing surface**, not a complete account of the project
and not a specification. Use the ingress routes below to enter from the
position relevant to your work.

## Ingress

| Entry position | Enter through |
|---|---|
| Operational | [Current operational state](docs/astronomical-core.md#current-capability) and [live demonstration](demo.py) |
| Provenance | [Trace collection](docs/traces/README.md) |
| Methodology | [Astronomical core and its conventions](docs/astronomical-core.md) |
| Reconstruction | [Reconstruct the executable baseline](docs/astronomical-core.md#reconstructing-the-baseline) |
| Continuation | [Latest development position](docs/traces/0002-astronomical-core-baseline.md#re-entry-position) |

These are parallel ingress points, not a prescribed reading order. An
observer may move between them as distinctions or questions become relevant.
The [ingress map](docs/ingress.md) shows how these entry positions relate to
the repository's traces and artifacts.

## Current operational state

The current core acquires Sun and Moon states, retains their positional and
motion components and calculation context, optionally calculates a separate
topocentric state for an explicit observer, and compares observations across
epochs.

See the [astronomical core record](docs/astronomical-core.md) for the precise
behaviour, conventions, limitations and reconstruction procedure.

## Trace discipline

Documentation preserves traces and their relationships. It does not replace
the source code, tests, workflow or Git history, and it should not collapse
them into a single authoritative narrative.

Claims in trace records identify their provenance and status. Assumptions,
decisions, rejected alternatives and unresolved questions are retained where
they materially affect reconstruction. A recorded conclusion is evidence of
what was concluded, not automatically proof that the conclusion is correct.

## Run

~~~sh
python demo.py
pytest -v
~~~

The test suite includes deterministic tests of engine behaviour and integration
tests that exercise the installed LibEphemeris dependency.
