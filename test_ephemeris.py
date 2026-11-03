import libephemeris as swe
from libephemeris.constants import SUN, MOON, MARS, FLG_SPEED

print("DEBUG: Script is starting", flush=True)

jd = swe.julday(2024, 3, 26, 12.0)

# Planet positions with velocity
sun, _ = swe.calc_ut(jd, SUN, FLG_SPEED)
moon, _ = swe.calc_ut(jd, MOON, FLG_SPEED)
mars, _ = swe.calc_ut(jd, MARS, FLG_SPEED)

# Returns: (longitude, latitude, distance, speed_lon, speed_lat, speed_dist)
print(f"Sun:  {sun[0]:.4f} deg, speed {sun[3]:.4f} deg/day")
print(f"Moon: {moon[0]:.4f} deg, speed {moon[3]:.4f} deg/day")
print(f"Mars: {mars[0]:.4f} deg, speed {mars[3]:.4f} deg/day")
