"""Integration smoke tests against the installed LibEphemeris dependency."""

from datetime import datetime, timezone
from math import isfinite

from calendar_engine import CalendarEngine, ObserverPosition
from libephemeris.constants import FLG_J2000, FLG_SPEED, FLG_TOPOCTR


def test_live_ephemeris_returns_sun_and_moon_state():
    observation = CalendarEngine().observe(
        datetime(2026, 11, 3, 12, 0, tzinfo=timezone.utc)
    )

    assert set(observation.geocentric) == {"sun", "moon"}
    for state in observation.geocentric.values():
        assert 0.0 <= state.longitude_deg < 360.0
        assert all(
            isfinite(value)
            for value in (
                state.latitude_deg,
                state.distance_au,
                state.longitude_speed_deg_per_day,
                state.latitude_speed_deg_per_day,
                state.distance_speed_au_per_day,
            )
        )
        assert state.frame.origin == "geocentric"
        assert state.frame.requested_flags & FLG_SPEED
        assert state.frame.requested_flags & FLG_J2000


def test_live_ephemeris_applies_observer_position_to_topocentric_states():
    observation = CalendarEngine(
        observer=ObserverPosition(51.5, -0.1, 25.0)
    ).observe(datetime(2026, 11, 3, 12, 0, tzinfo=timezone.utc))

    assert set(observation.topocentric) == {"sun", "moon"}
    assert observation.topocentric["moon"].frame.origin == "topocentric"
    assert observation.topocentric["moon"].frame.requested_flags & FLG_TOPOCTR
