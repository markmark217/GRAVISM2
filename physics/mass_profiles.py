"""
Mass Profiles for Gravitational Lensing
=======================================

Implements analytical and numerical mass distributions:
1. Point Mass
2. Singular Isothermal Sphere (SIS)
3. Singular Isothermal Ellipsoid (SIE) / Elliptical Galaxy Lens
4. Binary Point-Mass Lens
5. Galaxy Cluster Model (Main cluster halo + cluster subhalos)
6. Navarro-Frenk-White (NFW) Profile
"""

from typing import Tuple, Dict, Any, List
import numpy as np


class PointMassProfile:
    """Point mass lens at (x_0, y_0) with Einstein radius theta_e."""

    def __init__(self, theta_e: float, x_0: float = 0.0, y_0: float = 0.0):
        self.theta_e = float(theta_e)
        self.x_0 = float(x_0)
        self.y_0 = float(y_0)

    def deflection(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        dx = x - self.x_0
        dy = y - self.y_0
        r_sq = dx**2 + dy**2
        safe_r_sq = np.where(r_sq < 1e-14, 1e-14, r_sq)
        factor = (self.theta_e**2) / safe_r_sq
        return factor * dx, factor * dy

    def potential(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        dx = x - self.x_0
        dy = y - self.y_0
        r = np.hypot(dx, dy)
        safe_r = np.where(r < 1e-14, 1e-14, r)
        return (self.theta_e**2) * np.log(safe_r / self.theta_e)


class SISProfile:
    """Singular Isothermal Sphere (SIS) profile."""

    def __init__(self, theta_e: float, x_0: float = 0.0, y_0: float = 0.0):
        self.theta_e = float(theta_e)
        self.x_0 = float(x_0)
        self.y_0 = float(y_0)

    def deflection(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        dx = x - self.x_0
        dy = y - self.y_0
        r = np.hypot(dx, dy)
        safe_r = np.where(r < 1e-14, 1e-14, r)
        factor = self.theta_e / safe_r
        return factor * dx, factor * dy

    def convergence(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        dx = x - self.x_0
        dy = y - self.y_0
        r = np.hypot(dx, dy)
        safe_r = np.where(r < 1e-14, 1e-14, r)
        return 0.5 * self.theta_e / safe_r


class SIEProfile:
    """
    Singular Isothermal Ellipsoid (SIE) profile.
    Uses Kormann, Schneider, Bartelmann (1994) formulation.
    q: axis ratio (minor / major axis, 0 < q <= 1).
    phi_deg: position angle of major axis in degrees.
    """

    def __init__(self, theta_e: float, q: float = 0.8, phi_deg: float = 0.0,
                 x_0: float = 0.0, y_0: float = 0.0):
        self.theta_e = float(theta_e)
        self.q = float(np.clip(q, 0.05, 0.99999))
        self.phi_rad = np.radians(phi_deg)
        self.x_0 = float(x_0)
        self.y_0 = float(y_0)

    def deflection(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        # Shift and rotate into lens coordinate system
        dx = x - self.x_0
        dy = y - self.y_0
        cos_p = np.cos(self.phi_rad)
        sin_p = np.sin(self.phi_rad)
        xp = dx * cos_p + dy * sin_p
        yp = -dx * sin_p + dy * cos_p

        q = self.q
        f = np.sqrt(1.0 - q**2)

        # Elliptical radius psi
        psi = np.sqrt(q**2 * xp**2 + yp**2)
        safe_psi = np.where(psi < 1e-12, 1e-12, psi)

        # Deflection in aligned frame
        # alpha_x = (theta_E * sqrt(q) / f) * arcsin(f * xp / psi)
        # alpha_y = (theta_E * sqrt(q) / f) * arcsinh(f * yp / (q * safe_psi))
        arg_x = np.clip(f * xp / safe_psi, -0.999999, 0.999999)
        alpha_xp = (self.theta_e * np.sqrt(q) / f) * np.arcsin(arg_x)

        # arcsinh(u) = log(u + sqrt(u^2 + 1))
        arg_y = f * yp / safe_psi
        alpha_yp = (self.theta_e * np.sqrt(q) / f) * np.arcsinh(arg_y / q)

        # Rotate back to original frame
        alpha_x = alpha_xp * cos_p - alpha_yp * sin_p
        alpha_y = alpha_xp * sin_p + alpha_yp * cos_p
        return alpha_x, alpha_y


class BinaryLensProfile:
    """
    Binary point-mass lens model.
    m1, m2: mass fractions (m1 + m2 = 1.0).
    sep: separation between masses in angular units (e.g. arcsec).
    q_mass: mass ratio m2 / m1.
    """

    def __init__(self, total_theta_e: float, separation: float, q_mass: float = 1.0,
                 angle_deg: float = 0.0, center_x: float = 0.0, center_y: float = 0.0):
        self.theta_e = float(total_theta_e)
        self.sep = float(separation)
        self.q_mass = float(q_mass)
        self.angle_rad = np.radians(angle_deg)
        self.center_x = float(center_x)
        self.center_y = float(center_y)

        # Mass fractions
        self.m1 = 1.0 / (1.0 + self.q_mass)
        self.m2 = self.q_mass / (1.0 + self.q_mass)

        # Positions of masses
        half_d = 0.5 * self.sep
        cos_a = np.cos(self.angle_rad)
        sin_a = np.sin(self.angle_rad)
        self.x1 = self.center_x - half_d * cos_a
        self.y1 = self.center_y - half_d * sin_a
        self.x2 = self.center_x + half_d * cos_a
        self.y2 = self.center_y + half_d * sin_a

    def deflection(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        # Mass 1 contribution
        dx1 = x - self.x1
        dy1 = y - self.y1
        r1_sq = dx1**2 + dy1**2
        safe_r1 = np.where(r1_sq < 1e-14, 1e-14, r1_sq)
        f1 = (self.m1 * self.theta_e**2) / safe_r1

        # Mass 2 contribution
        dx2 = x - self.x2
        dy2 = y - self.y2
        r2_sq = dx2**2 + dy2**2
        safe_r2 = np.where(r2_sq < 1e-14, 1e-14, r2_sq)
        f2 = (self.m2 * self.theta_e**2) / safe_r2

        alpha_x = f1 * dx1 + f2 * dx2
        alpha_y = f1 * dy1 + f2 * dy2
        return alpha_x, alpha_y


class GalaxyClusterProfile:
    """
    Galaxy cluster lens composed of a main cluster halo (smooth isothermal core)
    plus discrete galaxy subhalos.
    """

    def __init__(self, cluster_theta_e: float, core_radius: float = 2.0,
                 subhalo_fraction: float = 0.25):
        self.cluster_theta_e = float(cluster_theta_e)
        self.core_radius = float(core_radius)
        self.subhalo_fraction = float(subhalo_fraction)

        # Predefine representative cluster galaxies
        self.galaxies = [
            {"x": -4.0, "y": 2.5, "theta_e": cluster_theta_e * 0.15},
            {"x": 3.5, "y": -3.0, "theta_e": cluster_theta_e * 0.18},
            {"x": 1.5, "y": 4.0, "theta_e": cluster_theta_e * 0.12},
            {"x": -2.0, "y": -4.5, "theta_e": cluster_theta_e * 0.14},
            {"x": 0.0, "y": 0.0, "theta_e": cluster_theta_e * 0.25}  # BCG (Brightest Cluster Galaxy)
        ]

    def deflection(self, x: np.ndarray, y: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        # Main cluster halo deflection (pseudo-isothermal with core)
        r = np.hypot(x, y)
        safe_r = np.where(r < 1e-14, 1e-14, r)
        # alpha_main = theta_E * (sqrt(r^2 + r_core^2) - r_core) / r
        alpha_mag = self.cluster_theta_e * (np.sqrt(r**2 + self.core_radius**2) - self.core_radius) / safe_r
        alpha_x = alpha_mag * (x / safe_r)
        alpha_y = alpha_mag * (y / safe_r)

        # Add subhalos
        for gal in self.galaxies:
            gx = gal["x"]
            gy = gal["y"]
            gte = gal["theta_e"]
            dx = x - gx
            dy = y - gy
            gr = np.hypot(dx, dy)
            safe_gr = np.where(gr < 1e-14, 1e-14, gr)
            factor = gte / safe_gr
            alpha_x += factor * dx
            alpha_y += factor * dy

        return alpha_x, alpha_y

