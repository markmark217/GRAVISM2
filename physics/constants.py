"""
GRAVISIM: Fundamental Physical and Astronomical Constants
=========================================================

Standard physical constants and conversion factors used throughout
the gravitational lensing simulation. Values follow CODATA 2022 / IAU recommendations.
"""

import math

# Fundamental Physical Constants (SI Units)
# Gravitational constant [m^3 kg^-1 s^-2]
G: float = 6.67430e-11

# Speed of light in vacuum [m s^-1]
C: float = 299792458.0
C_SQ: float = C * C

# Astronomical Units
# Solar mass [kg]
M_SUN: float = 1.98847e30

# Astronomical Unit [m]
AU: float = 1.495978707e11

# Parsec [m]
PARSEC: float = 3.0856775814913673e16

# Megaparsec [m]
MPC: float = 1e6 * PARSEC

# Kiloparsec [m]
KPC: float = 1e3 * PARSEC

# Angular Conversions
# Radians to Arcseconds: (180 * 3600) / pi
RAD_TO_ARCSEC: float = (180.0 * 3600.0) / math.pi  # ~ 206264.80624709636
ARCSEC_TO_RAD: float = 1.0 / RAD_TO_ARCSEC

# Radians to Degrees
RAD_TO_DEG: float = 180.0 / math.pi
DEG_TO_RAD: float = math.pi / 180.0

# Arcseconds to Degrees
ARCSEC_TO_DEG: float = 1.0 / 3600.0
DEG_TO_ARCSEC: float = 3600.0

# Cosmological Defaults (Planck / Flat Lambda-CDM)
DEFAULT_H0: float = 70.0  # [km s^-1 Mpc^-1]
DEFAULT_OMEGA_M: float = 0.3
DEFAULT_OMEGA_LAMBDA: float = 0.7

