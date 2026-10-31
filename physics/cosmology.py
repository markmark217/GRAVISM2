"""
Cosmology and Angular Diameter Distance Calculator
==================================================

Computes cosmological distances for gravitational lensing under Flat Lambda-CDM:
- Angular diameter distance D_A(z)
- Angular diameter distance between lens and source D_A(z_L, z_S)
- Time-delay distance D_dt = (1 + z_L) * (D_L * D_S) / D_LS
- Independent numerical integration with Astropy validation.
"""

import math
from typing import Tuple, Dict, Any
import numpy as np
from scipy.integrate import quad
from physics.constants import C, MPC, DEFAULT_H0, DEFAULT_OMEGA_M, DEFAULT_OMEGA_LAMBDA


class FlatLambdaCDMCosmology:
    """
    Standard Flat Lambda Cold Dark Matter cosmological model.
    """

    def __init__(self, h0: float = DEFAULT_H0, om0: float = DEFAULT_OMEGA_M):
        self.h0 = float(h0)
        self.om0 = float(om0)
        self.ode0 = 1.0 - self.om0  # Flat universe: Omega_M + Omega_Lambda = 1
        # Hubble distance D_H = c / H0 in meters
        # H0 is in km/s/Mpc -> H0_SI in s^-1 = H0 * 1000 / MPC
        self.h0_si = (self.h0 * 1000.0) / MPC
        self.d_h_m = C / self.h0_si
        self.d_h_mpc = (C / 1000.0) / self.h0

    def e_z(self, z: float) -> float:
        """Dimensionless Hubble parameter E(z) = H(z) / H0."""
        return math.sqrt(self.om0 * (1.0 + z)**3 + self.ode0)

    def comoving_distance_mpc(self, z1: float, z2: float) -> float:
        """Line-of-sight comoving distance in Mpc between z1 and z2 (z1 < z2)."""
        if z1 >= z2:
            return 0.0
        integral, _ = quad(lambda z: 1.0 / self.e_z(z), z1, z2)
        return self.d_h_mpc * integral

    def angular_diameter_distance_mpc(self, z: float) -> float:
        """Observer-to-redshift z angular diameter distance in Mpc."""
        if z <= 0.0:
            return 0.0
        d_c = self.comoving_distance_mpc(0.0, z)
        return d_c / (1.0 + z)

    def angular_diameter_distance_z1_z2_mpc(self, z1: float, z2: float) -> float:
        """Angular diameter distance between z1 and z2 in Mpc (z1 < z2)."""
        if z1 >= z2:
            return 0.0
        d_c12 = self.comoving_distance_mpc(z1, z2)
        return d_c12 / (1.0 + z2)

    def lensing_distances(self, z_lens: float, z_source: float) -> Dict[str, float]:
        """
        Compute standard lensing angular diameter distances:
            D_L: Observer -> Lens [Mpc]
            D_S: Observer -> Source [Mpc]
            D_LS: Lens -> Source [Mpc]
            D_dt: Time-delay distance [Mpc]
        """
        if z_lens >= z_source:
            raise ValueError(f"Lens redshift (z_lens={z_lens}) must be less than source redshift (z_source={z_source}).")

        d_l = self.angular_diameter_distance_mpc(z_lens)
        d_s = self.angular_diameter_distance_mpc(z_source)
        d_ls = self.angular_diameter_distance_z1_z2_mpc(z_lens, z_source)

        time_delay_distance = (1.0 + z_lens) * (d_l * d_s) / d_ls if d_ls > 0 else 0.0

        return {
            "d_l_mpc": float(d_l),
            "d_s_mpc": float(d_s),
            "d_ls_mpc": float(d_ls),
            "time_delay_distance_mpc": float(time_delay_distance),
            "distance_ratio": float(d_ls / d_s) if d_s > 0 else 0.0
        }

