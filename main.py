"""
GRAVISIM: Interactive Gravitational Lensing Simulation and Computational Physics Laboratory
===========================================================================================

Main Streamlit Application Entrypoint.
Conforms to specifications in Gravitational.md and GravitationalLensingFUnction.md.
"""

import streamlit as st

# Configure wide layout and page metadata
st.set_page_config(
    page_title="GRAVISIM: Gravitational Lensing Laboratory",
    page_icon="🔭",
    layout="wide",
    initial_sidebar_state="expanded"
)

from interface.styles import apply_custom_styles
from interface.dashboard import render_dashboard
from interface.simulation_2d import render_2d_simulation
from interface.visualization_3d import render_3d_visualization
from interface.astronomical_data import render_astronomical_data
from interface.analysis_lab import render_analysis_lab
from interface.learning import render_learning


def main():
    # Inject design system styling
    apply_custom_styles()

    # Application Header
    st.markdown("""
    <div class="gravisim-header">
        <div>
            <h1 class="gravisim-title">🔭 GRAVISIM</h1>
            <div class="gravisim-subtitle">
                Interactive Gravitational Lensing Simulation & Computational Physics Laboratory
            </div>
        </div>
        <div style="text-align: right;">
            <span class="badge-pill badge-green">Engine Online</span>
            <span class="badge-pill" style="margin-left: 6px;">v1.0.0 Thesis</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Initialize navigation state
    if "active_tab" not in st.session_state:
        st.session_state["active_tab"] = "Dashboard"

    # Sidebar Navigation and Global Settings
    with st.sidebar:
        st.markdown("### 🎛️ Navigation & Global Settings")

        tabs_list = [
            "Dashboard",
            "2D Simulation",
            "3D Visualization",
            "Astronomical Data",
            "Analysis Laboratory",
            "Learning & Research"
        ]

        # Sync selectbox with session state
        curr_idx = tabs_list.index(st.session_state["active_tab"]) if st.session_state["active_tab"] in tabs_list else 0
        selected_nav = st.radio("Navigation", options=tabs_list, index=curr_idx)
        st.session_state["active_tab"] = selected_nav

        st.markdown("---")
        st.markdown("#### ⚙️ Simulation Mode")
        sim_mode = st.selectbox(
            "Curriculum / Complexity Mode",
            options=["Basic (Educational)", "Intermediate (Astrophysics)", "Advanced (Research & GR)"],
            index=1
        )

        st.markdown("#### 📏 Unit Convention")
        units = st.radio("Display Units", options=["Astronomical (M_sun, Mpc, arcsec)", "SI Metric (kg, m, rad)"])

        st.markdown("---")
        st.markdown("#### ℹ️ Physical Constants")
        st.caption("""
        - **G**: `6.67430e-11 m^3 kg^-1 s^-2`
        - **c**: `2.99792e8 m s^-1`
        - **M_sun**: `1.98847e30 kg`
        - **1 rad**: `206,264.8 arcsec`
        - **H0**: `70.0 km s^-1 Mpc^-1`
        """)

        st.markdown("---")
        if st.button("🔄 Reset Simulation Session", use_container_width=True):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    # Route to Selected Laboratory Tab
    tab = st.session_state["active_tab"]

    if tab == "Dashboard":
        render_dashboard()
    elif tab == "2D Simulation":
        render_2d_simulation()
    elif tab == "3D Visualization":
        render_3d_visualization()
    elif tab == "Astronomical Data":
        render_astronomical_data()
    elif tab == "Analysis Laboratory":
        render_analysis_lab()
    elif tab == "Learning & Research":
        render_learning()


if __name__ == "__main__":
    main()

