# calendar_engine.py (updated observe())
# Frozen Specification Realization

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Callable, List, Dict, Any
import libephemeris as ephem
import pickle
import sched
import time
# import math
# import json


# === Ecology ===
# Classification Schema (Frozen)
class Phase:
    """Ecological classification schema."""

    # Solar phases
    SOLSTICE = "solstice"
    EQUINOX = "equinox"
    # Lunar phases
    NEW = "new"
    WAXING = "waxing"
    FULL = "full"
    WANING = "waning"
    # Combined phases
    ACCUMULATION = "accumulation"
    EXPRESSION = "expression"
    INTEGRATION = "integration"
    SIMPLIFICATION = "simplification"


# Affordances (Incorporated)
# - Ephemeris: to be provided by skyfield or equivalent
# - Persistence: file I/O, pickle
# - Scheduling: sched, asyncio
# - Interface: function-based API

# Contracts (Frozen)
# - Continuity: field coherence across changes
# - Recurrence: distinguishable return
# - Directionality: irreversible ordering
# - Reachability: observer establishment
# - Persistence: state recovery
# - Reconstructive Integrity: self-reference


# === Runtime ===
@dataclass
class RawObservation:
    """Raw measurements (Observation activity)."""

    timestamp: datetime
    latitude: float
    longitude: float
    solar_longitude: float
    lunar_longitude: float
    lunar_phase: float


@dataclass
class Distinction:
    """Preserved distinctions (Recognition activity)."""

    solar_position: str  # "spring", "summer", "autumn", "winter"
    lunar_position: str  # "new", "waxing", "full", "waning"
    combined_phase: float  # 0-360


@dataclass
class Category:
    """Assigned categories (Classification activity, using Schema)."""

    solar_category: str  # Phase.SOLSTICE, Phase.EQUINOX, etc.
    lunar_category: str  # Phase.NEW, Phase.WAXING, etc.
    combined_category: str  # Phase.ACCUMULATION, etc.


@dataclass
class OperationalMeaning:
    """Operational interpretation (Interpretation activity)."""

    orientation: str  # Phase.ACCUMULATION, Phase.EXPRESSION, etc.
    meaning: str  # "Build", "Express", "Integrate", "Simplify"


@dataclass
class OperationalField:
    """Resulting operational state (Projection activity → Field)."""

    orientation: str
    active_cycles: List[str]
    transitions: Dict[str, Any]
    participation_surfaces: List[str]
    persistence_horizons: Dict[str, Any]
    calibration_state: Dict[str, Any]
    reconstructive_integrity: float


