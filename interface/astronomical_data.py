"""
GRAVISIM: Astronomical Data and Observational Database
======================================================

Curated database of observed gravitational lenses and compact objects,
FITS image reader, and observational comparison tools.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from data.catalog import ASTRONOMICAL_CATALOG, get_catalog_dataframe, get_object_by_id
from data.fits_loader import read_fits_data, create_sample_fits_buffer
from simulation.galaxy_lens import GalaxyLensSimulation
from simulation.cluster_lens import ClusterLensSimulation
from visualization.plots_2d import plot_lensed_system_2d


def render_astronomical_data():
    st.markdown("### 🔭 Astronomical Catalog & Observational Comparison")
    st.write(
        "Connect theoretical lensing simulations with empirical observational astronomy "
        "from NASA/NED, ESA/Hubble, MAST, and the Event Horizon Telescope."
    )

    tab_cat, tab_fits, tab_comp = st.tabs([
        "1. Real Gravitational Lenses Catalog",
        "2. FITS Astronomical Data Loader",
        "3. Observation vs. Simulation Matching"
    ])

    with tab_cat:
        st.markdown("#### 🌟 Observed Strong Lensing Systems Catalog")
        df_cat = get_catalog_dataframe()

        # Display catalog summary table
        cols_to_show = ["id", "name", "lensType", "zLens", "zSource", "estimatedMassSolar", "einsteinRadiusArcsec", "survey"]
        st.dataframe(df_cat[cols_to_show], use_container_width=True)

        st.markdown("##### 🔍 Object Inspector")
        obj_names = [f"{o['id']}: {o['name']}" for o in ASTRONOMICAL_CATALOG]
        selected_name = st.selectbox("Select Astronomical Object", options=obj_names)
        sel_id = selected_name.split(":")[0]
        obj = get_object_by_id(sel_id)

        if obj:
            c1, c2 = st.columns([6, 6])
            with c1:
                st.markdown(f"### {obj['name']}")
                st.markdown(f"**Classification:** {obj['objectType']} ({obj['lensType']})")
                st.markdown(f"**Description:** {obj['description']}")
                st.markdown(f"**Sky Coordinates (J2000):** RA `{obj['rightAscensionDeg']:.4f}°`, Dec `{obj['declinationDeg']:.4f}°`")
                if obj["zLens"] is not None:
                    st.markdown(f"**Lens Redshift ($z_L$):** `{obj['zLens']}` | **Source Redshift ($z_S$):** `{obj['zSource']}`")
                if obj["estimatedMassSolar"]:
                    unc = f" ± {obj['massUncertaintySolar']:.1e}" if obj['massUncertaintySolar'] else ""
                    st.markdown(f"**Estimated Mass:** `{obj['estimatedMassSolar']:.2e}{unc} M_sun`")
                if obj["einsteinRadiusArcsec"]:
                    st.markdown(f"**Observed Einstein Radius ($\\theta_E$):** `{obj['einsteinRadiusArcsec']:.2f} arcsec`")

            with c2:
                st.markdown("#### 📜 Provenance & Citation")
                st.markdown(f"**Survey / Telescope:** {obj['survey']}")
                st.markdown(f"**Observation Date:** {obj['observationDate']}")
                st.markdown(f"**Citation:** *{obj['citation']}*")
                st.markdown(f"**Public Archive:** [{obj['sourceUrl']}]({obj['sourceUrl']})")

                if st.button(f"🚀 Load {obj['name']} into Simulator", use_container_width=True):
                    st.session_state["preset_model"] = obj["recommendedModel"]
                    st.session_state["active_tab"] = "2D Simulation"
                    st.rerun()

    with tab_fits:
        st.markdown("#### 📁 FITS Astronomical Image Reader")
        st.write(
            "Upload raw astronomical Flexible Image Transport System (.fits) data files "
            "to inspect headers, pixel photometry, and image planes."
        )

        sample_buf = create_sample_fits_buffer("Einstein_Cross_HST_WFC3")
        st.download_button(
            "⬇️ Download Sample FITS File (Einstein Cross)",
            data=sample_buf,
            file_name="sample_einstein_cross.fits",
            mime="application/octet-stream"
        )

        uploaded_fits = st.file_uploader("Upload FITS File (.fits)", type=["fits", "fit", "fts"])

        fits_to_parse = uploaded_fits if uploaded_fits else sample_buf
        if fits_to_parse:
            fits_res = read_fits_data(fits_to_parse)
            if fits_res["success"]:
                f_data = fits_res["data"]
                f_hdr = fits_res["header"]
                f_stats = fits_res["stats"]

                col_fimg, col_fmeta = st.columns([7, 5])
                with col_fimg:
                    fig_f = go.Figure(data=go.Heatmap(z=f_data, colorscale="Viridis"))
                    fig_f.update_layout(
                        title=f"FITS Image Plane ({f_stats['shape'][0]} x {f_stats['shape'][1]})",
                        template="plotly_dark",
                        paper_bgcolor="#1A2254",
                        height=420
                    )
                    st.plotly_chart(fig_f, use_container_width=True)

                with col_fmeta:
                    st.markdown("##### 📊 Photometric Statistics")
                    st.write(f"- **Dimensions**: {f_stats['shape']}")
                    st.write(f"- **Minimum Flux**: {f_stats['min']:.2f}")
                    st.write(f"- **Maximum Flux**: {f_stats['max']:.2f}")
                    st.write(f"- **Mean Flux**: {f_stats['mean']:.2f}")

                    st.markdown("##### 🏷️ Primary Header Keywords")
                    hdr_df = pd.DataFrame(list(f_hdr.items()), columns=["Keyword", "Value"])
                    st.dataframe(hdr_df.head(15), height=250, use_container_width=True)
            else:
                st.error(f"Error parsing FITS file: {fits_res.get('error')}")

    with tab_comp:
        st.markdown("#### ⚖️ Real Observation vs. Analytical Lens Modeling")
        st.write(
            "Compare the idealized parametric model of **Q2237+0305 (Einstein's Cross)** with the simulated quadrupole image."
        )

        sim_cross = GalaxyLensSimulation(
            is_elliptical=True,
            theta_e_arcsec=0.89,
            axis_ratio_q=0.74,
            orientation_deg=45.0,
            source_x=0.04,
            source_y=0.03,
            source_radius=0.12,
            resolution=140
        ).run()

        fig_cross = plot_lensed_system_2d(sim_cross)
        st.plotly_chart(fig_cross, use_container_width=True)

        st.markdown("""
        **Physics Comparison Analysis:**
        - **Image Multiplicity**: Produces 4 distinct images located on a ring-like quadrupole caustic crossing.
        - **Parity**: 2 images correspond to positive-parity local minima of Fermat potential; 2 correspond to negative-parity saddle points.
        - **Microlensing Note**: Individual stars in the foreground spiral core (ZW 2237+030) induce micro-caustic crossings, causing independent variability of the 4 quasar components over months.
        """)

