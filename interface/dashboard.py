"""
GRAVISIM: Dashboard Page — Fully Interactive Control Center
===========================================================

Live-updating metric cards, real-time parameter controls, animated simulation
preview, interactive scientific plots, and dynamic preset launchers.
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from interface.styles import render_metric_card
from simulation.point_mass import PointMassSimulation
from simulation.galaxy_lens import GalaxyLensSimulation
from simulation.binary_lens import BinaryLensSimulation
from visualization.plots_2d import plot_lensed_system_2d
from physics.einstein_radius import calculate_einstein_radius_arcsec
from physics.deflection import weak_field_deflection_angle_arcsec
from physics.lens_equation import solve_point_mass_images_1d, solve_point_mass_images_2d
from physics.magnification import point_mass_magnification_analytical
from physics.constants import M_SUN, KPC, MPC, RAD_TO_ARCSEC
from relativity.schwarzschild import black_hole_summary


def _interactive_deflection_chart(mass_solar: float):
    """Live-updating deflection angle vs impact parameter graph."""
    mass_kg = mass_solar * M_SUN
    b_vals = np.linspace(1.0, 100.0, 80)  # kpc
    alpha_vals = [weak_field_deflection_angle_arcsec(mass_kg, b * KPC) for b in b_vals]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=b_vals, y=alpha_vals,
        mode="lines",
        line=dict(color="#4A5FD9", width=3),
        fill="tozeroy",
        fillcolor="rgba(74, 95, 217, 0.15)",
        name="α(b)"
    ))
    # Marker at b=10 kpc reference
    alpha_10 = weak_field_deflection_angle_arcsec(mass_kg, 10.0 * KPC)
    fig.add_trace(go.Scatter(
        x=[10.0], y=[alpha_10],
        mode="markers+text",
        marker=dict(size=12, color="#FFD700", symbol="diamond"),
        text=[f"{alpha_10:.3f}\""],
        textposition="top right",
        textfont=dict(color="#FFD700", size=13),
        name="b = 10 kpc"
    ))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(11, 15, 41, 0.6)",
        font=dict(family="Inter, sans-serif", color="#FFFFFF", size=12),
        xaxis_title="Impact Parameter b (kpc)",
        yaxis_title="Deflection α (arcsec)",
        margin=dict(l=45, r=15, t=10, b=40),
        height=260,
        showlegend=False
    )
    return fig


def _interactive_einstein_vs_mass(d_l_mpc: float, d_s_mpc: float, d_ls_mpc: float, current_mass: float):
    """Live-updating Einstein radius vs lens mass graph."""
    masses = np.logspace(9.0, 14.0, 60)
    te_vals = [calculate_einstein_radius_arcsec(m * M_SUN, d_l_mpc, d_s_mpc, d_ls_mpc) for m in masses]

    te_current = calculate_einstein_radius_arcsec(current_mass * M_SUN, d_l_mpc, d_s_mpc, d_ls_mpc)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=masses, y=te_vals,
        mode="lines",
        line=dict(color="#00FFAA", width=3),
        fill="tozeroy",
        fillcolor="rgba(0, 255, 170, 0.1)",
        name="θ_E(M)"
    ))
    fig.add_trace(go.Scatter(
        x=[current_mass], y=[te_current],
        mode="markers+text",
        marker=dict(size=14, color="#FF4B4B", symbol="star"),
        text=[f"{te_current:.2f}\""],
        textposition="top left",
        textfont=dict(color="#FF4B4B", size=14, family="Inter"),
        name="Current"
    ))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(11, 15, 41, 0.6)",
        font=dict(family="Inter, sans-serif", color="#FFFFFF", size=12),
        xaxis_title="Lens Mass (M☉)",
        yaxis_title="Einstein Radius θ_E (arcsec)",
        xaxis_type="log",
        margin=dict(l=45, r=15, t=10, b=40),
        height=260,
        showlegend=False
    )
    return fig


def _interactive_magnification_chart(theta_e: float):
    """Live-updating magnification vs source offset graph."""
    betas = np.linspace(0.05, 4.0, 80)
    mu_tot = []
    mu_p = []
    mu_m = []
    for b in betas:
        mag = point_mass_magnification_analytical(b, theta_e)
        mu_tot.append(min(mag["mu_tot"], 50.0))
        mu_p.append(min(mag["mu_plus"], 50.0))
        mu_m.append(min(mag["mu_minus"], 50.0))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=betas, y=mu_tot,
        mode="lines",
        line=dict(color="#FFD700", width=3),
        name="Total |μ|"
    ))
    fig.add_trace(go.Scatter(
        x=betas, y=mu_p,
        mode="lines",
        line=dict(color="#00FFAA", width=2, dash="dot"),
        name="μ₊"
    ))
    fig.add_trace(go.Scatter(
        x=betas, y=mu_m,
        mode="lines",
        line=dict(color="#FF8800", width=2, dash="dot"),
        name="|μ₋|"
    ))
    # Reference line at mu = 1 (no lensing)
    fig.add_hline(y=1.0, line_dash="dash", line_color="#555555", annotation_text="No lensing")
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(11, 15, 41, 0.6)",
        font=dict(family="Inter, sans-serif", color="#FFFFFF", size=12),
        xaxis_title="Source Offset β (arcsec)",
        yaxis_title="Magnification |μ|",
        margin=dict(l=45, r=15, t=10, b=40),
        height=260,
        legend=dict(orientation="h", y=1.12, x=0.0, font=dict(size=11))
    )
    return fig


def _interactive_image_position_chart(theta_e: float, current_beta: float):
    """Live-updating image position diagram showing where images form as source moves."""
    betas = np.linspace(0.01, 3.0, 60)
    t_plus_vals = []
    t_minus_vals = []
    for b in betas:
        tp, tm = solve_point_mass_images_1d(b, theta_e)
        t_plus_vals.append(tp)
        t_minus_vals.append(tm)

    tp_curr, tm_curr = solve_point_mass_images_1d(max(current_beta, 0.01), theta_e)

    fig = go.Figure()
    # Einstein radius reference lines
    fig.add_hline(y=theta_e, line_dash="dot", line_color="#4A5FD9",
                  annotation_text=f"θ_E = {theta_e:.2f}\"", annotation_position="top left")
    fig.add_hline(y=-theta_e, line_dash="dot", line_color="#4A5FD9")

    fig.add_trace(go.Scatter(
        x=betas, y=t_plus_vals,
        mode="lines",
        line=dict(color="#00FFAA", width=3),
        name="θ₊ (primary)"
    ))
    fig.add_trace(go.Scatter(
        x=betas, y=t_minus_vals,
        mode="lines",
        line=dict(color="#FF8800", width=3),
        name="θ₋ (secondary)"
    ))
    # Current markers
    fig.add_trace(go.Scatter(
        x=[current_beta, current_beta],
        y=[tp_curr, tm_curr],
        mode="markers",
        marker=dict(size=14, color=["#00FFAA", "#FF8800"], symbol="diamond",
                    line=dict(color="#FFFFFF", width=2)),
        name="Current Images"
    ))
    # Vertical reference line at current beta
    fig.add_vline(x=current_beta, line_dash="dash", line_color="rgba(255,255,255,0.3)")

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(11, 15, 41, 0.6)",
        font=dict(family="Inter, sans-serif", color="#FFFFFF", size=12),
        xaxis_title="Source Offset β (arcsec)",
        yaxis_title="Image Position θ (arcsec)",
        margin=dict(l=45, r=15, t=10, b=40),
        height=260,
        legend=dict(orientation="h", y=1.12, x=0.0, font=dict(size=11))
    )
    return fig


def render_dashboard():
    # ── Interactive Control Bar ──────────────────────────────────────
    st.markdown("### 🔭 Mission Control & Live Simulation Dashboard")

    with st.expander("⚡ **Quick-Tune Physical Parameters** — drag sliders to update everything in real-time", expanded=True):
        pc1, pc2, pc3, pc4 = st.columns(4)
        with pc1:
            mass_exp = st.slider("Lens Mass log₁₀(M/M☉)", 9.0, 14.0, 11.0, 0.1,
                                 help="Drag to change lens mass — all charts and metrics update live")
        with pc2:
            d_l_mpc = st.slider("D_L (Mpc)", 100.0, 3000.0, 1000.0, 50.0,
                                help="Observer-to-Lens angular diameter distance")
        with pc3:
            d_s_mpc = st.slider("D_S (Mpc)", 500.0, 5000.0, 2000.0, 50.0,
                                help="Observer-to-Source angular diameter distance")
        with pc4:
            src_offset = st.slider("Source Offset β (arcsec)", 0.0, 3.0, 0.5, 0.05,
                                   help="Background source misalignment from optical axis")

    mass_solar = 10.0 ** mass_exp
    d_ls_mpc = max(d_s_mpc - d_l_mpc, 50.0)

    # ── Live-Computed Physics ────────────────────────────────────────
    mass_kg = mass_solar * M_SUN
    theta_e = calculate_einstein_radius_arcsec(mass_kg, d_l_mpc, d_s_mpc, d_ls_mpc)
    defl_10kpc = weak_field_deflection_angle_arcsec(mass_kg, 10.0 * KPC)

    if src_offset > 0.01:
        mag_data = point_mass_magnification_analytical(src_offset, theta_e)
        mu_tot = mag_data["mu_tot"]
        n_images = 2
        tp, tm = solve_point_mass_images_1d(src_offset, theta_e)
    else:
        mu_tot = float("inf")
        n_images = "∞ (Ring)"
        tp, tm = theta_e, -theta_e

    # ── Live Metric Cards ────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)

    with m1:
        render_metric_card(
            title="Active Lens Model",
            value=f"{mass_solar:.1e} M☉",
            caption=f"Point-mass thin-lens | log₁₀M = {mass_exp:.1f}",
            badge="Live"
        )
    with m2:
        render_metric_card(
            title="Einstein Radius θ_E",
            value=f"{theta_e:.3f}\"",
            caption=f"= {theta_e * 1000:.1f} milliarcsec | D_LS/D_S = {d_ls_mpc/d_s_mpc:.2f}",
            badge="Live"
        )
    with m3:
        render_metric_card(
            title="Deflection α (b=10 kpc)",
            value=f"{defl_10kpc:.4f}\"",
            caption=f"Weak-field 4GM/(c²b) at b = 10 kpc",
            badge="4GM/c²"
        )
    with m4:
        if isinstance(n_images, int):
            mu_str = f"{mu_tot:.2f}×"
        else:
            mu_str = "∞ (Singular)"
        render_metric_card(
            title="Total Magnification",
            value=mu_str,
            caption=f"{n_images} images | β = {src_offset:.2f}\" | θ₊ = {tp:.2f}\" θ₋ = {tm:.2f}\"",
            badge="Live"
        )

    st.markdown("---")

    # ── Main Content: Preview + Live Science Graphs ──────────────────
    col_preview, col_graphs = st.columns([6, 6])

    with col_preview:
        st.markdown("#### 🌐 Live Simulation Preview")
        st.caption("Parameters above control this preview — drag sliders to watch the lensing change.")

        # Source position angle for 2D placement
        src_x = src_offset * 0.8
        src_y = src_offset * 0.6

        with st.spinner("Ray-tracing..."):
            preview_sim = PointMassSimulation(
                mass_solar=mass_solar,
                d_l_mpc=d_l_mpc,
                d_s_mpc=d_s_mpc,
                d_ls_mpc=d_ls_mpc,
                source_x=src_x,
                source_y=src_y,
                source_radius=0.18,
                resolution=130
            )
            data = preview_sim.run()

        fig_preview = plot_lensed_system_2d(data)
        st.plotly_chart(fig_preview, use_container_width=True, key="dash_preview")

        # Image solutions table
        if "images" in data:
            cols_im = st.columns(len(data["images"]))
            for idx, im in enumerate(data["images"]):
                with cols_im[idx]:
                    if im.get("is_ring"):
                        st.markdown(f"""
                        <div class="metric-card" style="text-align:center;">
                            <div class="metric-title">🟡 Einstein Ring</div>
                            <div class="metric-value" style="font-size:18px;">r = {im['radius']:.3f}\"</div>
                            <div class="metric-caption">μ = ∞ (Singular)</div>
                        </div>""", unsafe_allow_html=True)
                    else:
                        parity_icon = "🟢" if im["parity"] > 0 else "🟠"
                        parity_label = "Primary (+)" if im["parity"] > 0 else "Secondary (−)"
                        st.markdown(f"""
                        <div class="metric-card" style="text-align:center;">
                            <div class="metric-title">{parity_icon} Image {idx+1}: {parity_label}</div>
                            <div class="metric-value" style="font-size:16px;">({im['x']:.3f}\", {im['y']:.3f}\")</div>
                            <div class="metric-caption">μ = {im['magnification']:.3f}× | d = {im.get('distance_from_lens',0):.3f}\"</div>
                        </div>""", unsafe_allow_html=True)

    with col_graphs:
        st.markdown("#### 📊 Live Scientific Graphs")
        st.caption("All curves update in real-time as you change the parameters above.")

        graph_tab1, graph_tab2, graph_tab3, graph_tab4 = st.tabs([
            "α vs b", "θ_E vs M", "μ vs β", "Image θ vs β"
        ])

        with graph_tab1:
            fig_defl = _interactive_deflection_chart(mass_solar)
            st.plotly_chart(fig_defl, use_container_width=True, key="dash_defl")

        with graph_tab2:
            fig_te = _interactive_einstein_vs_mass(d_l_mpc, d_s_mpc, d_ls_mpc, mass_solar)
            st.plotly_chart(fig_te, use_container_width=True, key="dash_te")

        with graph_tab3:
            fig_mag = _interactive_magnification_chart(theta_e)
            st.plotly_chart(fig_mag, use_container_width=True, key="dash_mag")

        with graph_tab4:
            fig_img = _interactive_image_position_chart(theta_e, src_offset)
            st.plotly_chart(fig_img, use_container_width=True, key="dash_img")

    st.markdown("---")

    # ── Quick Launch Presets ──────────────────────────────────────────
    st.markdown("#### ⚡ Quick-Launch Astrophysical Scenarios")
    st.caption("Click any card below to jump straight into a pre-configured simulation.")

    p1, p2, p3, p4, p5, p6 = st.columns(6)

    with p1:
        if st.button("🔴\nPerfect\nEinstein Ring", use_container_width=True):
            st.session_state["preset_model"] = "point_mass"
            st.session_state["preset_source_x"] = 0.0
            st.session_state["preset_source_y"] = 0.0
            st.session_state["active_tab"] = "2D Simulation"
            st.rerun()
    with p2:
        if st.button("✨\nEinstein's\nCross", use_container_width=True):
            st.session_state["preset_model"] = "sie_galaxy"
            st.session_state["preset_source_x"] = 0.06
            st.session_state["preset_source_y"] = 0.04
            st.session_state["active_tab"] = "2D Simulation"
            st.rerun()
    with p3:
        if st.button("🌌\nGalaxy\nArc", use_container_width=True):
            st.session_state["preset_model"] = "sis_galaxy"
            st.session_state["preset_source_x"] = 0.15
            st.session_state["preset_source_y"] = 0.1
            st.session_state["active_tab"] = "2D Simulation"
            st.rerun()
    with p4:
        if st.button("🪐\nBinary\nCaustic", use_container_width=True):
            st.session_state["preset_model"] = "binary_lens"
            st.session_state["preset_source_x"] = 0.2
            st.session_state["preset_source_y"] = 0.1
            st.session_state["active_tab"] = "2D Simulation"
            st.rerun()
    with p5:
        if st.button("🕳️\nBlack Hole\nGeodesics", use_container_width=True):
            st.session_state["active_tab"] = "3D Visualization"
            st.rerun()
    with p6:
        if st.button("🏅\nValidation\nTest Suite", use_container_width=True):
            st.session_state["active_tab"] = "Analysis Laboratory"
            st.rerun()

    st.markdown("---")

    # ── Interactive Parameter Sensitivity Explorer ────────────────────
    st.markdown("#### 🔬 Parameter Sensitivity Explorer")
    st.caption(
        "Investigate how each physical parameter independently affects lensing observables. "
        "Select a parameter to sweep and watch the resulting curves."
    )

    sens_col1, sens_col2 = st.columns([3, 9])

    with sens_col1:
        sweep_param = st.selectbox(
            "Sweep Parameter",
            options=["Lens Mass", "Observer-Lens Distance", "Source Offset"],
            help="Choose which variable to sweep while holding others fixed"
        )
        n_points = st.slider("Sweep Resolution", 20, 100, 50, 10)
        show_secondary = st.checkbox("Show secondary observables", value=True)

    with sens_col2:
        fig_sens = make_subplots(
            rows=1, cols=3,
            subplot_titles=("Einstein Radius θ_E", "Deflection α(b=10kpc)", "Total Magnification |μ|"),
            horizontal_spacing=0.08
        )

        if sweep_param == "Lens Mass":
            sweep_vals = np.logspace(9.0, 14.0, n_points)
            x_label = "Mass (M☉)"
            te_arr = [calculate_einstein_radius_arcsec(m * M_SUN, d_l_mpc, d_s_mpc, d_ls_mpc) for m in sweep_vals]
            alpha_arr = [weak_field_deflection_angle_arcsec(m * M_SUN, 10.0 * KPC) for m in sweep_vals]
            mu_arr = []
            for te_val in te_arr:
                if src_offset > 0.01:
                    mu_arr.append(min(point_mass_magnification_analytical(src_offset, te_val)["mu_tot"], 100.0))
                else:
                    mu_arr.append(100.0)
            x_type = "log"

        elif sweep_param == "Observer-Lens Distance":
            sweep_vals = np.linspace(100.0, 2500.0, n_points)
            x_label = "D_L (Mpc)"
            te_arr = []
            for dl in sweep_vals:
                dls = max(d_s_mpc - dl, 50.0)
                te_arr.append(calculate_einstein_radius_arcsec(mass_kg, dl, d_s_mpc, dls))
            alpha_arr = [defl_10kpc] * n_points  # doesn't depend on distance
            mu_arr = []
            for te_val in te_arr:
                if src_offset > 0.01:
                    mu_arr.append(min(point_mass_magnification_analytical(src_offset, te_val)["mu_tot"], 100.0))
                else:
                    mu_arr.append(100.0)
            x_type = "linear"

        else:  # Source Offset
            sweep_vals = np.linspace(0.05, 3.0, n_points)
            x_label = "Source Offset β (arcsec)"
            te_arr = [theta_e] * n_points
            alpha_arr = [defl_10kpc] * n_points
            mu_arr = [min(point_mass_magnification_analytical(b, theta_e)["mu_tot"], 100.0) for b in sweep_vals]
            x_type = "linear"

        fig_sens.add_trace(go.Scatter(x=sweep_vals, y=te_arr, mode="lines",
                                      line=dict(color="#00FFAA", width=3)), row=1, col=1)
        fig_sens.add_trace(go.Scatter(x=sweep_vals, y=alpha_arr, mode="lines",
                                      line=dict(color="#4A5FD9", width=3)), row=1, col=2)
        fig_sens.add_trace(go.Scatter(x=sweep_vals, y=mu_arr, mode="lines",
                                      line=dict(color="#FFD700", width=3)), row=1, col=3)

        fig_sens.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(11, 15, 41, 0.6)",
            font=dict(family="Inter, sans-serif", color="#FFFFFF", size=12),
            margin=dict(l=40, r=20, t=35, b=40),
            height=280,
            showlegend=False
        )
        if x_type == "log":
            fig_sens.update_xaxes(type="log")
        for i in range(1, 4):
            fig_sens.update_xaxes(title_text=x_label, row=1, col=i)
        fig_sens.update_yaxes(title_text="arcsec", row=1, col=1)
        fig_sens.update_yaxes(title_text="arcsec", row=1, col=2)
        fig_sens.update_yaxes(title_text="|μ|", row=1, col=3)

        st.plotly_chart(fig_sens, use_container_width=True, key="dash_sensitivity")

    st.markdown("---")

    # ── Interactive Black Hole Quick Lookup ───────────────────────────
    st.markdown("#### 🕳️ Quick Black Hole Inspector")
    st.caption("Select a known astrophysical black hole to instantly compute its relativistic properties.")

    bh_col1, bh_col2 = st.columns([4, 8])

    with bh_col1:
        bh_choice = st.selectbox(
            "Astrophysical Object",
            options=["M87* (6.5 billion M☉)", "Sgr A* (4.15 million M☉)",
                     "Cygnus X-1 (21.2 M☉)", "TON 618 (66 billion M☉)", "Custom"],
            key="dash_bh"
        )

        if "M87*" in bh_choice:
            bh_mass = 6.5e9
        elif "Sgr A*" in bh_choice:
            bh_mass = 4.15e6
        elif "Cygnus" in bh_choice:
            bh_mass = 21.2
        elif "TON 618" in bh_choice:
            bh_mass = 6.6e10
        else:
            bh_mass_exp = st.slider("log₁₀(M / M☉)", 1.0, 11.0, 7.0, 0.5, key="dash_bh_mass")
            bh_mass = 10.0 ** bh_mass_exp

        bh_info = black_hole_summary(bh_mass)

    with bh_col2:
        bh_c1, bh_c2, bh_c3, bh_c4 = st.columns(4)
        with bh_c1:
            render_metric_card("Schwarzschild r_s", f"{bh_info['schwarzschild_radius_km']:.2e} km",
                               "Event horizon radius = 2GM/c²", badge="GR")
        with bh_c2:
            render_metric_card("Photon Sphere r_ph", f"{bh_info['photon_sphere_radius_km']:.2e} km",
                               "Unstable photon orbit = 1.5 r_s", badge="GR")
        with bh_c3:
            render_metric_card("Critical b_crit", f"{bh_info['critical_impact_parameter_km']:.2e} km",
                               "Capture threshold = 2.598 r_s", badge="GR")
        with bh_c4:
            render_metric_card("ISCO Radius", f"{bh_info['isco_radius_km']:.2e} km",
                               "Innermost stable orbit = 3 r_s", badge="GR")

    st.markdown("---")

    # ── Science Knowledge Brief ──────────────────────────────────────
    with st.expander("📖 **Scientific Briefing**: Principles of Gravitational Lensing"):
        st.markdown("""
        ### Foundations of Gravitational Deflection
        According to Einstein's General Theory of Relativity (1915), mass curves spacetime. Light travelling through curved spacetime follows **null geodesics**, causing rays to bend when passing near a mass $M$:

        $$\\hat{\\alpha} = \\frac{4GM}{c^2 b}$$

        Where:
        - $G = 6.67430 \\times 10^{-11}\\,\\text{m}^3\\,\\text{kg}^{-1}\\,\\text{s}^{-2}$ (Gravitational constant)
        - $c = 2.99792458 \\times 10^8\\,\\text{m/s}$ (Speed of light)
        - $b$ is the impact parameter (closest approach distance).

        ### Regimes of Gravitational Lensing
        | Regime | Image Separation | Observational Feature | Example Application |
        |---|---|---|---|
        | **Strong Lensing** | > 0.5\" | Arcs, rings, multiple images | Galaxy clusters, giant ellipticals |
        | **Weak Lensing** | Unresolved | Coherent tangential shear | Dark matter mapping, cosmology |
        | **Microlensing** | ~ μas | Transient brightening | Exoplanet detection, compact DM |

        ### Key Equations Used in GRAVISIM
        - **Einstein Radius**: $\\theta_E = \\sqrt{\\frac{4GM}{c^2}\\frac{D_{LS}}{D_L D_S}}$
        - **Lens Equation**: $\\vec{\\beta} = \\vec{\\theta} - \\theta_E^2 \\frac{\\vec{\\theta}}{|\\vec{\\theta}|^2}$
        - **Magnification**: $\\mu = \\frac{1}{\\det A}$, where $A = \\frac{\\partial \\vec{\\beta}}{\\partial \\vec{\\theta}}$
        - **Point-Mass Identity**: $\\mu_+ - \\mu_- = 1$ for all $\\beta > 0$
        """)
