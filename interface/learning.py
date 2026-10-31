"""
GRAVISIM: Learning, Tutorials, and Research Laboratory
=====================================================

Educational computational physics laboratory featuring:
- 5 Structured Learning Modules with mathematical foundations
- Interactive Guided Experiments
- Knowledge Assessment Quizzes
- Student Research Notebook and Report Generator
"""

import streamlit as st
import numpy as np
import pandas as pd
from storage.exports import generate_experiment_markdown_report


def render_learning():
    st.markdown("### 🎓 Learning Center & Research Laboratory")
    st.write(
        "Structured physics education modules, interactive experiments, "
        "and self-guided research activities in gravitational astrophysics."
    )

    tab_modules, tab_exp, tab_quiz, tab_notebook = st.tabs([
        "1. Physics Learning Modules",
        "2. Guided Experiments",
        "3. Knowledge Assessment",
        "4. Research Notebook"
    ])

    with tab_modules:
        st.markdown("#### 📚 Theoretical Curriculum")

        mod = st.selectbox(
            "Select Curriculum Module",
            options=[
                "Module 1: Introduction to General Relativity",
                "Module 2: Gravitational Lensing Fundamentals",
                "Module 3: Mathematical Foundations of Lensing",
                "Module 4: Computational Physics & Ray Tracing",
                "Module 5: Advanced Lensing, Caustics & Schwarzschild"
            ]
        )

        if "Module 1" in mod:
            st.markdown("""
            ### Module 1: Introduction to General Relativity
            #### 1. The Equivalence Principle
            Albert Einstein formulated the Principle of Equivalence in 1907: locally, the physical effects of a uniform gravitational field are completely indistinguishable from the effects of uniform acceleration. A direct consequence is that light must curve in a gravitational field.

            #### 2. Spacetime Curvature
            In General Relativity (1915), gravity is not an attractive Newtonian force acting across empty space. Instead, mass and energy curve four-dimensional spacetime according to the Einstein Field Equations:
            $$G_{\\mu\\nu} + \\Lambda g_{\\mu\\nu} = \\frac{8\\pi G}{c^4} T_{\\mu\\nu}$$

            #### 3. Geodesic Motion
            Free-falling particles follow **geodesics** (curves of extremal proper time). Light rays follow **null geodesics** where the spacetime interval $ds^2 = 0$.
            """)

        elif "Module 2" in mod:
            st.markdown("""
            ### Module 2: Gravitational Lensing Fundamentals
            #### 1. Light Deflection Angle
            When a photon passes a point mass $M$ with impact parameter $b$, its weak-field deflection is:
            $$\\hat{\\alpha} = \\frac{4GM}{c^2 b}$$
            *Note:* This is exactly twice the Newtonian prediction ($2GM / c^2 b$) because spatial curvature contributes equally to time dilation in bending the null trajectory.

            #### 2. The Einstein Ring
            When a background light source, foreground deflector, and observer are in collinear alignment:
            $$\\theta_E = \\sqrt{\\frac{4GM}{c^2} \\frac{D_{LS}}{D_L D_S}}$$
            The source is imaged into an unbroken ring of angular radius $\\theta_E$.
            """)

        elif "Module 3" in mod:
            st.markdown("""
            ### Module 3: Mathematical Foundations of Lensing
            #### 1. The Lens Equation
            In angular coordinates, the mapping from image plane $\\vec{\\theta}$ to source plane $\\vec{\\beta}$ is:
            $$\\vec{\\beta} = \\vec{\\theta} - \\vec{\\alpha}(\\vec{\\theta})$$

            #### 2. The Jacobian Matrix & Magnification
            The local deformation of an image element is described by the Jacobian matrix $A$:
            $$A = \\frac{\\partial\\vec{\\beta}}{\\partial\\vec{\\theta}} = \\begin{pmatrix} 1 - \\frac{\\partial\\alpha_x}{\\partial\\theta_x} & -\\frac{\\partial\\alpha_x}{\\partial\\theta_y} \\\\ -\\frac{\\partial\\alpha_y}{\\partial\\theta_x} & 1 - \\frac{\\partial\\alpha_y}{\\partial\\theta_y} \\end{pmatrix}$$
            Gravitational magnification $\\mu$ is given by:
            $$\\mu = \\frac{1}{\\det A}$$
            """)

        elif "Module 4" in mod:
            st.markdown("""
            ### Module 4: Computational Physics & Ray Tracing
            #### 1. Backward Ray Tracing & Liouville's Theorem
            In gravitational lensing, forward ray tracing from source to observer is computationally inefficient because most emitted photons do not enter the observer's aperture. Instead, we use **backward ray tracing**:
            1. Generate a regular 2D grid in the image plane $(\\theta_x, \\theta_y)$.
            2. Compute the deflection field $\\vec{\\alpha}(\\vec{\\theta})$.
            3. Map backward to source coordinates $\\vec{\\beta} = \\vec{\\theta} - \\vec{\\alpha}$.
            4. By Liouville's theorem, surface brightness is conserved along rays:
            $$I_\\text{image}(\\vec{\\theta}) = I_\\text{source}(\\vec{\\beta})$$
            """)

        elif "Module 5" in mod:
            st.markdown("""
            ### Module 5: Advanced Lensing, Caustics & Schwarzschild
            #### 1. Critical Curves and Caustics
            - **Critical Curves**: Lines in the image plane where $\\det A = 0$, producing formally infinite magnification for point sources.
            - **Caustics**: The mapping of critical curves into the source plane $\\vec{\\beta}_\\text{caustic} = \\vec{\\theta}_\\text{crit} - \\vec{\\alpha}(\\vec{\\theta}_\\text{crit})$. When a background source crosses a caustic boundary, the image multiplicity changes by $\\pm 2$ (e.g. 1 image $\\to$ 3 images, or 3 images $\\to$ 5 images).

            #### 2. Relativistic Photon Sphere
            In Schwarzschild geometry, photons orbiting at $r = 1.5\\,r_s = \\frac{3GM}{c^2}$ occupy the **photon sphere**, an unstable circular orbit. Any photon with impact parameter $b < b_\\text{crit} = \\frac{3\\sqrt{3}}{2} r_s \\approx 2.598\\,r_s$ is captured across the event horizon.
            """)

    with tab_exp:
        st.markdown("#### 🔬 Guided Student Experiments")

        exp_choice = st.selectbox(
            "Select Experiment Template",
            options=[
                "Experiment 1: Mass Dependence of the Einstein Radius",
                "Experiment 2: Alignment and Einstein Ring Formation",
                "Experiment 3: Galaxy Cluster Arc Formation",
                "Experiment 4: Black Hole Relativistic Photon Capture"
            ]
        )

        if "Experiment 1" in exp_choice:
            st.markdown("""
            **Research Question:** How does deflector mass affect the observed angular scale of an Einstein ring?  
            **Hypothesis:** $\\theta_E \\propto \\sqrt{M}$. Quadrupling the mass should exactly double $\\theta_E$.  
            **Procedure:**
            1. Navigate to **2D Simulation** with Point-Mass lens.
            2. Record $\\theta_E$ at $M = 10^{11}\\,M_\\odot$.
            3. Increase mass to $4 \\times 10^{11}\\,M_\\odot$ and verify ratio is $2.0$.
            """)
        elif "Experiment 2" in exp_choice:
            st.markdown("""
            **Research Question:** What happens to image geometry and total magnification as a background source approaches perfect alignment?  
            **Hypothesis:** As $\\beta \\to 0$, the two distinct images stretch tangentially and merge into a closed Einstein ring, with magnification diverging asymptotically.
            """)
        elif "Experiment 3" in exp_choice:
            st.markdown("""
            **Research Question:** Why do massive galaxy clusters produce giant curved arcs rather than symmetric rings?  
            **Hypothesis:** The superposition of a broad cluster halo potential with discrete galaxy subhalos breaks radial symmetry, creating extended critical curves and fold caustics.
            """)
        elif "Experiment 4" in exp_choice:
            st.markdown("""
            **Research Question:** What is the critical impact parameter separating photon capture from escape in Schwarzschild spacetime?  
            **Hypothesis:** Photons with $b < 2.598\\,r_s$ fall into the event horizon, while photons with $b > 2.598\\,r_s$ escape after experiencing strong relativistic deflection.
            """)

    with tab_quiz:
        st.markdown("#### 📝 Knowledge Assessment Quiz")

        q1 = st.radio(
            "1. Why is the general relativistic deflection of light twice the Newtonian corpuscular value?",
            options=[
                "Because of gravitational redshift",
                "Because spatial curvature and temporal curvature contribute equally",
                "Because photons carry mass according to E=mc^2",
                "Because light speed decreases near a star"
            ]
        )

        q2 = st.radio(
            "2. For a point-mass gravitational lens, what is the value of the magnification difference mu_+ - mu_-?",
            options=[
                "Always equal to 0",
                "Always equal to 1",
                "Proportional to the Einstein radius",
                "Depends on cosmological redshift"
            ]
        )

        q3 = st.radio(
            "3. At what radius is the photon sphere located for a Schwarzschild black hole of radius r_s?",
            options=[
                "r = 0.5 r_s",
                "r = 1.0 r_s",
                "r = 1.5 r_s",
                "r = 3.0 r_s"
            ]
        )

        if st.button("Check Answers"):
            score = 0
            if q1 == "Because spatial curvature and temporal curvature contribute equally":
                st.success("Q1: Correct! General relativity's curved spatial metric doubles the deflection.")
                score += 1
            else:
                st.error("Q1: Incorrect. In GR, both g_00 and g_rr contribute equally to null geodesic bending.")

            if q2 == "Always equal to 1":
                st.success("Q2: Correct! Analytical identity mu_+ - mu_- = 1 holds for all beta > 0.")
                score += 1
            else:
                st.error("Q2: Incorrect. The analytical identity is mu_+ - mu_- = 1.")

            if q3 == "r = 1.5 r_s":
                st.success("Q3: Correct! The photon sphere is at r_ph = 1.5 r_s = 3GM/c^2.")
                score += 1
            else:
                st.error("Q3: Incorrect. The photon sphere is at 1.5 r_s.")

            st.metric("Total Score", f"{score} / 3")

    with tab_notebook:
        st.markdown("#### 📓 Scientific Research Notebook")
        st.write("Record your experimental observations and export a structured Markdown thesis report.")

        nb_title = st.text_input("Experiment Title", value="Verification of Point-Mass Einstein Radius Scaling")
        nb_hypo = st.text_area("Hypothesis", value="The Einstein radius scales as the square root of deflector mass.")
        nb_obs = st.text_area("Observations", value="Measured theta_E = 1.43 arcsec at 1e11 M_sun and 2.86 arcsec at 4e11 M_sun.")
        nb_disc = st.text_area("Conclusions", value="Confirmed sqrt(M) scaling with zero numerical divergence.")

        rep_md = generate_experiment_markdown_report(
            title=nb_title,
            hypothesis=nb_hypo,
            model_type="Point-Mass Theoretical",
            parameters={"Mass": "1e11 to 4e11 M_sun", "Distance": "1000 Mpc"},
            results={"Ratio": 2.000000, "Relative Error": "0.00%"},
            conclusions=nb_disc
        )

        st.download_button(
            "📥 Download Research Report (.md)",
            data=rep_md,
            file_name="gravisim_research_report.md",
            mime="text/markdown",
            use_container_width=True
        )