# === Complete Runtime ===
class CalendarEngine:
    """
    Operational Reconstruction Engine.
    Realizes the frozen Artifact Specification with ecological separation.
    """

    def __init__(self, latitude: float = 51.5, longitude: float = -0.1):
        self.latitude = latitude
        self.longitude = longitude
        self._field: Optional[OperationalField] = None
        self._scheduler = sched.scheduler(time.time, time.sleep)
        self._callbacks: List[Callable] = []
        self._running = False

    # === 1. Observation (Runtime Activity) ===
    # def observe(self, dt: Optional[datetime] = None) -> RawObservation:
    #     """Acquire raw measurements."""
    #     if dt is None:
    #         dt = datetime.now()
    #     # In production: use Skyfield
    #     day_of_year = dt.timetuple().tm_yday
    #     solar_longitude = (day_of_year / 365.25) * 360.0
    #     days_since_epoch = (dt - datetime(2000, 1, 1)).days
    #     lunar_longitude = (days_since_epoch * 13.37) % 360.0
    #     lunar_phase = (lunar_longitude - solar_longitude) % 360.0
    #     return RawObservation(
    #         timestamp=dt,
    #         latitude=self.latitude,
    #         longitude=self.longitude,
    #         solar_longitude=solar_longitude,
    #         lunar_longitude=lunar_longitude,
    #         lunar_phase=lunar_phase,
    #     )

    def observe(self, dt: Optional[datetime] = None) -> RawObservation:
        """Acquire live astronomical observations via ephemeris."""
        if dt is None:
            dt = datetime.now()

        # Create observer location
        obs = ephem.Observer()
        obs.lat = str(self.latitude)
        obs.long = str(self.longitude)
        obs.date = dt.strftime("%Y/%m/%d %H:%M:%S")

        # Solar position
        sun = ephem.Sun()
        sun.compute(obs)
        solar_longitude = sun.ra * 180.0 / 3.14159  # Convert to degrees

        # Lunar position
        moon = ephem.Moon()
        moon.compute(obs)
        lunar_longitude = moon.ra * 180.0 / 3.14159  # Convert to degrees

        # Lunar phase (0-360)
        lunar_phase = (lunar_longitude - solar_longitude) % 360.0

        return RawObservation(
            timestamp=dt,
            latitude=self.latitude,
            longitude=self.longitude,
            solar_longitude=solar_longitude,
            lunar_longitude=lunar_longitude,
            lunar_phase=lunar_phase,
        )

    # === 2. Recognition (Runtime Activity) ===
    def _recognize(self, obs: RawObservation) -> Distinction:
        """Preserve distinctions."""
        # Solar position
        solar_pos = obs.solar_longitude
        if 0 <= solar_pos < 90:
            solar_dist = "spring"
        elif 90 <= solar_pos < 180:
            solar_dist = "summer"
        elif 180 <= solar_pos < 270:
            solar_dist = "autumn"
        else:
            solar_dist = "winter"

        # Lunar position
        phase = obs.lunar_phase
        if phase < 45 or phase > 315:
            lunar_dist = "waxing"
        elif 45 <= phase < 135:
            lunar_dist = "full"
        elif 135 <= phase < 225:
            lunar_dist = "waning"
        else:
            lunar_dist = "new"

        return Distinction(
            solar_position=solar_dist,
            lunar_position=lunar_dist,
            combined_phase=obs.lunar_phase,
        )

    # === 3. Classification (Runtime Activity, using Schema) ===
    def _classify(self, dist: Distinction) -> Category:
        """Assign categories using ecological schema."""
        # Solar category
        if dist.solar_position == "spring" or dist.solar_position == "autumn":
            solar_cat = Phase.EQUINOX
        else:
            solar_cat = Phase.SOLSTICE

        # Lunar category
        lunar_cat = dist.lunar_position

        # Combined category
        phase = dist.combined_phase
        if phase < 45 or phase > 315:
            combined_cat = Phase.ACCUMULATION
        elif 45 <= phase < 135:
            combined_cat = Phase.EXPRESSION
        elif 135 <= phase < 225:
            combined_cat = Phase.INTEGRATION
        else:
            combined_cat = Phase.SIMPLIFICATION

        return Category(
            solar_category=solar_cat,
            lunar_category=lunar_cat,
            combined_category=combined_cat,
        )

    # === 4. Interpretation (Runtime Activity) ===
    def _interpret(self, cat: Category) -> OperationalMeaning:
        """Assign operational meaning."""
        # Map category to orientation
        orientation = cat.combined_category

        # Map to meaning
        meaning_map = {
            Phase.ACCUMULATION: "Build",
            Phase.EXPRESSION: "Express",
            Phase.INTEGRATION: "Integrate",
            Phase.SIMPLIFICATION: "Simplify",
        }
        meaning = meaning_map.get(orientation, "Observe")

        return OperationalMeaning(orientation=orientation, meaning=meaning)

    # === 5. Projection (Runtime Activity) ===
    def _project(self, meaning: OperationalMeaning) -> OperationalField:
        """Instantiate consequences."""
        # Determine active cycles
        active_cycles = ["solar"]
        if meaning.orientation in [Phase.ACCUMULATION, Phase.EXPRESSION]:
            active_cycles.append("lunar")

        # Determine transitions
        transitions = {"next": "3.0 days", "type": "phase_shift"}

        # Determine participation surfaces
        surfaces = []
        if meaning.orientation == Phase.ACCUMULATION:
            surfaces.append("new_moon")
        elif meaning.orientation == Phase.EXPRESSION:
            surfaces.append("full_moon")

        # Determine persistence horizons
        horizons = {"immediate": "day", "medium": "lunar", "long": "seasonal"}

        # Calibration state
        calibration = {"drift": 0.02, "adjustment": "none"}

        # Reconstructive integrity
        integrity = 0.97

        return OperationalField(
            orientation=meaning.orientation,
            active_cycles=active_cycles,
            transitions=transitions,
            participation_surfaces=surfaces,
            persistence_horizons=horizons,
            calibration_state=calibration,
            reconstructive_integrity=integrity,
        )

    # === Complete Reconstruction Pipeline ===
    def reconstruct(self, observations: RawObservation) -> OperationalField:
        """Complete reconstruction pipeline."""
        distinctions = self._recognize(observations)
        categories = self._classify(distinctions)
        meaning = self._interpret(categories)
        field = self._project(meaning)
        return field

    # === Permit Participation ===
    def field(self) -> Optional[OperationalField]:
        """Expose the operational field."""
        return self._field

    def update(self):
        """Update the engine: observe, reconstruct, store."""
        obs = self.observe()
        self._field = self.reconstruct(obs)
        for callback in self._callbacks:
            callback(self._field)

    # === Maintain Continuity ===
    def persist(self, filepath: str = "calendar_state.pkl") -> None:
        """Preserve state for continuity."""
        if self._field is None:
            return
        with open(filepath, "wb") as f:
            pickle.dump(
                {
                    "field": self._field,
                    "latitude": self.latitude,
                    "longitude": self.longitude,
                    "timestamp": datetime.now(),
                },
                f,
            )

    def recover(
        self, filepath: str = "calendar_state.pkl"
    ) -> Optional[OperationalField]:
        """Recover state after discontinuity."""
        try:
            with open(filepath, "rb") as f:
                data = pickle.load(f)
                self._field = data["field"]
                self.latitude = data.get("latitude", self.latitude)
                self.longitude = data.get("longitude", self.longitude)
                return self._field
        except FileNotFoundError:
            return None

    # === Support Re-entry ===
    def schedule(self, interval: float, callback: Callable) -> None:
        """Schedule recurring re-entry."""
        self._callbacks.append(callback)
        self._schedule_loop(interval, callback)

    def _schedule_loop(self, interval: float, callback: Callable):
        if not self._running:
            return
        self._scheduler.enter(interval, 1, self._schedule_loop, (interval, callback))
        self._scheduler.enter(0, 1, callback, (self._field,))
        self._scheduler.run()

    def start(self):
        """Start the engine."""
        self._running = True
        self.update()
        self._scheduler.run()

    def stop(self):
        """Stop the engine."""
        self._running = False

    # === Preserve Reconstructability ===
    def specification(self) -> Dict[str, Any]:
        """Return the frozen specification embedded in the artifact."""
        return {
            "ecology": {
                "classification_schema": "frozen",
                "affordances": "frozen",
                "contracts": "frozen",
            },
            "grammar": {
                "acquire_observer_position": "frozen",
                "establish_operational_field": "frozen",
                "permit_participation": "frozen",
                "maintain_continuity": "frozen",
                "support_re_entry": "frozen",
                "preserve_reconstructability": "frozen",
            },
            "specification": {
                "observe": "frozen",
                "reconstruct": "frozen",
                "field": "frozen",
                "persist": "frozen",
                "recover": "frozen",
                "schedule": "frozen",
            },
            "composition": {
                "ecology": "frozen",
                "input": "frozen",
                "runtime": "frozen",
                "field": "frozen",
                "participation": "frozen",
            },
            "contracts": {
                "continuity": "frozen",
                "recurrence": "frozen",
                "directionality": "frozen",
                "reachability": "frozen",
                "persistence": "frozen",
                "reconstructive_integrity": "frozen",
            },
        }
