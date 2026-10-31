"""
2D Scientific Lensing Plots
===========================

Generates publication-quality 2D scientific figures using Matplotlib and Plotly,
adhering to the GRAVISIM visual identity (#2E3A8C primary, #4A5FD9 light blue, #1A2254 navy).
"""

from typing import Dict, Any, List
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_lensed_system_2d(sim_data: Dict[str, Any], show_caustics: bool = True):
    """
    Generate an interactive Plotly figure comparing:
    1) Source Plane (Intrinsic source, caustics)
    2) Image Plane (Lensed images, critical curves, Einstein ring)
    """
    theta_x = sim_data["theta_x"]
    theta_y = sim_data["theta_y"]
    source_img = sim_data["source_image"]
    lensed_img = sim_data["lensed_image"]

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Source Plane (True Coordinates)", "Image Plane (Observer View)"),
        horizontal_spacing=0.08
    )

    x_1d = theta_x[0, :]
    y_1d = theta_y[:, 0]

    # Source plane heatmap
    fig.add_trace(
        go.Heatmap(
            x=x_1d, y=y_1d, z=source_img,
            colorscale=[[0, "#0d1333"], [0.5, "#4A5FD9"], [1, "#FFFFFF"]],
            showscale=False,
            name="Source Intensity"
        ),
        row=1, col=1
    )

    # Image plane heatmap
    fig.add_trace(
        go.Heatmap(
            x=x_1d, y=y_1d, z=lensed_img,
            colorscale=[[0, "#0d1333"], [0.5, "#4A5FD9"], [1, "#FFFFFF"]],
            showscale=False,
            name="Lensed Intensity"
        ),
        row=1, col=2
    )

    # Plot caustics if present
    if show_caustics and "caustics" in sim_data:
        for c in sim_data["caustics"]:
            if len(c) > 0:
                fig.add_trace(
                    go.Scatter(
                        x=c[:, 0], y=c[:, 1],
                        mode="lines",
                        line=dict(color="#FF4B4B", width=2, dash="dash"),
                        name="Caustic"
                    ),
                    row=1, col=1
                )

    # Plot critical curves if present
    if show_caustics and "critical_curves" in sim_data:
        for cc in sim_data["critical_curves"]:
            if len(cc) > 0:
                fig.add_trace(
                    go.Scatter(
                        x=cc[:, 0], y=cc[:, 1],
                        mode="lines",
                        line=dict(color="#00FFAA", width=2),
                        name="Critical Curve"
                    ),
                    row=1, col=2
                )

    # Add Einstein Ring circle for point mass or SIS
    theta_e = sim_data.get("theta_e_arcsec", None)
    if theta_e and sim_data.get("model_type") in ["point_mass", "sis_galaxy"]:
        angles = np.linspace(0, 2 * np.pi, 100)
        ring_x = theta_e * np.cos(angles)
        ring_y = theta_e * np.sin(angles)
        fig.add_trace(
            go.Scatter(
                x=ring_x, y=ring_y,
                mode="lines",
                line=dict(color="#4A5FD9", width=1.5, dash="dot"),
                name=f"Einstein Radius ({theta_e:.2f}\")"
            ),
            row=1, col=2
        )

    # Add analytical point image markers if available
    if "images" in sim_data:
        for idx, im in enumerate(sim_data["images"]):
            if not im.get("is_ring", False):
                fig.add_trace(
                    go.Scatter(
                        x=[im["x"]], y=[im["y"]],
                        mode="markers+text",
                        marker=dict(size=10, color="#FFD700", symbol="diamond"),
                        text=[f"Im {idx+1}"],
                        textposition="top right",
                        name=f"Image {idx+1}"
                    ),
                    row=1, col=2
                )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1A2254",
        plot_bgcolor="#0b0f29",
        font=dict(family="Inter, sans-serif", color="#FFFFFF"),
        margin=dict(l=40, r=40, t=50, b=40),
        height=520
    )
    fig.update_xaxes(title_text=r"$\beta_x \text{ (arcsec)}$", row=1, col=1, scaleanchor="y1")
    fig.update_yaxes(title_text=r"$\beta_y \text{ (arcsec)}$", row=1, col=1)
    fig.update_xaxes(title_text=r"$\theta_x \text{ (arcsec)}$", row=1, col=2, scaleanchor="y2")
    fig.update_yaxes(title_text=r"$\theta_y \text{ (arcsec)}$", row=1, col=2)

    return fig

