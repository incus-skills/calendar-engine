"""Live demonstration of the Calendar Engine astronomical core."""

from datetime import datetime, timedelta, timezone

from calendar_engine import CalendarEngine, ObserverPosition


def main() -> None:
    # Illustrative observer position; replace with an explicit site when used.
    observer = ObserverPosition(
        latitude_deg=51.5,
        longitude_deg=-0.1,
        altitude_m=0.0,
    )
    engine = CalendarEngine(observer=observer)

    now = datetime.now(timezone.utc).replace(microsecond=0)
    earlier = engine.observe(now)
    later = engine.observe(now + timedelta(days=1))
    change = engine.compare(earlier, later)

    print("Calendar Engine — Astronomical Core")
    print(f"UTC epoch: {earlier.timestamp_utc.isoformat()}")
    print(f"Julian day (UT proxy): {earlier.julian_day_ut:.8f}")
    print(
        "Ephemeris: "
        f"{earlier.calculation_context.library} "
        f"{earlier.calculation_context.library_version}"
    )
    print(f"Reference frame: {earlier.calculation_context.reference_frame}")

    print("\nGeocentric states")
    for name, state in earlier.geocentric.items():
        print(
            f"{name.title():4} "
            f"lon={state.longitude_deg:10.6f}° "
            f"lat={state.latitude_deg:9.6f}° "
            f"distance={state.distance_au:.9f} AU "
            f"motion={state.longitude_speed_deg_per_day:.6f}°/day"
        )
    relative = earlier.geocentric_moon_sun
    print(
        "Moon–Sun ecliptic-longitude separation: "
        f"{relative.separation_deg:.6f}° "
        f"({relative.separation_speed_deg_per_day:.6f}°/day)"
    )

    print("\nObserver-conditioned states")
    for name, state in earlier.topocentric.items():
        print(
            f"{name.title():4} "
            f"lon={state.longitude_deg:10.6f}° "
            f"lat={state.latitude_deg:9.6f}°"
        )
    print("These are topocentric ecliptic coordinates, not horizon visibility.")

    print("\nOne-day state comparison")
    for name, movement in change.body_changes.items():
        print(
            f"{name.title():4} "
            f"principal Δlongitude={movement.principal_longitude_change_deg:+.6f}° "
            f"principal mean rate={movement.principal_mean_longitude_rate_deg_per_day:+.6f}°/day "
            f"rate change={movement.mean_longitude_acceleration_deg_per_day2:+.6f}°/day²"
        )


if __name__ == "__main__":
    main()
