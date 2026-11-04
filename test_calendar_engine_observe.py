"""Deterministic tests for time normalization and observation acquisition."""

from datetime import datetime, timedelta, timezone

import pytest

import calendar_engine
from calendar_engine import CalendarEngine, ObserverPosition


class FakeEphemerisContext:
    instances = []

    def __init__(self):
        self.topo = None
        self.calls = []
        self.__class__.instances.append(self)

    def set_topo(self, longitude, latitude, altitude):
        self.topo = (longitude, latitude, altitude)

    def calc_ut(self, jd, body, flags):
        self.calls.append((jd, body, flags))
        offset = 0.0 if body == calendar_engine.SUN else 100.0
        position = [
            (10.0 + offset + (jd - 2461348.0)) % 360.0,
            1.0 + offset / 100.0,
            1.0 + offset / 1000.0,
            1.0 + offset / 10.0,
            0.1 + offset / 100.0,
            0.001 + offset / 1000.0,
        ]
        return position, flags


def install_fake_ephemeris(monkeypatch):
    FakeEphemerisContext.instances = []
    monkeypatch.setattr(calendar_engine, "EphemerisContext", FakeEphemerisContext)
    monkeypatch.setattr(calendar_engine, "_libephemeris_version", lambda: "test-version")


def test_observe_normalizes_utc_offset_and_retains_epoch(monkeypatch):
    install_fake_ephemeris(monkeypatch)
    dt = datetime(
        2026, 11, 3, 17, 30, 0,
        tzinfo=timezone(timedelta(hours=5, minutes=30)),
    )

    observation = CalendarEngine().observe(dt)

    assert observation.timestamp_utc == datetime(2026, 11, 3, 12, 0, tzinfo=timezone.utc)
    assert observation.julian_day_ut == pytest.approx(2461348.0)
    assert observation.calculation_context.timestamp_scale == "UTC"
    assert observation.calculation_context.ephemeris_time_scale == "UT (UTC proxy)"
    assert observation.calculation_context.dut1_correction_applied is False


def test_naive_datetime_is_assumed_utc(monkeypatch):
    install_fake_ephemeris(monkeypatch)
    observation = CalendarEngine().observe(datetime(2026, 11, 3, 12, 0))
    assert observation.timestamp_utc == datetime(2026, 11, 3, 12, 0, tzinfo=timezone.utc)


def test_observation_retains_six_position_and_motion_values(monkeypatch):
    install_fake_ephemeris(monkeypatch)
    observation = CalendarEngine().observe(datetime(2026, 11, 3, 12, tzinfo=timezone.utc))
    moon = observation.geocentric["moon"]

    assert moon.longitude_deg == pytest.approx(110.0)
    assert moon.latitude_deg == pytest.approx(2.0)
    assert moon.distance_au == pytest.approx(1.1)
    assert moon.longitude_speed_deg_per_day == pytest.approx(11.0)
    assert moon.latitude_speed_deg_per_day == pytest.approx(1.1)
    assert moon.distance_speed_au_per_day == pytest.approx(0.101)
    assert moon.frame.origin == "geocentric"
    assert moon.frame.reference_frame == "J2000 ecliptic"


def test_observer_produces_separate_topocentric_states(monkeypatch):
    install_fake_ephemeris(monkeypatch)
    observer = ObserverPosition(51.5, -0.1, 25.0)
    observation = CalendarEngine(observer=observer).observe(
        datetime(2026, 11, 3, 12, tzinfo=timezone.utc)
    )

    assert observation.observer == observer
    assert set(observation.geocentric) == {"sun", "moon"}
    assert set(observation.topocentric) == {"sun", "moon"}
    assert observation.topocentric["moon"].frame.origin == "topocentric"
    assert observation.topocentric["moon"].frame.requested_flags & calendar_engine.FLG_TOPOCTR
    topo_context = FakeEphemerisContext.instances[1]
    assert topo_context.topo == (-0.1, 51.5, 25.0)


def test_no_observer_does_not_invent_local_coordinates(monkeypatch):
    install_fake_ephemeris(monkeypatch)
    observation = CalendarEngine().observe(datetime(2026, 11, 3, 12, tzinfo=timezone.utc))
    assert observation.observer is None
    assert observation.topocentric == {}
    assert observation.topocentric_moon_sun is None


def test_relative_longitude_retains_relationship_and_rate(monkeypatch):
    install_fake_ephemeris(monkeypatch)
    observation = CalendarEngine().observe(datetime(2026, 11, 3, 12, tzinfo=timezone.utc))
    relation = observation.geocentric_moon_sun
    assert relation.from_body == "sun"
    assert relation.to_body == "moon"
    assert relation.separation_deg == pytest.approx(100.0)
    assert relation.separation_speed_deg_per_day == pytest.approx(10.0)


def test_observer_coordinates_are_validated():
    with pytest.raises(ValueError):
        ObserverPosition(91.0, 0.0)
    with pytest.raises(ValueError):
        ObserverPosition(0.0, 181.0)


def test_latitude_and_longitude_must_be_supplied_together():
    with pytest.raises(ValueError):
        CalendarEngine(latitude=51.5)


def test_unspecified_observer_altitude_is_recorded_as_unspecified(monkeypatch):
    install_fake_ephemeris(monkeypatch)
    observer = ObserverPosition(51.5, -0.1)
    observation = CalendarEngine(observer=observer).observe(
        datetime(2026, 11, 3, 12, tzinfo=timezone.utc)
    )
    assert observation.observer.altitude_m is None
    assert FakeEphemerisContext.instances[1].topo == (-0.1, 51.5, 0.0)
