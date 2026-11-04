# Astronomical core

This record describes the current executable core. It is an entry surface into
the implementation and its evidence, not a replacement for either.

## Current capability

~~~python
engine = CalendarEngine(observer=optional_observer)
observation = engine.observe(datetime_value)
comparison = engine.compare(earlier, later, origin="geocentric")
~~~

The core currently:

- Acquires geocentric Sun and Moon states for a supplied epoch.
- Retains longitude, latitude, distance, longitude speed, latitude speed and
  distance speed for each body.
- Calculates in a fixed J2000 ecliptic frame.
- Optionally calculates separate topocentric states for an explicit observer.
- Retains a directed Sun-to-Moon ecliptic-longitude separation and its
  instantaneous relative rate for each available origin.
- Compares two observations while retaining both source observations and
  deriving principal angular displacement, principal-arc mean rate and
  endpoint rate change.

The executable entry points are
[calendar_engine.py](../calendar_engine.py), [demo.py](../demo.py) and
[main.py](../main.py).

## Observation and provenance

An AstronomicalObservation retains:

- UTC-normalized timestamp and Julian day supplied to the UT calculation API;
- CalculationContext with library/version, input time scale, UT proxy
  convention, DUT1 correction status and reference frame;
- optional ObserverPosition;
- separate geocentric and topocentric body-state mappings;
- the Moon–Sun ecliptic-longitude relationship for each available origin.

A BodyState retains all six values returned by calc_ut():

| Value | Unit |
|---|---|
| Ecliptic longitude | degrees |
| Ecliptic latitude | degrees |
| Distance | astronomical units |
| Longitude speed | degrees/day |
| Latitude speed | degrees/day |
| Distance speed | AU/day |

The requested and returned calculation flags are retained with each state's
coordinate-frame record. The source calculation path is in
[calendar_engine.py](../calendar_engine.py).

## Time conventions

- Aware datetimes are normalized to UTC.
- Naive datetimes are interpreted as UTC.
- The UTC components are converted to a Julian day and passed to the
  LibEphemeris UT calculation interface.
- UTC is used as a proxy for UT; no DUT1 correction is applied.
- The observation records that approximation in its calculation context.

These are current implementation conventions. Their suitability for every
future Calendar precision profile has not been established.

## Observer conventions

An observer is optional. When supplied, its latitude and longitude are used
for a separate topocentric calculation; the geocentric calculation is retained
as a common reference.

Altitude is accepted in metres. When altitude is omitted, the current code
passes 0 m to the topocentric calculation while preserving altitude_m=None
in the observer record. This means sea level is an explicit calculation
assumption, not an observed altitude.

Topocentric ecliptic coordinates do not constitute horizontal altitude and
azimuth, horizon crossing, atmospheric visibility or practical observability.
Those remain outside the current core.

## Relationships and comparison

The retained Moon–Sun relationship is a directed difference in ecliptic
longitude. Its rate is the Moon's longitudinal speed minus the Sun's
longitudinal speed. It is not a complete phase-angle or illumination
calculation.

Comparison requires increasing epochs and matching calculation context. For
topocentric comparison, the observer position must also match.

Longitude displacement uses the principal signed angular difference in
[-180°, 180°). This resolves wraparound for nearby observations, such as
359° to 1°, but it does not recover complete revolutions between widely
spaced snapshots. The reported mean rate is therefore a principal-arc rate,
not a substitute for a sampled trajectory or event-crossing search.

The comparison implementation and its edge-case tests are available in
[calendar_engine.py](../calendar_engine.py) and
[test_calendar_engine_comparison.py](../test_calendar_engine_comparison.py).

## Reconstructing the baseline

From a clean checkout on the default master branch:

~~~sh
python -m pip install -r requirements.txt
python demo.py
pytest -v
~~~

The demonstration performs two live observations one day apart, displays
geocentric and observer-conditioned states, and compares the retained results.

Tests are divided by evidential role:

- [test_calendar_engine_observe.py](../test_calendar_engine_observe.py)
  uses a deterministic test double to verify normalization, retained values,
  observer handling and relative relationships.
- [test_calendar_engine_comparison.py](../test_calendar_engine_comparison.py)
  verifies source retention, comparison semantics, wraparound, epoch ordering
  and comparability constraints.
- [test_ephemeris.py](../test_ephemeris.py) exercises the installed
  LibEphemeris dependency directly.
- [verify_julday.py](../verify_julday.py) checks one known Julian Day reference.
- [CI workflow](../.github/workflows/test.yml) runs the installation,
  verification, demonstration and test path under Python 3.12 and 3.13.

The recorded baseline CI evidence is linked from
[trace 0002](traces/0002-astronomical-core-baseline.md).

## Not-yet-represented relationships

This baseline does not yet calculate or preserve:

- event-crossing times and intervals;
- named recurrence models or interactions between different cycles;
- trajectory samples sufficient to resolve complete revolutions across
  arbitrary intervals;
- local horizontal coordinates, horizon crossings or practical visibility;
- lunar/solar tidal forcing combined with local tidal characteristics;
- growing, harvesting or other ecological condition observations;
- Almanac knowledge, generative grammar or orthopractic declarations.

These are boundaries of the current executable state, not a complete list of
the domain's possible requirements. Their treatment should be established by
subsequent observation and bounded development increments.
