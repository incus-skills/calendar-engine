# Calendar Engine

## Purpose

The Calendar Engine provides a computational foundation for establishing
observer position within recurring astronomical and environmental cycles.
Its first core layer acquires astronomical states, preserves their motion and
calculation context, and supports comparison across epochs.

Astronomical calculations do not by themselves assign cultural meaning,
determine appropriate practice, or establish local environmental suitability.
Those relationships belong to higher layers that can use the core without
being conflated with it.

## Current baseline

The executable baseline provides:

- Sun and Moon geocentric ecliptic states at a supplied epoch.
- Retention of longitude, latitude, distance, and all three corresponding
  motion components returned by LibEphemeris.
- An explicit J2000 ecliptic reference frame for comparison across epochs.
- Optional observer-conditioned topocentric states, kept separate from the
  geocentric reference states.
- A directed Moon–Sun ecliptic-longitude relationship and its instantaneous
  rate of change for each available coordinate origin.
- Like-for-like observation comparison that retains both source observations
  and derives principal angular displacement, principal-arc mean rate, and rate
  change. Two snapshots alone cannot reveal the count of complete revolutions
  across a long interval; trajectory sampling is required to resolve that.
- Calculation provenance including the LibEphemeris version, input time
  scale, ephemeris time-scale convention, DUT1 status, and reference frame.

## Time handling

CalendarEngine.observe() accepts aware or naive Python datetimes. Aware
values are normalized to UTC; naive values are interpreted as UTC. The UTC
components are converted to a Julian day and supplied to LibEphemeris' UT
calculation interface. UTC is used as a proxy for UT; no DUT1 correction is
currently applied. The observation records this explicitly.

## Observer handling

An observer is optional and must be supplied explicitly as an
ObserverPosition. Without one, the engine returns geocentric states only.
With one, it calculates a separate topocentric set using an isolated
EphemerisContext. The geocentric states remain available as the common
reference. If altitude is omitted, the topocentric calculation uses 0 m while
the observation retains altitude_m=None to show that sea level was assumed
rather than observed or supplied.

Topocentric ecliptic coordinates are not equivalent to horizontal altitude
and azimuth, horizon crossing, atmospheric visibility, or practical
observability. Those are not implemented in this baseline.

## Units and conventions

- Ecliptic longitude and latitude: degrees.
- Distance: astronomical units (AU).
- Angular motion: degrees per day.
- Distance motion: AU per day.
- Epoch: UTC timestamp plus Julian day supplied on the UT interface.
- Reference frame: J2000 ecliptic.

The retained Moon–Sun relationship is a directed difference in ecliptic
longitude. It is not presented as a complete lunar phase-angle or illumination
calculation. Snapshot comparison reports the shortest signed angular
displacement; it does not infer unobserved complete revolutions.

## Not yet implemented

This baseline does not yet provide event-crossing searches, named recurrence
models, local horizontal coordinates, horizon/visibility calculations,
tidal prediction, seasonal or agricultural condition models, Almanac content,
or cultural/orthopractic declarations. The current point is to establish a
reliable state-and-motion foundation from which those can be developed as
separate, testable capabilities.

## Run

    python demo.py
    pytest -v

The integration tests exercise the installed LibEphemeris runtime. The
observation and comparison tests use a deterministic test double to verify
engine behaviour independently of ephemeris data availability.
