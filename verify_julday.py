"""Runtime verification of libephemeris julday() against a known reference.

ORB-2: verifies that eph.julday(2026, 11, 3, 12.0) == 2461348.0.
This exercises the actual libephemeris runtime, closing the gap left by
the controlled conversion probe.
"""

import libephemeris as eph


def test_julday_known_epoch():
    """ORB-2 reference: 2026-11-03 12:00:00 UTC should be JD 2461348.0."""
    jd = eph.julday(2026, 11, 3, 12.0)
    assert abs(jd - 2461348.0) < 1e-9, f"Expected 2461348.0, got {jd}"


if __name__ == "__main__":
    test_julday_known_epoch()
    print("PASS: julday(2026, 11, 3, 12.0) == 2461348.0")
