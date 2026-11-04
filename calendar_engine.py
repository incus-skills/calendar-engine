"""Astronomical observation core for the Calendar Engine.

The core preserves astronomical states and the context in which they were
calculated. It keeps geocentric reference positions distinct from optional
observer-centred positions and does not assign calendar, cultural, or
operational meanings to astronomical configurations.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
from math import isfinite
from typing import Literal, Mapping

from libephemeris import EphemerisContext
from libephemeris.constants import (
    FLG_J2000,
    FLG_SPEED,
    FLG_TOPOCTR,
    MOON,
    SUN,
)

BodyName = Literal["sun", "moon"]
CoordinateOrigin = Literal["geocentric", "topocentric"]


def _libephemeris_version() -> str:
    try:
        return version("libephemeris")
    except PackageNotFoundError:
        return "unknown"


def _utc_datetime(value: datetime | None) -> datetime:
    """Normalize an instant to UTC; naive datetimes are assumed to be UTC."""
    if value is None:
        return datetime.now(timezone.utc)
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _julian_day_ut(value: datetime) -> float:
    """Build a Julian day for UT, using UTC as a proxy (no DUT1 correction)."""
    fractional_hour = (
        value.hour
        + value.minute / 60.0
        + (value.second + value.microsecond / 1_000_000.0) / 3600.0
    )
    # libephemeris.calc_ut expects a UT Julian day. UTC is used as a close
    # proxy here; a DUT1 correction is not currently applied.
    import libephemeris as eph

    return eph.julday(
        value.year, value.month, value.day, fractional_hour
    )


@dataclass(frozen=True)
class ObserverPosition:
    """A geographic observer position used for topocentric calculations."""

    latitude_deg: float
    longitude_deg: float
    altitude_m: float | None = None

    def __post_init__(self) -> None:
        values = (self.latitude_deg, self.longitude_deg)
        if not all(isfinite(value) for value in values):
            raise ValueError("Observer coordinates must be finite numbers")
        if self.altitude_m is not None and not isfinite(self.altitude_m):
            raise ValueError("Observer altitude must be a finite number when supplied")
        if not -90.0 <= self.latitude_deg <= 90.0:
            raise ValueError("Latitude must be between -90 and 90 degrees")
        if not -180.0 <= self.longitude_deg <= 180.0:
            raise ValueError("Longitude must be between -180 and 180 degrees")


@dataclass(frozen=True)
class CalculationContext:
    """Shared provenance for one astronomical observation."""

    library: str
    library_version: str
    timestamp_scale: str
    ephemeris_time_scale: str
    dut1_correction_applied: bool
    reference_frame: str


@dataclass(frozen=True)
class CoordinateFrame:
    """Coordinate origin and flags for a set of body coordinates."""

    origin: CoordinateOrigin
    reference_frame: str
    requested_flags: int
    returned_flags: int


@dataclass(frozen=True)
class BodyState:
    """Six-component position and motion result for one body and epoch.

    Distances are in astronomical units; angular rates are degrees/day and
    distance rates are AU/day, following the LibEphemeris calc_ut contract.
    """

    body: BodyName
    body_id: int
    longitude_deg: float
    latitude_deg: float
    distance_au: float
    longitude_speed_deg_per_day: float
    latitude_speed_deg_per_day: float
    distance_speed_au_per_day: float
    frame: CoordinateFrame


@dataclass(frozen=True)
class RelativeLongitude:
    """Directed ecliptic-longitude relationship between two bodies."""

    from_body: BodyName
    to_body: BodyName
    origin: CoordinateOrigin
    separation_deg: float
    separation_speed_deg_per_day: float


@dataclass(frozen=True)
class AstronomicalObservation:
    """Astronomical states at one instant, retaining both source frames."""

    timestamp_utc: datetime
    julian_day_ut: float
    calculation_context: CalculationContext
    observer: ObserverPosition | None
    geocentric: Mapping[BodyName, BodyState]
    topocentric: Mapping[BodyName, BodyState]
    geocentric_moon_sun: RelativeLongitude
    topocentric_moon_sun: RelativeLongitude | None

    def states(self, origin: CoordinateOrigin = "geocentric") -> Mapping[BodyName, BodyState]:
        """Return retained body states for the requested coordinate origin."""
        if origin == "geocentric":
            return self.geocentric
        if origin == "topocentric":
            if self.observer is None:
                raise ValueError("Topocentric states require an observer position")
            return self.topocentric
        raise ValueError(f"Unsupported coordinate origin: {origin}")


@dataclass(frozen=True)
class BodyChange:
    """Change in one body's retained state between two observations.

    The longitude displacement is the principal signed angular difference.
    It does not recover complete revolutions across a long observation gap.
    """

    earlier: BodyState
    later: BodyState
    principal_longitude_change_deg: float
    latitude_change_deg: float
    distance_change_au: float
    principal_mean_longitude_rate_deg_per_day: float
    mean_longitude_acceleration_deg_per_day2: float


@dataclass(frozen=True)
class ObservationComparison:
    """A comparison that retains both original observations and derived change."""

    earlier: AstronomicalObservation
    later: AstronomicalObservation
    origin: CoordinateOrigin
    elapsed_days: float
    body_changes: Mapping[BodyName, BodyChange]


def _relative_longitude(
    states: Mapping[BodyName, BodyState], origin: CoordinateOrigin
) -> RelativeLongitude:
    sun = states["sun"]
    moon = states["moon"]
    return RelativeLongitude(
        from_body="sun",
        to_body="moon",
        origin=origin,
        separation_deg=(moon.longitude_deg - sun.longitude_deg) % 360.0,
        separation_speed_deg_per_day=(
            moon.longitude_speed_deg_per_day - sun.longitude_speed_deg_per_day
        ),
    )


def _calculate_states(
    jd_ut: float,
    origin: CoordinateOrigin,
    observer: ObserverPosition | None,
) -> dict[BodyName, BodyState]:
    context = EphemerisContext()
    flags = FLG_SPEED | FLG_J2000
    if origin == "topocentric":
        if observer is None:
            raise ValueError("Topocentric calculation requires an observer position")
        context.set_topo(
            observer.longitude_deg,
            observer.latitude_deg,
            observer.altitude_m if observer.altitude_m is not None else 0.0,
        )
        flags |= FLG_TOPOCTR

    calculated: dict[BodyName, BodyState] = {}
    for name, body_id in (("sun", SUN), ("moon", MOON)):
        position, returned_flags = context.calc_ut(jd_ut, body_id, flags)
        if len(position) < 6:
            raise RuntimeError(
                f"LibEphemeris returned {len(position)} values for {name}; expected 6"
            )
        values = tuple(float(value) for value in position[:6])
        if not all(isfinite(value) for value in values):
            raise RuntimeError(f"LibEphemeris returned non-finite values for {name}")
        frame = CoordinateFrame(
            origin=origin,
            reference_frame="J2000 ecliptic",
            requested_flags=flags,
            returned_flags=int(returned_flags),
        )
        calculated[name] = BodyState(
            body=name,
            body_id=body_id,
            longitude_deg=values[0] % 360.0,
            latitude_deg=values[1],
            distance_au=values[2],
            longitude_speed_deg_per_day=values[3],
            latitude_speed_deg_per_day=values[4],
            distance_speed_au_per_day=values[5],
            frame=frame,
        )
    return calculated


class CalendarEngine:
    """Acquire and compare astronomical states without assigning meanings."""

    def __init__(
        self,
        observer: ObserverPosition | None = None,
        *,
        latitude: float | None = None,
        longitude: float | None = None,
        altitude_m: float | None = None,
    ) -> None:
        if (latitude is None) != (longitude is None):
            raise ValueError("Latitude and longitude must be supplied together")
        if observer is not None and latitude is not None:
            raise ValueError("Supply observer or latitude/longitude, not both")
        if latitude is not None and longitude is not None:
            observer = ObserverPosition(latitude, longitude, altitude_m)
        self.observer = observer

    def observe(self, dt: datetime | None = None) -> AstronomicalObservation:
        """Calculate Sun/Moon geocentric states and optional local topocentric states.

        Naive datetimes are assumed to be UTC. Aware datetimes are normalized
        to UTC. UTC is supplied to the UT calculation interface without DUT1
        correction. The fixed J2000 ecliptic frame makes positions comparable
        across observation epochs.
        """
        timestamp_utc = _utc_datetime(dt)
        jd_ut = _julian_day_ut(timestamp_utc)
        geocentric = _calculate_states(jd_ut, "geocentric", None)
        topocentric: dict[BodyName, BodyState] = {}
        topocentric_relative: RelativeLongitude | None = None
        if self.observer is not None:
            topocentric = _calculate_states(jd_ut, "topocentric", self.observer)
            topocentric_relative = _relative_longitude(topocentric, "topocentric")

        calculation_context = CalculationContext(
            library="libephemeris",
            library_version=_libephemeris_version(),
            timestamp_scale="UTC",
            ephemeris_time_scale="UT (UTC proxy)",
            dut1_correction_applied=False,
            reference_frame="J2000 ecliptic",
        )
        return AstronomicalObservation(
            timestamp_utc=timestamp_utc,
            julian_day_ut=jd_ut,
            calculation_context=calculation_context,
            observer=self.observer,
            geocentric=geocentric,
            topocentric=topocentric,
            geocentric_moon_sun=_relative_longitude(geocentric, "geocentric"),
            topocentric_moon_sun=topocentric_relative,
        )

    def compare(
        self,
        earlier: AstronomicalObservation,
        later: AstronomicalObservation,
        origin: CoordinateOrigin = "geocentric",
    ) -> ObservationComparison:
        return compare_observations(earlier, later, origin)


def _signed_angular_difference(later: float, earlier: float) -> float:
    """Shortest signed angular displacement in [-180, 180) degrees."""
    return (later - earlier + 180.0) % 360.0 - 180.0


def compare_observations(
    earlier: AstronomicalObservation,
    later: AstronomicalObservation,
    origin: CoordinateOrigin = "geocentric",
) -> ObservationComparison:
    """Compare like-for-like states while retaining both source observations.

    Longitude change is reported on the principal arc [-180, 180). Two
    snapshots alone cannot reveal the number of complete revolutions between
    them; trajectory/event sampling is needed to resolve long-gap winding.
    """
    elapsed_days = later.julian_day_ut - earlier.julian_day_ut
    if elapsed_days <= 0.0:
        raise ValueError("Later observation must have a greater Julian day")
    if earlier.calculation_context != later.calculation_context:
        raise ValueError("Observations have different calculation contexts")
    if origin == "topocentric" and earlier.observer != later.observer:
        raise ValueError("Topocentric observations require the same observer position")

    earlier_states = earlier.states(origin)
    later_states = later.states(origin)
    if earlier_states.keys() != later_states.keys():
        raise ValueError("Observations contain different body sets")

    changes: dict[BodyName, BodyChange] = {}
    for name in earlier_states:
        first = earlier_states[name]
        second = later_states[name]
        if (
            first.body_id != second.body_id
            or first.frame.origin != second.frame.origin
            or first.frame.reference_frame != second.frame.reference_frame
            or first.frame.requested_flags != second.frame.requested_flags
            or first.frame.returned_flags != second.frame.returned_flags
        ):
            raise ValueError(f"Observations for {name} are not comparable")
        longitude_change = _signed_angular_difference(
            second.longitude_deg, first.longitude_deg
        )
        changes[name] = BodyChange(
            earlier=first,
            later=second,
            principal_longitude_change_deg=longitude_change,
            latitude_change_deg=second.latitude_deg - first.latitude_deg,
            distance_change_au=second.distance_au - first.distance_au,
            principal_mean_longitude_rate_deg_per_day=longitude_change / elapsed_days,
            mean_longitude_acceleration_deg_per_day2=(
                second.longitude_speed_deg_per_day
                - first.longitude_speed_deg_per_day
            ) / elapsed_days,
        )

    return ObservationComparison(
        earlier=earlier,
        later=later,
        origin=origin,
        elapsed_days=elapsed_days,
        body_changes=changes,
    )