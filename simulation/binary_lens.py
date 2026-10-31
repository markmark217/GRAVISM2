"""
Binary Lens Simulation Runner
=============================
"""

from typing import Dict, Any
import numpy as np
from physics.mass_profiles import BinaryLensProfile
from simulation.source_models import GaussianSource
from simulation.ray_tracing import RayTracingEngine


class BinaryLensSimulation:
    def __init__(self,
                 total_theta_e: float = 2.0,
                 separation: float = 2.2,
                 mass_ratio: float = 1.0,
                 angle_deg: float = 0.0,
                 source_x: float = 0.2,
                 source_y: float = 0.1,
                 source_radius: float = 0.15,
                 resolution: int = 160):
        self.total_theta_e = float(total_theta_e)
        self.separation = float(separation)
        self.mass_ratio = float(mass_ratio)
        self.angle_deg = float(angle_deg)
        self.source_x = float(source_x)
        self.source_y = float(source_y)
        self.source_radius = float(source_radius)
        self.resolution = int(resolution)

    def run(self) -> Dict[str, Any]:
        profile = BinaryLensProfile(
            total_theta_e=self.total_theta_e,
            separation=self.separation,
            q_mass=self.mass_ratio,
            angle_deg=self.angle_deg
        )

        fov = max(6.0, 2.5 * max(self.total_theta_e, self.separation))

        source = GaussianSource(self.source_x, self.source_y, sigma=self.source_radius)
        engine = RayTracingEngine(fov_arcsec=fov, resolution=self.resolution)
        results = engine.simulate(profile, source)

        results.update({
            "model_type": "binary_lens",
            "total_theta_e": self.total_theta_e,
            "separation": self.separation,
            "mass_ratio": self.mass_ratio,
            "angle_deg": self.angle_deg,
            "m1_pos": (profile.x1, profile.y1),
            "m2_pos": (profile.x2, profile.y2)
        })
        return results

