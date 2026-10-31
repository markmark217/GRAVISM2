"""
Optical Bench Light Path Visualizations
======================================

Visualizes the 2D optical bench geometry:
- Observer position at z = 0
- Lens plane at z = D_L
- Source plane at z = D_S
- Straight-line unlensed path vs deflected light rays
- Deflection angle alpha_hat and reduced angle alpha
"""

from typing import Dict, Any, List
import numpy as np
import plotly.graph_objects as go


def plot_optical_bench_rays(d_l: float, d_s: float, beta_arcsec: float,
                            theta_e_arcsec: float, theta_plus: float, theta_minus: float):
    """
    Generate an interactive Plotly diagram of the optical bench light rays.
    """
    fig = go.Figure()

    # Optical Axis (z from 0 to d_s)
    fig.add_trace(go.Scatter(
        x=[0, d_s * 1.1], y=[0, 0],
        mode="lines",
        line=dict(color="#888888", width=1.5, dash="dash"),
        name="Optical Axis"
    ))

    # Observer (z=0, y=0)
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode="markers+text",
        marker=dict(size=14, color="#FFFFFF", symbol="circle"),
        text=["Observer"],
        textposition="bottom left",
        name="Observer"
    ))

    # Lens Plane (z = d_l)
    y_max = max(abs(theta_plus), abs(theta_minus), abs(beta_arcsec), theta_e_arcsec) * 1.6
    fig.add_trace(go.Scatter(
        x=[d_l, d_l], y=[-y_max, y_max],
        mode="lines",
        line=dict(color="#4A5FD9", width=1, dash="dot"),
        name="Lens Plane"
    ))
    # Lens Object
    fig.add_trace(go.Scatter(
        x=[d_l], y=[0],
        mode="markers+text",
        marker=dict(size=14, color="#FFD700", symbol="star"),
        text=["Lens Mass"],
        textposition="top right",
        name="Lens"
    ))

    # Source Plane (z = d_s)
    fig.add_trace(go.Scatter(
        x=[d_s, d_s], y=[-y_max, y_max],
        mode="lines",
        line=dict(color="#2E3A8C", width=1, dash="dot"),
        name="Source Plane"
    ))
    # Source Object
    fig.add_trace(go.Scatter(
        x=[d_s], y=[beta_arcsec],
        mode="markers+text",
        marker=dict(size=12, color="#FF4B4B", symbol="diamond"),
        text=[f"Source (beta={beta_arcsec:.2f}\")"],
        textposition="top right",
        name="Source"
    ))

    # Primary Image Ray (Source -> Lens at theta_plus * D_L / D_S? In angular coordinates):
    # From observer to lens at impact parameter y = theta_plus, then from lens to source at beta!
    # Ray 1: Observer(0,0) -> Lens(d_l, theta_plus) -> Source(d_s, beta)
    fig.add_trace(go.Scatter(
        x=[0, d_l, d_s],
        y=[0, theta_plus, beta_arcsec],
        mode="lines",
        line=dict(color="#00FFAA", width=2.5),
        name=f"Primary Ray (theta_+ = {theta_plus:.2f}\")"
    ))
    # Apparent straight line back projection
    fig.add_trace(go.Scatter(
        x=[d_l, d_s],
        y=[theta_plus, theta_plus * (d_s / d_l)],
        mode="lines",
        line=dict(color="#00FFAA", width=1.5, dash="dot"),
        name="Apparent Direction (+)"
    ))

    # Secondary Image Ray:
    # Observer(0,0) -> Lens(d_l, theta_minus) -> Source(d_s, beta)
    fig.add_trace(go.Scatter(
        x=[0, d_l, d_s],
        y=[0, theta_minus, beta_arcsec],
        mode="lines",
        line=dict(color="#FF8800", width=2.5),
        name=f"Secondary Ray (theta_- = {theta_minus:.2f}\")"
    ))
    # Apparent straight line back projection
    fig.add_trace(go.Scatter(
        x=[d_l, d_s],
        y=[theta_minus, theta_minus * (d_s / d_l)],
        mode="lines",
        line=dict(color="#FF8800", width=1.5, dash="dot"),
        name="Apparent Direction (-)"
    ))

    # Einstein radius marker on lens plane
    fig.add_trace(go.Scatter(
        x=[d_l, d_l],
        y=[-theta_e_arcsec, theta_e_arcsec],
        mode="markers",
        marker=dict(size=8, color="#4A5FD9", symbol="line-ew"),
        name=f"Einstein Radius (+/- {theta_e_arcsec:.2f}\")"
    ))

    fig.update_layout(
        title="2D Gravitational Optical Bench Geometry",
        template="plotly_dark",
        paper_bgcolor="#1A2254",
        plot_bgcolor="#0b0f29",
        font=dict(family="Inter, sans-serif", color="#FFFFFF"),
        xaxis_title="Distance along Line of Sight (Mpc)",
        yaxis_title="Angular Scale / Impact Position (arcsec)",
        height=450,
        margin=dict(l=40, r=40, t=50, b=40)
    )

    return fig

