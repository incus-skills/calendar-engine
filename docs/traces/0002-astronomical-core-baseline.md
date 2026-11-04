# Trace 0002 — Astronomical core baseline

**Trace type:** Development increment and verified state transition  
**Recorded:** 2026-11-04  
**Primary repository branch:** master  
**Status:** Baseline established; subsequent development proceeds through feature branches and pull requests

## Observer position

The project had accumulated enough observation of the earlier executable
implementation to identify a bounded core-engine increment. Further
investigation of every astronomical or ecological relationship was not
required before acting.

The governing distinction was between investigating the existing executable
and making a demonstrable development step toward the Calendar Engine's
intended operation.

## External anchor

- [Baseline commit 0eef181](https://github.com/incus-skills/calendar-engine/commit/0eef1816ae55c5d0c33cb14b4dc5fa631a5f4394)
- [Baseline CI run 41822832916](https://github.com/incus-skills/calendar-engine/actions/runs/41822832916)
- [Default-branch CI cleanup commit cca47c8](https://github.com/incus-skills/calendar-engine/commit/cca47c8790d84715d61e2d17566285b07990cd9b)
- [CI run after workflow cleanup 41823430207](https://github.com/incus-skills/calendar-engine/actions/runs/41823430207)

## Observations

1. Before the baseline increment, the executable observation retained solar
   and lunar longitude and a derived longitude difference, but discarded the
   other position and motion values returned by LibEphemeris.
2. Observer coordinates were stored in the observation record but were not
   passed into the astronomical calculations.
3. The baseline replaced the former classification-and-projection pipeline
   as the primary active engine path with an astronomical observation core.
4. The new observation retains six position/motion values for each body,
   records calculation context and keeps geocentric and optional topocentric
   states separate.
5. The comparison operation retains both source observations and derives
   principal-arc displacement and endpoint rate change.
6. The baseline commit was tested by GitHub Actions under Python 3.12 and
   Python 3.13. Both jobs completed successfully; the CI log reports
   16 passing tests per job, including live LibEphemeris integration tests.
7. The subsequent workflow change restricted push and pull-request triggers
   to the default master branch. Both Python jobs passed again.
8. The user confirmed removal of the obsolete main branch. The observed
   repository state after that removal contained only master.

## Distinctions preserved

- **Geocentric reference** and **observer-conditioned topocentric result**
  remain separate representations.
- **Astronomical state** and **calendar/operational interpretation** are
  separate concerns.
- **Instantaneous motion** and **change inferred from two snapshots** are
  distinct. A principal-arc comparison cannot reveal unobserved complete
  revolutions over arbitrary intervals.
- **Calculation convention** and **validated precision profile** are distinct.
- **Historical specification labels** and **current executable behaviour**
  are not interchangeable.

## Assumptions and conventions now visible

- Naive datetimes are interpreted as UTC.
- UTC is supplied as a proxy for UT in the LibEphemeris calculation path;
  no DUT1 correction is applied.
- J2000 ecliptic coordinates are used for the retained body states.
- When an observer altitude is omitted, zero metres is passed to the
  topocentric calculation, while the observer record retains altitude_m=None.
- Comparison uses the principal signed angular difference. It is not a
  complete trajectory reconstruction.

These are current implementation conventions. Their suitability for every
future use has not been established.

## Rejected or deferred alternatives

- The initial increment did not attempt a complete Calendar–Almanac model.
- It did not encode cultural, agricultural or tidal meaning into astronomical
  states.
- It did not treat topocentric ecliptic coordinates as proof of local
  visibility.
- It did not attempt to resolve all recurrence and event relationships before
  establishing a state-and-motion foundation.

These boundaries kept the increment demonstrable without declaring the
remaining domain settled.

## Unresolved questions

- How should continuous trajectories and event crossings be represented?
- Which recurrence relationships are needed across solar, lunar, orbital,
  tidal and other cycles?
- Which local observability relationships require horizontal coordinates,
  horizon models or atmospheric conditions?
- How should Almanac observations and predictions relate to astronomical
  calculations without being conflated with them?
- What precision and uncertainty profiles are required by different uses?

These are open boundaries, not an exhaustive list of eventual requirements.

## Re-entry position

The current observer enters from a project with a verified astronomical
state-and-motion baseline. A useful next bounded increment is event and cycle
representation: derive actual event times and intervals from retained states
and motion, while preserving source states and their calculation context.

That is a proposed next movement, not a claim that its detailed semantics or
architecture have already been settled.

For current behaviour, enter through
[the astronomical core record](../astronomical-core.md). For alternative
entry positions, use the [ingress map](../ingress.md).
