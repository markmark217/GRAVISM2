"""
Numerical Null Geodesic Integrator in Schwarzschild Spacetime
============================================================

Integrates the general relativistic equations of motion for light rays (null geodesics)
orbiting or falling into a Schwarzschild black hole.

Equation of motion (in dimensionless units where r_s = 1):
    d^2 u / dphi^2 + u = 1.5 * r_s * u^2
where u = 1 / r.
"""

from typing import Dict, Any, List, Tuple
import math
import numpy as np
from scipy.integrate import solve_ivp
from relativity.schwarzschild import (
    schwarzschild_radius_m,
    photon_sphere_radius_m,
    critical_impact_parameter_m
)


def integrate_null_geodesic(b_over_rs: float,
                            r_init_over_rs: float = 30.0,
                            max_phi: float = 8.0 * math.pi,
                            rtol: float = 1e-8,
                            atol: float = 1e-10) -> Dict[str, Any]:
    """
    Integrate a single photon trajectory approaching from r_init with impact parameter b.
    All distance quantities are normalized by the Schwarzschild radius r_s (i.e., r_s = 1).

    Parameters:
        b_over_rs: Impact parameter b / r_s.
        r_init_over_rs: Starting radius r_init / r_s.
        max_phi: Maximum angular progression before terminating.

    Returns:
        Dict containing:
            b: impact parameter
            status: 'captured' | 'escaped' | 'orbiting'
            r: array of radial distances
            phi: array of angles
            x: array of Cartesian x coordinates
            y: array of Cartesian y coordinates
            deflection_rad: total light deflection angle (escaped only)
            r_min: closest approach distance reached
    """
    u_0 = 1.0 / r_init_over_rs
    b = float(b_over_rs)

    # From conservation law: (du/dphi)^2 = 1/b^2 - u^2 + u^3 (since r_s = 1)
    val = (1.0 / b**2) - u_0**2 + u_0**3
    if val < 0.0:
        val = 0.0
    v_0 = math.sqrt(val)  # Positive: u = 1/r is increasing as photon approaches black hole

    # Initial state: y = [u, du/dphi]
    y0 = [u_0, v_0]

    def ode(phi, y):
        u, v = y
        # d^2u/dphi^2 = 1.5 * u^2 - u
        dudphi = v
        dvdphi = 1.5 * (u**2) - u
        return [dudphi, dvdphi]

    # Termination events
    def event_horizon(phi, y):
        # u = 1 corresponds to r = r_s
        return y[0] - 1.0
    event_horizon.terminal = True
    event_horizon.direction = 1

    def infinity(phi, y):
        # Escaping back to infinity: u <= 1e-4 and moving outward (v < 0)
        return y[0] - 1e-4
    infinity.terminal = True
    infinity.direction = -1

    sol = solve_ivp(
        ode,
        t_span=(0.0, max_phi),
        y0=y0,
        events=[event_horizon, infinity],
        dense_output=True,
        max_step=0.02,
        rtol=rtol,
        atol=atol
    )

    phi_arr = sol.t
    u_arr = sol.y[0]
    # Filter out any non-positive u
    safe_u = np.maximum(u_arr, 1e-6)
    r_arr = 1.0 / safe_u

    # Determine status
    if len(sol.t_events[0]) > 0:
        status = "captured"
        deflection_rad = None
    elif len(sol.t_events[1]) > 0:
        status = "escaped"
        # Total angular change delta_phi
        delta_phi = phi_arr[-1] - phi_arr[0]
        # Deflection angle is total deflection minus straight line (pi)
        deflection_rad = float(delta_phi - math.pi)
    else:
        status = "orbiting"
        deflection_rad = None

    r_min = float(np.min(r_arr))

    # Convert (r, phi) to Cartesian (x, y) coordinates
    # Orient so photon starts at x = -sqrt(r_init^2 - b^2), y = b
    # Angle offset: initially, tan(phi_0) = b / (-x)
    phi_offset = math.pi - math.asin(np.clip(b / r_init_over_rs, -1.0, 1.0))
    polar_angle = phi_arr + phi_offset

    x_arr = r_arr * np.cos(polar_angle)
    y_arr = r_arr * np.sin(polar_angle)

    return {
        "b_over_rs": b,
        "status": status,
        "phi": phi_arr,
        "r": r_arr,
        "x": x_arr,
        "y": y_arr,
        "r_min": r_min,
        "deflection_rad": deflection_rad
    }


def trace_bundle_geodesics(impact_parameters: List[float],
                           r_init_over_rs: float = 30.0) -> List[Dict[str, Any]]:
    """
    Trace multiple geodesics for a range of impact parameters to visualize
    strong lensing, shadow, and relativistic rings.
    """
    results = []
    for b in impact_parameters:
        res = integrate_null_geodesic(b, r_init_over_rs=r_init_over_rs)
        results.append(res)
    return results
