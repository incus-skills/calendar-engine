# demo.py

from calendar_engine import CalendarEngine, RawObservation, OperationalField


def main():
    print("Calendar Operational Reconstruction Engine")
    print("Frozen Specification Realization with Ecological Separation")
    print("=" * 60)

    engine = CalendarEngine()

    print("\n1. Observation (Runtime)")
    obs = engine.observe()
    print(f"   Solar: {obs.solar_longitude:.2f}°")
    print(f"   Lunar: {obs.lunar_longitude:.2f}°")
    print(f"   Phase: {obs.lunar_phase:.2f}°")

    print("\n2. Recognition (Runtime)")
    dist = engine._recognize(obs)
    print(f"   Solar distinction: {dist.solar_position}")
    print(f"   Lunar distinction: {dist.lunar_position}")

    print("\n3. Classification (Runtime, using Ecology Schema)")
    cat = engine._classify(dist)
    print(f"   Solar category: {cat.solar_category}")
    print(f"   Lunar category: {cat.lunar_category}")
    print(f"   Combined category: {cat.combined_category}")

    print("\n4. Interpretation (Runtime)")
    meaning = engine._interpret(cat)
    print(f"   Orientation: {meaning.orientation}")
    print(f"   Meaning: {meaning.meaning}")

    print("\n5. Projection (Runtime) → Field")
    field = engine._project(meaning)
    print(f"   Orientation: {field.orientation}")
    print(f"   Active cycles: {field.active_cycles}")
    print(f"   Participation surfaces: {field.participation_surfaces}")

    print("\n6. Complete Reconstruction")
    engine._field = field
    retrieved = engine.field()
    print(f"   Retrieved orientation: {retrieved.orientation}")

    print("\n7. Continuity (Persistence)")
    engine.persist("state.pkl")
    recovered = engine.recover("state.pkl")
    print(f"   Recovered orientation: {recovered.orientation}")

    print("\n8. Re-entry (Scheduling)")

    def callback(f):
        print(f"   Re-entry: Orientation = {f.orientation}")

    engine.schedule(1.0, callback)
    import threading

    timer = threading.Timer(2.0, engine.stop)
    timer.start()
    engine.start()

    print("\n9. Reconstructability (Self-Reference)")
    spec = engine.specification()
    print(f"   Ecology: {len(spec['ecology'])} elements frozen")
    print(f"   Grammar: {len(spec['grammar'])} movements frozen")
    print(f"   Specification: {len(spec['specification'])} operations frozen")
    print(f"   Composition: {len(spec['composition'])} layers frozen")
    print(f"   Contracts: {len(spec['contracts'])} frozen")

    print("\n" + "=" * 60)
    print("Construction Complete. Artifact Delivered.")
    print("The frozen specification remains unchanged.")


if __name__ == "__main__":
    main()
