"""
GRAVISIM: 3D Visualization Laboratory
=====================================

Interactive 3D representations of:
1. Spacetime curvature deformation
2. 3D Light-path trajectories along the cosmological optical bench
3. Schwarzschild black hole strong-field null geodesics & photon sphere
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from visualization.spacetime_grid import generate_spacetime_surface
from visualization.visualization_3d import plot_3d_light_rays, plot_3d_black_hole_geodesics
from relativity.schwarzschild import black_hole_summary
from relativity.black_hole_raytracing import generate_black_hole_image
from relativity.photon_orbits import deflection_comparison_data
from physics.lens_equation import solve_point_mass_images_1d
from physics.constants import M_SUN


def render_3d_visualization():
    st.markdown("### 🌌 3D Interactive Astrophysics & Spacetime Laboratory")
    st.write(
        "Explore three-dimensional spacetime curvature, light trajectories across cosmological distances, "
        "and strong-field relativistic photon orbits around Schwarzschild black holes."
    )

    tab_spacetime, tab_rays, tab_blackhole = st.tabs([
        "1. Spacetime Curvature Surface",
        "2. 3D Optical Light Paths",
        "3. Schwarzschild Black Hole Geodesics"
    ])

    with tab_spacetime:
        st.markdown("#### 🌐 3D Spacetime Curvature (Conceptual Embedding Surface)")
        st.info(
            "**Scientific Note:** The rubber-sheet embedding diagram visually illustrates gravitational potential "
            "wells ($\\Phi / c^2$). It is an explanatory heuristic representation, not a direct solution "
            "of the full four-dimensional Einstein field equations."
        )

        col_st_ctrl, col_st_plot = st.columns([3, 9])
        with col_st_ctrl:
            surface_model = st.selectbox(
                "Potential Configuration",
                options=["point_mass", "binary", "cluster"],
                format_func=lambda x: {
                    "point_mass": "Single Compact Mass / Galaxy",
                    "binary": "Binary Lens System",
                    "cluster": "Galaxy Cluster + Subhalos"
                }[x]
            )
            mass_exp = st.slider("Central Mass log10(M / M_sun)", 9.0, 14.0, 11.5, 0.5)
            grid_res = st.slider("Mesh Resolution", 30, 80, 50, 5)

        with col_st_plot:
            fig_surf = generate_spacetime_surface(
                mass_solar=10.0**mass_exp,
                model_type=surface_model,
                grid_size=grid_res
            )
            st.plotly_chart(fig_surf, use_container_width=True)

    with tab_rays:
        st.markdown("#### 🔭 3D Cosmological Optical Light Paths")
        st.write(
            "Visualizes the 3D ray geometry traversing from the background source plane ($z = D_S$), "
            "bending across the lens plane ($z = D_L$), and converging onto the observer ($z = 0$)."
        )

        r_col1, r_col2 = st.columns([3, 9])
        with r_col1:
            d_l = st.number_input("D_L: Observer to Lens (Mpc)", 200.0, 3000.0, 800.0, 100.0)
            d_s = st.number_input("D_S: Observer to Source (Mpc)", d_l + 100.0, 6000.0, 1800.0, 100.0)
            src_bx = st.slider("Source beta_x (arcsec)", -2.0, 2.0, 0.5, 0.1)
            src_by = st.slider("Source beta_y (arcsec)", -2.0, 2.0, 0.3, 0.1)
            te_arcsec = st.slider("Einstein Radius theta_E (arcsec)", 0.5, 3.0, 1.4, 0.1)

            beta_dist = np.hypot(src_bx, src_by)
            t_plus, t_minus = solve_point_mass_images_1d(beta_dist, te_arcsec)

        with r_col2:
            fig_rays = plot_3d_light_rays(
                d_l=d_l, d_s=d_s,
                beta_x=src_bx, beta_y=src_by,
                theta_plus=t_plus, theta_minus=t_minus
            )
            st.plotly_chart(fig_rays, use_container_width=True)

    with tab_blackhole:
        st.markdown("#### 🕳️ General Relativistic Schwarzschild Black Hole Geodesics")
        st.warning(
            "**General Relativity Distinction:** In the strong-field regime near a black hole ($r < 10\\,r_s$), "
            "the weak-field thin-lens approximation is strictly invalid. Light paths must be computed via "
            "numerical integration of the relativistic null geodesic equation in Schwarzschild spacetime: "
            "$$\\frac{d^2 u}{d\\phi^2} + u = \\frac{3}{2} r_s u^2$$"
        )

        bh_col1, bh_col2 = st.columns([4, 8])

        with bh_col1:
            st.markdown("##### ⚙️ Black Hole Parameters")
            bh_preset = st.selectbox(
                "Known Astrophysical Black Hole",
                options=["Custom", "M87*", "Sagittarius A* (Milky Way)", "Stellar-mass BH (Cyg X-1)"]
            )

            if bh_preset == "M87*":
                m_solar = 6.5e9
            elif bh_preset == "Sagittarius A* (Milky Way)":
                m_solar = 4.15e6
            elif bh_preset == "Stellar-mass BH (Cyg X-1)":
                m_solar = 21.2
            else:
                m_exp = st.slider("Black Hole Mass log10(M / M_sun)", 1.0, 10.0, 6.0, 0.5)
                m_solar = 10.0**m_exp

            bh_info = black_hole_summary(m_solar)

            st.markdown("##### 📏 Characteristic Relativistic Radii")
            st.markdown(f"""
            - **Mass**: `{m_solar:.2e} M_sun`
            - **Schwarzschild Radius ($r_s$)**: `{bh_info['schwarzschild_radius_km']:.2f} km`
            - **Photon Sphere ($r_{{ph}} = 1.5\\,r_s$)**: `{bh_info['photon_sphere_radius_km']:.2f} km`
            - **Critical Impact Parameter ($b_{{crit}}$)**: `{bh_info['critical_impact_parameter_km']:.2f} km` ($2.598\\,r_s$)
            - **ISCO Radius ($3.0\\,r_s$)**: `{bh_info['isco_radius_km']:.2f} km`
            - **Apparent Shadow Diameter**: `{bh_info['shadow_angular_diameter_factor']:.2f} r_s`
            """)

            st.markdown("##### ☄️ Ray Bundle Impact Parameters")
            b_list_str = st.text_input(
                "Impact Parameters b / r_s (comma-separated)",
                value="2.0, 2.3, 2.55, 2.65, 3.0, 4.0, 6.0, 9.0"
            )
            try:
                b_vals = [float(x.strip()) for x in b_list_str.split(",") if x.strip()]
            except ValueError:
                b_vals = [2.0, 2.4, 2.65, 3.0, 5.0]

        with bh_col2:
            st.markdown("##### 🪐 3D Geodesic Trajectories (Event Horizon & Photon Sphere)")
            fig_bh = plot_3d_black_hole_geodesics(b_values=b_vals)
            st.plotly_chart(fig_bh, use_container_width=True)

            st.markdown("##### 📷 Synthetic Black Hole Shadow & Photon Ring (2D Ray-Traced)")
            xx_bh, yy_bh, img_bh = generate_black_hole_image(grid_size=140, fov_rs=12.0)
            fig_shadow = go.Figure(data=go.Image(z=(img_bh * 255).astype(np.uint8)))
            fig_shadow.update_layout(
                title="Black Hole Shadow, Photon Ring, and Inner Accretion Flow",
                template="plotly_dark",
                paper_bgcolor="#1A2254",
                margin=dict(l=20, r=20, t=40, b=20),
                height=350,
                xaxis=dict(showticklabels=False),
                yaxis=dict(showticklabels=False)
            )
            st.plotly_chart(fig_shadow, use_container_width=True)

            # Scientific comparison: GR Deflection vs Weak-Field
            st.markdown("##### 📈 Scientific Validation: Exact GR Deflection vs. Weak-Field 1/b")
            comp_data = deflection_comparison_data([2.65, 2.8, 3.0, 3.5, 4.5, 6.0, 10.0, 15.0, 25.0])
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Scatter(
                x=comp_data["b_over_rs"], y=comp_data["gr_deflection_rad"],
                mode="lines+markers", line=dict(color="#00FFAA", width=2),
                name="Exact Numerical GR Deflection"
            ))
            fig_comp.add_trace(go.Scatter(
                x=comp_data["b_over_rs"], y=comp_data["weak_deflection_rad"],
                mode="lines", line=dict(color="#FF8800", width=2, dash="dash"),
                name="Weak-Field Approximation 2 r_s / b"
            ))
            fig_comp.update_layout(
                title="Relativistic Deflection Divergence near Photon Sphere",
                template="plotly_dark",
                paper_bgcolor="#1A2254",
                xaxis_title="Impact Parameter b / r_s",
                yaxis_title="Deflection Angle (radians)",
                height=320,
                margin=dict(l=40, r=20, t=40, b=40)
            )
            st.plotly_chart(fig_comp, use_container_width=True)

