"""
Interactive 3D Visualizations
=============================

3D light ray paths and 3D Black Hole null geodesics with event horizon and photon sphere.
"""

from typing import List, Dict, Any
import numpy as np
import plotly.graph_objects as go
from relativity.geodesics import trace_bundle_geodesics


def plot_3d_light_rays(d_l: float, d_s: float, beta_x: float, beta_y: float,
                       theta_plus: float, theta_minus: float) -> go.Figure:
    """
    3D ray trajectories from Observer (0,0,0) to Lens plane (D_L) to Source (D_S).
    """
    fig = go.Figure()

    # Observer (0, 0, 0)
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode="markers+text",
        marker=dict(size=8, color="#FFFFFF"),
        text=["Observer"],
        name="Observer"
    ))

    # Lens at (0, 0, D_L)
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[d_l],
        mode="markers+text",
        marker=dict(size=12, color="#FFD700", symbol="diamond"),
        text=["Lens Object"],
        name="Lens"
    ))

    # Source at (beta_x, beta_y, D_S)
    fig.add_trace(go.Scatter3d(
        x=[beta_x], y=[beta_y], z=[d_s],
        mode="markers+text",
        marker=dict(size=10, color="#FF4B4B"),
        text=["Source"],
        name="Source"
    ))

    # Ray 1: Observer -> (theta_plus, 0, D_L) -> (beta_x, beta_y, D_S)
    fig.add_trace(go.Scatter3d(
        x=[0, theta_plus, beta_x],
        y=[0, 0, beta_y],
        z=[0, d_l, d_s],
        mode="lines",
        line=dict(color="#00FFAA", width=4),
        name="Primary Light Ray (+)"
    ))

    # Ray 2: Observer -> (theta_minus, 0, D_L) -> (beta_x, beta_y, D_S)
    fig.add_trace(go.Scatter3d(
        x=[0, theta_minus, beta_x],
        y=[0, 0, beta_y],
        z=[0, d_l, d_s],
        mode="lines",
        line=dict(color="#FF8800", width=4),
        name="Secondary Light Ray (-)"
    ))

    # Undeflected straight ray from Source to Observer
    fig.add_trace(go.Scatter3d(
        x=[0, beta_x],
        y=[0, beta_y],
        z=[0, d_s],
        mode="lines",
        line=dict(color="#888888", width=2, dash="dash"),
        name="Straight (Unlensed) Line"
    ))

    fig.update_layout(
        title="3D Optical Ray Mapping",
        template="plotly_dark",
        paper_bgcolor="#1A2254",
        scene=dict(
            xaxis_title="X (arcsec)",
            yaxis_title="Y (arcsec)",
            zaxis_title="Line of Sight Distance Z (Mpc)",
            bgcolor="#0b0f29",
            camera=dict(eye=dict(x=-1.6, y=-1.6, z=0.8))
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        height=550
    )
    return fig


def plot_3d_black_hole_geodesics(b_values: List[float] = None) -> go.Figure:
    """
    3D visualization of Schwarzschild black hole null geodesics.
    Displays:
    - Central black hole event horizon sphere at r = r_s (black)
    - Photon sphere wireframe at r = 1.5 r_s (gold)
    - Photon trajectories colored by outcome (escaped vs captured)
    """
    if b_values is None:
        b_values = [2.0, 2.3, 2.55, 2.65, 3.0, 4.0, 6.0, 9.0]

    bundle = trace_bundle_geodesics(b_values)
    fig = go.Figure()

    # Create 3D Event Horizon Sphere (r = 1.0)
    u_s = np.linspace(0, 2 * np.pi, 30)
    v_s = np.linspace(0, np.pi, 20)
    xs = 1.0 * np.outer(np.cos(u_s), np.sin(v_s))
    ys = 1.0 * np.outer(np.sin(u_s), np.sin(v_s))
    zs = 1.0 * np.outer(np.ones(np.size(u_s)), np.cos(v_s))

    fig.add_trace(go.Surface(
        x=xs, y=ys, z=zs,
        colorscale=[[0, "#000000"], [1, "#111111"]],
        showscale=False,
        name="Event Horizon (r = r_s)"
    ))

    # Photon sphere circle (r = 1.5 in xy plane)
    th = np.linspace(0, 2 * np.pi, 100)
    fig.add_trace(go.Scatter3d(
        x=1.5 * np.cos(th),
        y=1.5 * np.sin(th),
        z=np.zeros_like(th),
        mode="lines",
        line=dict(color="#FFD700", width=3, dash="dot"),
        name="Photon Sphere (r = 1.5 r_s)"
    ))

    # Add trajectories in 3D (lying in equatorial z=0 plane or inclined)
    for ray in bundle:
        b = ray["b_over_rs"]
        x = ray["x"]
        y = ray["y"]
        z = np.zeros_like(x)
        status = ray["status"]

        color = "#00FFAA" if status == "escaped" else "#FF4B4B"
        label = f"b={b:.2f} r_s ({status})"

        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode="lines",
            line=dict(color=color, width=3),
            name=label
        ))

    fig.update_layout(
        title="3D Null Geodesics in Schwarzschild Spacetime",
        template="plotly_dark",
        paper_bgcolor="#1A2254",
        scene=dict(
            xaxis_title="X / r_s",
            yaxis_title="Y / r_s",
            zaxis_title="Z / r_s",
            bgcolor="#0b0f29",
            xaxis=dict(range=[-15, 15]),
            yaxis=dict(range=[-15, 15]),
            zaxis=dict(range=[-5, 5]),
            camera=dict(eye=dict(x=0.0, y=-1.5, z=1.8))
        ),
        margin=dict(l=20, r=20, t=50, b=20),
        height=550
    )
    return fig

