"""Tests for comparison of retained astronomical states across epochs."""

from datetime import datetime, timezone

import pytest

import calendar_engine
from calendar_engine import CalendarEngine, ObserverPosition
from test_calendar_engine_observe import install_fake_ephemeris


def test_comparison_retains_sources_and_derives_motion(monkeypatch):
    install_fake_ephemeris(monkeypatch)
    engine = CalendarEngine()
    first = engine.observe(datetime(2026, 11, 3, 12, tzinfo=timezone.utc))
    second = engine.observe(datetime(2026, 11, 4, 12, tzinfo=timezone.utc))

    result = engine.compare(first, second)
    assert result.earlier is first
    assert result.later is second
    assert result.elapsed_days == pytest.approx(1.0)
    assert result.body_changes["sun"].earlier is first.geocentric["sun"]
    assert result.body_changes["sun"].later is second.geocentric["sun"]
    assert result.body_changes["sun"].principal_longitude_change_deg == pytest.approx(1.0)
    assert result.body_changes["sun"].principal_mean_longitude_rate_deg_per_day == pytest.approx(1.0)
    assert result.body_changes["sun"].mean_longitude_acceleration_deg_per_day2 == pytest.approx(0.0)


def test_signed_angle_difference_uses_shortest_arc():
    assert calendar_engine._signed_angular_difference(1.0, 359.0) == pytest.approx(2.0)
    assert calendar_engine._signed_angular_difference(359.0, 1.0) == pytest.approx(-2.0)


def test_comparison_rejects_reversed_or_equal_epochs(monkeypatch):
    install_fake_ephemeris(monkeypatch)
    engine = CalendarEngine()
    first = engine.observe(datetime(2026, 11, 3, 12, tzinfo=timezone.utc))
    same = engine.observe(datetime(2026, 11, 3, 12, tzinfo=timezone.utc))
    with pytest.raises(ValueError, match="greater Julian day"):
        engine.compare(first, same)
    with pytest.raises(ValueError, match="greater Julian day"):
        engine.compare(same, first)


def test_topocentric_comparison_requires_same_observer(monkeypatch):
    install_fake_ephemeris(monkeypatch)
    first_engine = CalendarEngine(observer=ObserverPosition(51.5, -0.1))
    second_engine = CalendarEngine(observer=ObserverPosition(40.7, -74.0))
    first = first_engine.observe(datetime(2026, 11, 3, 12, tzinfo=timezone.utc))
    second = second_engine.observe(datetime(2026, 11, 4, 12, tzinfo=timezone.utc))
    with pytest.raises(ValueError, match="same observer position"):
        first_engine.compare(first, second, origin="topocentric")


def test_comparison_rejects_different_calculation_provenance(monkeypatch):
    install_fake_ephemeris(monkeypatch)
    engine = CalendarEngine()
    first = engine.observe(datetime(2026, 11, 3, 12, tzinfo=timezone.utc))
    second = engine.observe(datetime(2026, 11, 4, 12, tzinfo=timezone.utc))
    altered_context = calendar_engine.CalculationContext(
        library="libephemeris",
        library_version="different-version",
        timestamp_scale="UTC",
        ephemeris_time_scale="UT (UTC proxy)",
        dut1_correction_applied=False,
        reference_frame="J2000 ecliptic",
    )
    second = calendar_engine.AstronomicalObservation(
        timestamp_utc=second.timestamp_utc,
        julian_day_ut=second.julian_day_ut,
        calculation_context=altered_context,
        observer=second.observer,
        geocentric=second.geocentric,
        topocentric=second.topocentric,
        geocentric_moon_sun=second.geocentric_moon_sun,
        topocentric_moon_sun=second.topocentric_moon_sun,
    )
    with pytest.raises(ValueError, match="different calculation contexts"):
        engine.compare(first, second)
