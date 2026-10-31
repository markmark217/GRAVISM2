"""
Spacetime Curvature 3D Potential Well Surface
============================================

Generates a 3D deformed surface visualizing gravitational potential wells.
Includes explicit scientific disclaimers regarding the rubber-sheet analogy.
"""

from typing import Dict, Any, List
import numpy as np
import plotly.graph_objects as go


def generate_spacetime_surface(mass_solar: float = 1e11,
                               model_type: str = "point_mass",
                               grid_size: int = 50,
                               radius: float = 8.0) -> go.Figure:
    """
    Generate 3D potential surface using Plotly 3D Surface.
    """
    x = np.linspace(-radius, radius, grid_size)
    y = np.linspace(-radius, radius, grid_size)
    xx, yy = np.meshgrid(x, y)

    # Gravitational potential depth
    if model_type == "binary":
        # Two mass wells
        d1 = np.hypot(xx + 2.0, yy)
        d2 = np.hypot(xx - 2.0, yy)
        z = -3.0 / np.sqrt(d1**2 + 0.6) - 3.0 / np.sqrt(d2**2 + 0.6)
    elif model_type == "cluster":
        # Broad cluster well + subhalos
        r_main = np.hypot(xx, yy)
        z = -4.0 / np.sqrt(r_main**2 + 4.0)
        # Add 3 galaxy subhalos
        for gx, gy in [(-3, 2), (2.5, -2), (1, 3)]:
            dg = np.hypot(xx - gx, yy - gy)
            z -= 1.2 / np.sqrt(dg**2 + 0.3)
    else:
        # Standard point mass / central galaxy
        r = np.hypot(xx, yy)
        # Depth scaled by log(mass_solar)
        scale = max(1.0, np.log10(mass_solar) - 8.0)
        z = -scale * 1.5 / np.sqrt(r**2 + 0.8)

    fig = go.Figure(data=[
        go.Surface(
            x=xx, y=yy, z=z,
            colorscale=[[0, "#0b0f29"], [0.4, "#2E3A8C"], [0.8, "#4A5FD9"], [1.0, "#00FFAA"]],
            showscale=False,
            contours_z=dict(show=True, usecolormap=True, highlightcolor="#FFFFFF", project_z=True)
        )
    ])

    fig.update_layout(
        title="3D Conceptual Spacetime Curvature (Potential Well)",
        template="plotly_dark",
        paper_bgcolor="#1A2254",
        font=dict(family="Inter, sans-serif", color="#FFFFFF"),
        scene=dict(
            xaxis_title="X (kpc / arcsec)",
            yaxis_title="Y (kpc / arcsec)",
            zaxis_title="Gravitational Potential (Phi / c^2)",
            bgcolor="#0b0f29",
            camera=dict(eye=dict(x=1.5, y=-1.5, z=1.2))
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        height=550
    )

    return fig

