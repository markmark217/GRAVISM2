"""
Magnification, Convergence, and Shear Visualizations
====================================================
"""

from typing import Dict, Any
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_analysis_maps(sim_data: Dict[str, Any]):
    """
    Generate 3-panel Plotly figure:
    1) Magnification Map |mu| (log scale)
    2) Convergence Map kappa
    3) Shear Map gamma
    """
    theta_x = sim_data["theta_x"]
    theta_y = sim_data["theta_y"]
    x_1d = theta_x[0, :]
    y_1d = theta_y[:, 0]

    mag = np.log10(np.maximum(1.0, sim_data["magnification_map"]))
    kappa = sim_data["convergence_map"]
    shear = sim_data["shear_map"]

    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=("Magnification log10(|mu|)", "Convergence (kappa)", "Shear (gamma)"),
        horizontal_spacing=0.06
    )

    fig.add_trace(
        go.Heatmap(x=x_1d, y=y_1d, z=mag, colorscale="Viridis", name="log10(mu)"),
        row=1, col=1
    )
    fig.add_trace(
        go.Heatmap(x=x_1d, y=y_1d, z=kappa, colorscale="Inferno", name="kappa"),
        row=1, col=2
    )
    fig.add_trace(
        go.Heatmap(x=x_1d, y=y_1d, z=shear, colorscale="Magma", name="gamma"),
        row=1, col=3
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1A2254",
        plot_bgcolor="#0b0f29",
        font=dict(family="Inter, sans-serif", color="#FFFFFF"),
        margin=dict(l=30, r=30, t=50, b=30),
        height=450
    )
    fig.update_xaxes(title_text="arcsec", scaleanchor="y", scaleratio=1)
    fig.update_yaxes(title_text="arcsec")

    return fig

