# Trace 0001 — Seed and runtime bridge

**Trace type:** Project-origin and blocked-development trace  
**Repository anchor:** Initial commit d6103a7 and seed README at 35dd4e0  
**Recorded from:** Git history and repository artifacts  
**Status:** Historical trace; it does not prescribe current development

## Observer position

The project was at the point where an executable seed existed, but live
astronomical viability had not yet been established. The README at commit
35dd4e0 stated that the seed ran while viability remained unobserved, and
recorded a NumPy 2 / LibEphemeris hardware constraint.

This is a historical repository statement. It does not establish that the
same constraint remains active now.

## External anchor

The initial repository and its early README are the external evidence for
this trace:

- [Initial commit](https://github.com/incus-skills/calendar-engine/commit/d6103a7b1540b234b12d3a01c9c5983dd9ca0f63)
- [Initial CI/dependency commit](https://github.com/incus-skills/calendar-engine/commit/35dd4e02ff7f372d43919ebb096dccda8dfe5479)

## Observations

1. The initial README described an executable seed and explicitly said that
   viability had not yet been observed.
2. The same README identified NumPy 2 and LibEphemeris as a hardware-related
   block to live ephemeris incorporation.
3. The initial implementation embedded labels such as
   "Frozen Specification Realization" and returned operational categories
   from a narrow classification pipeline.
4. The historical source and its labels are artifacts of that development
   position. Their presence does not establish that they are a validated
   external contract.

## Distinctions preserved

- **Executable seed** is not the same as a verified astronomical runtime.
- **Runtime availability** is not the same as domain viability.
- **A source comment or embedded label** is not independent evidence of
  correctness or continuing authority.
- **A hardware constraint at one observer position in time** is not proof
  that the constraint remains active after the environment changes.

## Recorded development movement

Subsequent commits moved the runtime toward LibEphemeris, corrected the
observation path, added Julian Day verification and introduced tests for
datetime conversion. The relevant transitions are visible in the
[repository history](https://github.com/incus-skills/calendar-engine/commits/master/).

The initial README's "waiting for block resolution" position should therefore
not be repeated as the current operational state. The current state is
recorded separately in
[trace 0002](0002-astronomical-core-baseline.md).

## Assumptions and unresolved matters

The seed's embedded classification names and frozen labels were not
independently verified by this trace against astronomical or ecological
reality. They should be treated as historical implementation claims unless
separately re-established.

The original hardware constraint explains why development was interrupted;
it does not by itself determine what the next core-engine capability should
be.

## Re-entry

Re-enter through [the current astronomical core](../astronomical-core.md),
not through the initial seed's status statement. Use this trace when the
question concerns why the project began with a narrow executable seed and
what conditions constrained its early development.
