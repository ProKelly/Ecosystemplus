from dataclasses import dataclass, field
from typing import Dict

@dataclass
class FarmData:
    """Container for user-supplied farm information used in the emission calculator."""
    area_hectares: float
    season: str
    farming_method: str
    fertilizer_level: str
    livestock: Dict[str, int] = field(default_factory=dict)
    monthly_fuel_liters: float = 0.0

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------
    @property
    def has_livestock(self) -> bool:
        """Return True when the farm keeps at least one livestock animal."""
        return bool(self.livestock)

    def as_dict(self) -> Dict:
        """Return a plain-dict representation (useful for JSON serialisation)."""
        return {
            "area_hectares": self.area_hectares,
            "season": self.season,
            "farming_method": self.farming_method,
            "fertilizer_level": self.fertilizer_level,
            "livestock": self.livestock,
            "monthly_fuel_liters": self.monthly_fuel_liters,
        } 