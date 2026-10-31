"""
GRAVISIM: 2D Interactive Simulation Laboratory
==============================================

Primary interactive simulation environment supporting Point Mass, SIS,
Elliptical Galaxy (SIE), Binary Lens, and Galaxy Cluster mass models.
Enhanced with live source-dragging, animated result transitions, and
side-by-side analysis panels.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from simulation.point_mass import PointMassSimulation
from simulation.galaxy_lens import GalaxyLensSimulation
from simulation.binary_lens import BinaryLensSimulation
from simulation.cluster_lens import ClusterLensSimulation
from visualization.plots_2d import plot_lensed_system_2d
from visualization.lensing_maps import plot_analysis_maps
from visualization.light_paths import plot_optical_bench_rays
from physics.lens_equation import solve_point_mass_images_1d
from physics.magnification import point_mass_magnification_analytical
from storage.simulations import save_simulation_record
from storage.exports import export_to_json, export_images_to_csv


def _source_position_minimap(src_x: float, src_y: float, theta_e: float, fov: float):
    """Interactive source-position mini-map showing source, lens, Einstein ring, and images."""
    fig = go.Figure()

    # Einstein ring
    angles = np.linspace(0, 2 * np.pi, 100)
    fig.add_trace(go.Scatter(
        x=theta_e * np.cos(angles), y=theta_e * np.sin(angles),
        mode="lines",
        line=dict(color="#4A5FD9", width=2, dash="dot"),
        name=f"Einstein Ring (θ_E = {theta_e:.2f}\")",
        hoverinfo="name"
    ))

    # Lens at origin
    fig.add_trace(go.Scatter(
        x=[0], y=[0],
        mode="markers",
        marker=dict(size=14, color="#FFD700", symbol="star",
                    line=dict(color="#FFFFFF", width=1)),
        name="Lens", hoverinfo="name"
    ))

    # Source position
    fig.add_trace(go.Scatter(
        x=[src_x], y=[src_y],
        mode="markers+text",
        marker=dict(size=12, color="#FF4B4B", symbol="diamond",
                    line=dict(color="#FFFFFF", width=1)),
        text=[f"Source\n({src_x:.2f}\", {src_y:.2f}\")"],
        textposition="top right",
        textfont=dict(size=11, color="#FF4B4B"),
        name="Source", hoverinfo="name+text"
    ))

    # Predicted images (if not on-axis)
    beta_dist = np.hypot(src_x, src_y)
    if beta_dist > 0.01:
        tp, tm = solve_point_mass_images_1d(beta_dist, theta_e)
        ux = src_x / beta_dist
        uy = src_y / beta_dist
        im1_x, im1_y = tp * ux, tp * uy
        im2_x, im2_y = tm * ux, tm * uy

        fig.add_trace(go.Scatter(
            x=[im1_x], y=[im1_y],
            mode="markers",
            marker=dict(size=10, color="#00FFAA", symbol="circle",
                        line=dict(color="#FFFFFF", width=1)),
            name=f"Image + ({tp:.2f}\")", hoverinfo="name"
        ))
        fig.add_trace(go.Scatter(
            x=[im2_x], y=[im2_y],
            mode="markers",
            marker=dict(size=10, color="#FF8800", symbol="circle",
                        line=dict(color="#FFFFFF", width=1)),
            name=f"Image − ({abs(tm):.2f}\")", hoverinfo="name"
        ))

        # Lines connecting source to images through lens
        fig.add_trace(go.Scatter(
            x=[im1_x, 0, src_x], y=[im1_y, 0, src_y],
            mode="lines",
            line=dict(color="rgba(0,255,170,0.3)", width=1, dash="dash"),
            showlegend=False, hoverinfo="skip"
        ))

    half = max(fov / 2.0, theta_e * 2.0, beta_dist * 1.5)

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(11, 15, 41, 0.6)",
        font=dict(family="Inter, sans-serif", color="#FFFFFF", size=11),
        xaxis=dict(title="θ_x (arcsec)", range=[-half, half], scaleanchor="y", scaleratio=1),
        yaxis=dict(title="θ_y (arcsec)", range=[-half, half]),
        margin=dict(l=35, r=10, t=10, b=35),
        height=280,
        legend=dict(orientation="h", y=-0.25, x=0.0, font=dict(size=10))
    )
    return fig


def render_2d_simulation():
    st.markdown("### 🔬 2D Gravitational Lensing Simulation")
    st.write(
        "Manipulate physical parameters of the lensing geometry in real-time. "
        "The numerical engine traces millions of virtual light paths through the gravitational potential."
    )

    # Check for preset parameters transferred from dashboard
    default_model = st.session_state.get("preset_model", "point_mass")
    default_src_x = st.session_state.get("preset_source_x", 0.4)
    default_src_y = st.session_state.get("preset_source_y", 0.2)

    # ── Controls + Minimap Side-by-Side ──────────────────────────────
    col_ctrl, col_mini, col_viz = st.columns([3, 3, 6])

    with col_ctrl:
        st.markdown("#### ⚙️ Physical Parameters")

        model_choice = st.selectbox(
            "Lens Mass Profile",
            options=["point_mass", "sie_galaxy", "sis_galaxy", "binary_lens", "cluster"],
            format_func=lambda x: {
                "point_mass": "1. Point-Mass Lens",
                "sie_galaxy": "2. Elliptical Galaxy (SIE)",
                "sis_galaxy": "3. Isothermal Sphere (SIS)",
                "binary_lens": "4. Binary Point-Mass",
                "cluster": "5. Galaxy Cluster"
            }[x],
            index=["point_mass", "sie_galaxy", "sis_galaxy", "binary_lens", "cluster"].index(default_model)
        )

        st.markdown("##### 📍 Source Position")
        src_x = st.slider("β_x (arcsec)", -3.0, 3.0, float(default_src_x), 0.05, key="sim2d_sx")
        src_y = st.slider("β_y (arcsec)", -3.0, 3.0, float(default_src_y), 0.05, key="sim2d_sy")
        src_rad = st.slider("Source Radius (arcsec)", 0.05, 1.0, 0.18, 0.02, key="sim2d_sr")

        st.markdown("##### 🌌 Mass & Distance")
        if model_choice == "point_mass":
            mass_exp = st.slider("log₁₀(M / M☉)", 9.0, 14.0, 11.0, 0.2, key="sim2d_mass")
            mass_solar = 10.0**mass_exp
            d_l = st.number_input("D_L (Mpc)", 100.0, 5000.0, 1000.0, 50.0, key="sim2d_dl")
            d_s = st.number_input("D_S (Mpc)", d_l + 50.0, 10000.0, 2000.0, 50.0, key="sim2d_ds")
            d_ls = d_s - d_l
        elif model_choice in ["sie_galaxy", "sis_galaxy"]:
            theta_e_input = st.slider("θ_E (arcsec)", 0.5, 4.0, 1.5, 0.1, key="sim2d_te")
            if model_choice == "sie_galaxy":
                axis_ratio_q = st.slider("Axis Ratio q", 0.2, 0.99, 0.75, 0.05, key="sim2d_q")
                orient_deg = st.slider("PA (deg)", 0.0, 180.0, 30.0, 5.0, key="sim2d_pa")
        elif model_choice == "binary_lens":
            tot_te = st.slider("θ_E total (arcsec)", 0.8, 3.5, 1.8, 0.1, key="sim2d_bte")
            sep = st.slider("Separation (arcsec)", 0.5, 4.0, 1.6, 0.1, key="sim2d_sep")
            q_mass = st.slider("Mass Ratio q", 0.1, 5.0, 1.0, 0.1, key="sim2d_qm")
            bin_ang = st.slider("PA (deg)", 0.0, 180.0, 0.0, 5.0, key="sim2d_ba")
        elif model_choice == "cluster":
            cluster_te = st.slider("Cluster θ_E (arcsec)", 4.0, 18.0, 8.0, 0.5, key="sim2d_cte")
            core_rad = st.slider("Core Radius (arcsec)", 0.5, 5.0, 2.0, 0.2, key="sim2d_cr")

        resolution = st.select_slider(
            "Grid Resolution (N×N)",
            options=[80, 120, 160, 200, 240],
            value=160, key="sim2d_res"
        )
        show_caustics = st.checkbox("Critical Curves & Caustics", value=True, key="sim2d_cc")
        show_analysis = st.checkbox("Magnification & Shear Maps", value=False, key="sim2d_maps")
        show_bench = st.checkbox("Show Optical Bench Rays", value=False, key="sim2d_bench")

    # ── Run Simulation ───────────────────────────────────────────────
    with st.spinner("Computing backward ray-tracing..."):
        if model_choice == "point_mass":
            sim = PointMassSimulation(
                mass_solar=mass_solar,
                d_l_mpc=d_l, d_s_mpc=d_s, d_ls_mpc=d_ls,
                source_x=src_x, source_y=src_y,
                source_radius=src_rad,
                resolution=resolution
            )
        elif model_choice == "sie_galaxy":
            sim = GalaxyLensSimulation(
                is_elliptical=True,
                theta_e_arcsec=theta_e_input,
                axis_ratio_q=axis_ratio_q,
                orientation_deg=orient_deg,
                source_x=src_x, source_y=src_y,
                source_radius=src_rad,
                resolution=resolution
            )
        elif model_choice == "sis_galaxy":
            sim = GalaxyLensSimulation(
                is_elliptical=False,
                theta_e_arcsec=theta_e_input,
                source_x=src_x, source_y=src_y,
                source_radius=src_rad,
                resolution=resolution
            )
        elif model_choice == "binary_lens":
            sim = BinaryLensSimulation(
                total_theta_e=tot_te,
                separation=sep,
                mass_ratio=q_mass,
                angle_deg=bin_ang,
                source_x=src_x, source_y=src_y,
                source_radius=src_rad,
                resolution=resolution
            )
        elif model_choice == "cluster":
            sim = ClusterLensSimulation(
                cluster_theta_e=cluster_te,
                core_radius=core_rad,
                source_x=src_x, source_y=src_y,
                source_radius=src_rad,
                resolution=resolution
            )

        data = sim.run()

    # ── Source-Position Minimap ───────────────────────────────────────
    with col_mini:
        st.markdown("#### 🗺️ Geometry Map")
        st.caption("Source, lens, Einstein ring & predicted image positions")
        te_disp = data.get("theta_e_arcsec") or data.get("total_theta_e") or data.get("cluster_theta_e") or 1.5
        fig_mini = _source_position_minimap(src_x, src_y, te_disp, data.get("fov_arcsec", 6.0))
        st.plotly_chart(fig_mini, use_container_width=True, key="sim2d_minimap")

        # Live image statistics
        st.markdown("##### 📐 Live Image Summary")
        if "images" in data:
            for idx, im in enumerate(data["images"]):
                if im.get("is_ring"):
                    st.markdown(f"**🟡 Einstein Ring** — r = `{im['radius']:.3f}\"`")
                else:
                    parity_sym = "🟢 +" if im["parity"] > 0 else "🟠 −"
                    st.markdown(
                        f"**{parity_sym} Image {idx+1}** — "
                        f"(`{im['x']:.3f}\"`, `{im['y']:.3f}\"`) "
                        f"μ = `{im['magnification']:.3f}`"
                    )

    # ── Main Visualization Panel ─────────────────────────────────────
    with col_viz:
        st.markdown("#### 🖼️ Source Plane vs Image Plane")
        fig = plot_lensed_system_2d(data, show_caustics=show_caustics)
        st.plotly_chart(fig, use_container_width=True, key="sim2d_main")

        # Telemetry bar
        t1, t2, t3, t4 = st.columns(4)
        t1.metric("⏱️ Compute", f"{data['computation_time_seconds']*1000:.1f} ms")
        t2.metric("🔲 Grid", f"{resolution}²")
        t3.metric("🔍 Eff. Magnification", f"{data['effective_magnification']:.2f}×")
        t4.metric("⭕ θ_E", f"{te_disp:.2f}\"" if te_disp else "—")

    # ── Extended Analysis Panels ─────────────────────────────────────
    if show_analysis:
        st.markdown("---")
        st.markdown("#### 🗺️ Magnification, Convergence, and Shear Diagnostic Maps")
        fig_maps = plot_analysis_maps(data)
        st.plotly_chart(fig_maps, use_container_width=True, key="sim2d_analysis")

    if show_bench and model_choice == "point_mass":
        st.markdown("---")
        st.markdown("#### 🔭 Optical Bench Light-Path Diagram")
        beta_dist = np.hypot(src_x, src_y)
        tp, tm = solve_point_mass_images_1d(max(beta_dist, 0.01), data.get("theta_e_arcsec", 1.0))
        fig_bench = plot_optical_bench_rays(d_l, d_s, beta_dist, data.get("theta_e_arcsec", 1.0), tp, tm)
        st.plotly_chart(fig_bench, use_container_width=True, key="sim2d_bench")

    # ── Detailed Images Table ────────────────────────────────────────
    if "images" in data:
        with st.expander("📋 **Detailed Predicted Image Properties Table**", expanded=False):
            img_table = []
            for idx, im in enumerate(data["images"]):
                if im.get("is_ring", False):
                    img_table.append({
                        "Image": "Continuous Ring",
                        "X (arcsec)": "0.000",
                        "Y (arcsec)": "0.000",
                        "Radius (arcsec)": f"{im['radius']:.4f}",
                        "Parity": "Ring (0)",
                        "Magnification": "∞ (Singular)"
                    })
                else:
                    img_table.append({
                        "Image": f"Image {idx+1} ({im.get('type', 'Point')})",
                        "X (arcsec)": f"{im['x']:.4f}",
                        "Y (arcsec)": f"{im['y']:.4f}",
                        "Dist from Lens": f"{im.get('distance_from_lens', 0.0):.4f}",
                        "Parity": "+1 (Min)" if im["parity"] > 0 else "−1 (Saddle)",
                        "Magnification": f"{im['magnification']:.4f}×"
                    })
            st.dataframe(pd.DataFrame(img_table), use_container_width=True)

    # ── Save & Export ────────────────────────────────────────────────
    st.markdown("---")
    exp1, exp2, exp3 = st.columns(3)

    with exp1:
        if st.button("💾 Save to Database", use_container_width=True, key="sim2d_save"):
            sim_id = save_simulation_record(
                name=f"{model_choice.upper()} Sim",
                model_type=model_choice,
                config={"source_x": src_x, "source_y": src_y, "resolution": resolution},
                results={"effective_magnification": data["effective_magnification"]}
            )
            st.success(f"Saved! ID: `{sim_id}`")

    with exp2:
        json_str = export_to_json(data)
        st.download_button(
            "📥 Export JSON",
            data=json_str,
            file_name=f"gravisim_{model_choice}.json",
            mime="application/json",
            use_container_width=True,
            key="sim2d_json"
        )

    with exp3:
        if "images" in data:
            csv_str = export_images_to_csv(data["images"])
            st.download_button(
                "📥 Export Images CSV",
                data=csv_str,
                file_name=f"gravisim_images_{model_choice}.csv",
                mime="text/csv",
                use_container_width=True,
                key="sim2d_csv"
            )
