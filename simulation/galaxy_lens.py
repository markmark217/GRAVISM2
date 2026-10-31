"""
Galaxy Lens Simulation Runner (SIS and SIE Models)
==================================================
"""

from typing import Dict, Any
import numpy as np
from physics.mass_profiles import SISProfile, SIEProfile
from physics.einstein_radius import sis_einstein_radius_arcsec
from simulation.source_models import GaussianSource, SersicSource
from simulation.ray_tracing import RayTracingEngine


class GalaxyLensSimulation:
    def __init__(self,
                 is_elliptical: bool = True,
                 theta_e_arcsec: float = 1.5,
                 velocity_dispersion_kms: float = 220.0,
                 d_ls_mpc: float = 1000.0,
                 d_s_mpc: float = 2000.0,
                 axis_ratio_q: float = 0.75,
                 orientation_deg: float = 30.0,
                 source_x: float = 0.3,
                 source_y: float = 0.2,
                 source_radius: float = 0.15,
                 resolution: int = 160):
        self.is_elliptical = is_elliptical
        self.velocity_dispersion_kms = float(velocity_dispersion_kms)
        self.d_ls_mpc = float(d_ls_mpc)
        self.d_s_mpc = float(d_s_mpc)
        self.axis_ratio_q = float(axis_ratio_q)
        self.orientation_deg = float(orientation_deg)
        self.source_x = float(source_x)
        self.source_y = float(source_y)
        self.source_radius = float(source_radius)
        self.resolution = int(resolution)

        if theta_e_arcsec > 0:
            self.theta_e_arcsec = float(theta_e_arcsec)
        else:
            self.theta_e_arcsec = float(sis_einstein_radius_arcsec(
                self.velocity_dispersion_kms, self.d_ls_mpc, self.d_s_mpc
            ))

    def run(self) -> Dict[str, Any]:
        if self.is_elliptical:
            profile = SIEProfile(
                theta_e=self.theta_e_arcsec,
                q=self.axis_ratio_q,
                phi_deg=self.orientation_deg
            )
            model_type = "sie_galaxy"
        else:
            profile = SISProfile(theta_e=self.theta_e_arcsec)
            model_type = "sis_galaxy"

        dist_src = np.hypot(self.source_x, self.source_y)
        fov = max(5.0, 3.5 * max(self.theta_e_arcsec, dist_src))

        source = SersicSource(self.source_x, self.source_y, r_eff=self.source_radius, n=1.0)
        engine = RayTracingEngine(fov_arcsec=fov, resolution=self.resolution)
        results = engine.simulate(profile, source)

        results.update({
            "model_type": model_type,
            "theta_e_arcsec": self.theta_e_arcsec,
            "is_elliptical": self.is_elliptical,
            "axis_ratio_q": self.axis_ratio_q,
            "orientation_deg": self.orientation_deg,
            "source_pos": (self.source_x, self.source_y)
        })
        return results

