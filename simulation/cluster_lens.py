"""
Galaxy Cluster Lens Simulation Runner
=====================================
"""

from typing import Dict, Any
import numpy as np
from physics.mass_profiles import GalaxyClusterProfile
from simulation.source_models import GaussianSource, SersicSource
from simulation.ray_tracing import RayTracingEngine


class ClusterLensSimulation:
    def __init__(self,
                 cluster_theta_e: float = 8.0,
                 core_radius: float = 2.5,
                 source_x: float = 1.0,
                 source_y: float = 0.5,
                 source_radius: float = 0.4,
                 resolution: int = 160):
        self.cluster_theta_e = float(cluster_theta_e)
        self.core_radius = float(core_radius)
        self.source_x = float(source_x)
        self.source_y = float(source_y)
        self.source_radius = float(source_radius)
        self.resolution = int(resolution)

    def run(self) -> Dict[str, Any]:
        profile = GalaxyClusterProfile(
            cluster_theta_e=self.cluster_theta_e,
            core_radius=self.core_radius
        )

        fov = max(18.0, 2.5 * self.cluster_theta_e)

        source = SersicSource(self.source_x, self.source_y, r_eff=self.source_radius, n=1.0)
        engine = RayTracingEngine(fov_arcsec=fov, resolution=self.resolution)
        results = engine.simulate(profile, source)

        results.update({
            "model_type": "galaxy_cluster",
            "cluster_theta_e": self.cluster_theta_e,
            "core_radius": self.core_radius,
            "galaxies": profile.galaxies
        })
        return results

