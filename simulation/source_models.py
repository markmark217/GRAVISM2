"""
Source Models for Background Lensed Objects
===========================================

Models intrinsic surface brightness of background sources (quasars, galaxies, stars):
- Gaussian profile
- Sersic galaxy profile
- Uniform disk
- Point source
"""

from typing import Tuple, Union
import numpy as np


class SourceModel:
    """Base class for background source surface brightness."""
    def brightness(self, beta_x: np.ndarray, beta_y: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class GaussianSource(SourceModel):
    """
    2D circular or elliptical Gaussian light source.
    """
    def __init__(self, x0: float = 0.0, y0: float = 0.0, sigma: float = 0.2,
                 intensity: float = 1.0, ellipticity: float = 0.0, theta_deg: float = 0.0):
        self.x0 = float(x0)
        self.y0 = float(y0)
        self.sigma = float(max(1e-4, sigma))
        self.intensity = float(intensity)
        self.ellipticity = float(ellipticity)
        self.phi_rad = np.radians(theta_deg)

    def brightness(self, beta_x: np.ndarray, beta_y: np.ndarray) -> np.ndarray:
        dx = beta_x - self.x0
        dy = beta_y - self.y0
        # Rotate coordinates if elliptical
        cos_p = np.cos(self.phi_rad)
        sin_p = np.sin(self.phi_rad)
        xp = dx * cos_p + dy * sin_p
        yp = -dx * sin_p + dy * cos_p

        q = max(0.1, 1.0 - self.ellipticity)
        r_sq = xp**2 + (yp / q)**2
        return self.intensity * np.exp(-0.5 * r_sq / (self.sigma**2))


class SersicSource(SourceModel):
    """
    Sersic profile representing an elliptical or spiral galaxy.
    n=1: Exponential disk (spiral)
    n=4: de Vaucouleurs profile (elliptical)
    """
    def __init__(self, x0: float = 0.0, y0: float = 0.0, r_eff: float = 0.4,
                 n: float = 1.0, intensity: float = 1.0):
        self.x0 = float(x0)
        self.y0 = float(y0)
        self.r_eff = float(max(1e-4, r_eff))
        self.n = float(n)
        self.intensity = float(intensity)
        # b_n approximation: b_n ~ 2n - 1/3 + 4/(405n)
        self.b_n = 2.0 * self.n - 0.333333 + 0.009876 / self.n

    def brightness(self, beta_x: np.ndarray, beta_y: np.ndarray) -> np.ndarray:
        r = np.hypot(beta_x - self.x0, beta_y - self.y0)
        return self.intensity * np.exp(-self.b_n * ((r / self.r_eff)**(1.0 / self.n) - 1.0))


class UniformDiskSource(SourceModel):
    """Uniform brightness disk of radius R."""
    def __init__(self, x0: float = 0.0, y0: float = 0.0, radius: float = 0.3,
                 intensity: float = 1.0):
        self.x0 = float(x0)
        self.y0 = float(y0)
        self.radius = float(max(1e-4, radius))
        self.intensity = float(intensity)

    def brightness(self, beta_x: np.ndarray, beta_y: np.ndarray) -> np.ndarray:
        r = np.hypot(beta_x - self.x0, beta_y - self.y0)
        return np.where(r <= self.radius, self.intensity, 0.0)

