"""End-to-end tests for CalendarEngine.observe() datetime handling.

These tests exercise the engine's real datetime-to-Julian-date conversion path.
Ephemeris position calculation is stubbed so the JD passed into calc_ut() can
be recorded without loading planetary data files.
"""

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

import pytest

import calendar_engine
from calendar_engine import CalendarEngine


def expected_julian_day(dt: datetime) -> float:
    """Calculate the JD expected for the UTC instant represented by dt."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    utc = dt.astimezone(timezone.utc)
    fractional_hour = (
        utc.hour
        + utc.minute / 60
        + (utc.second + utc.microsecond / 1_000_000) / 3600
    )
    return calendar_engine.eph.julday(
        utc.year, utc.month, utc.day, fractional_hour
    )


def observe_with_recorded_calc_ut(monkeypatch, dt=None):
    """Run observe() while recording the JD passed to each calc_ut() call."""
    recorded_jds = []

    def recording_calc_ut(jd, body, flags):
        recorded_jds.append(jd)
        # The engine only consumes the returned ecliptic longitude.
        longitude = 42.0 if body == calendar_engine.SUN else 84.0
        return ([longitude, 0.0, 1.0, 0.0, 0.0, 0.0], None)

    monkeypatch.setattr(calendar_engine.eph, "calc_ut", recording_calc_ut)
    observation = CalendarEngine().observe(dt)
    assert len(recorded_jds) == 2  # Sun and Moon are calculated at one instant.
    assert recorded_jds[0] == pytest.approx(recorded_jds[1], abs=1e-12)
    return observation, recorded_jds[0]


def test_observe_utc_aware_datetime(monkeypatch):
    dt = datetime(2026, 11, 3, 12, 0, 0, tzinfo=timezone.utc)

    observation, actual_jd = observe_with_recorded_calc_ut(monkeypatch, dt)

    assert actual_jd == pytest.approx(expected_julian_day(dt), abs=1e-12)
    assert observation.timestamp.astimezone(timezone.utc) == dt


def test_observe_nonzero_offset_datetime_uses_same_instant(monkeypatch):
    # 17:30 at UTC+05:30 is exactly 12:00 UTC.
    dt = datetime(
        2026, 11, 3, 17, 30, 0,
        tzinfo=timezone(timedelta(hours=5, minutes=30)),
    )
    expected_utc = datetime(2026, 11, 3, 12, 0, 0, tzinfo=timezone.utc)

    observation, actual_jd = observe_with_recorded_calc_ut(monkeypatch, dt)

    assert actual_jd == pytest.approx(expected_julian_day(expected_utc), abs=1e-12)
    assert observation.timestamp.astimezone(timezone.utc) == expected_utc


def test_observe_naive_datetime_assumes_utc_by_contract(monkeypatch):
    dt = datetime(2026, 11, 3, 12, 0, 0)

    observation, actual_jd = observe_with_recorded_calc_ut(monkeypatch, dt)

    assert actual_jd == pytest.approx(expected_julian_day(dt), abs=1e-12)
    assert observation.timestamp == dt.replace(tzinfo=timezone.utc)
    assert observation.timestamp.utcoffset() == timedelta(0)


def test_observe_preserves_microseconds_in_julian_day(monkeypatch):
    dt = datetime(2026, 11, 3, 12, 0, 0, 500_000, tzinfo=timezone.utc)

    observation, actual_jd = observe_with_recorded_calc_ut(monkeypatch, dt)

    assert actual_jd == pytest.approx(expected_julian_day(dt), abs=1e-12)
    assert observation.timestamp == dt
    assert observation.timestamp.microsecond == 500_000


def test_observe_default_uses_current_utc_datetime(monkeypatch):
    fixed_now = datetime(2026, 11, 3, 12, 0, 0, 250_000, tzinfo=timezone.utc)

    class FixedDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            assert tz is timezone.utc
            return fixed_now

    monkeypatch.setattr(calendar_engine, "datetime", FixedDateTime)
    observation, actual_jd = observe_with_recorded_calc_ut(monkeypatch)

    assert actual_jd == pytest.approx(expected_julian_day(fixed_now), abs=1e-12)
    assert observation.timestamp == fixed_now
    assert observation.timestamp.tzinfo is timezone.utc
