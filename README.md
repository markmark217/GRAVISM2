# GRAVISIM: Interactive Gravitational Lensing Simulation and Computational Physics Laboratory

**GRAVISIM** is a high-performance computational physics platform developed in Python for physics education, undergraduate thesis research, and astrophysical visualization of gravitational lensing phenomena.

---

## 🌌 Key Capabilities & Architecture

- **Physics Engine (`physics/`)**:
  - Independent implementations of weak-field light deflection, Einstein radius, 1D & 2D point-mass lens equation solvers, and analytical magnifications.
  - Multi-profile support: Point Mass, Singular Isothermal Sphere (SIS), Singular Isothermal Ellipsoid (SIE), Binary Lens, and Galaxy Cluster potential with subhalos.
  - Full Flat $\Lambda\text{CDM}$ cosmological distance integrator ($D_L, D_S, D_{LS}, D_{\Delta t}$).
  - Gravitational time delays and Fermat potential calculations.

- **General Relativity Extension (`relativity/`)**:
  - Non-rotating Schwarzschild black hole geometry ($r_s, r_{ph}, b_{crit}, r_{isco}$).
  - Numerical integration of null geodesics via Runge-Kutta ODE solvers (`solve_ivp`).
  - Strong-field relativistic light deflection and Bozza logarithmic divergence.
  - 2D ray-traced black hole shadow and photon ring synthesis.

- **Interactive Simulation Engine (`simulation/`)**:
  - 2D backward ray tracing based on Liouville's theorem (surface brightness conservation).
  - Dynamic computation of numerical Jacobian matrices, local convergence ($\kappa$), shear ($\gamma$), critical curves, and caustic mapping.
  - Multiple background source models: Gaussian profiles, Sersic galaxy profiles, and uniform disks.

- **2D & 3D Scientific Visualization (`visualization/`)**:
  - Publication-quality interactive Plotly 2D image-plane and source-plane visualizers.
  - 3D spacetime curvature embedding surfaces ("rubber sheet" potential wells with scientific disclaimers).
  - 3D optical bench ray paths tracing from observer to source across cosmological megaparsec distances.
  - 3D Schwarzschild null geodesics displaying photon capture vs relativistic escape.

- **Astronomical Database (`data/`)**:
  - Curated database of observed gravitational lenses: *Q2237+0305 (Einstein's Cross)*, *SDSS J0946+1006 (Cosmic Horseshoe)*, *SDSS J1004+4112*, *MACS J1149.5+2223 (Refsdal)*, *M87\**, and *Sagittarius A\**.
  - Astropy FITS image loader and header metadata viewer.
  - Real observation matching with simulated models.

- **Scientific Analysis & Validation Laboratory (`analysis/`)**:
  - Precision deflection and Einstein radius calculators.
  - Grid resolution convergence tests ($N \times N$) verifying numerical stability.
  - Formal Thesis Validation Test Suite verifying:
    - Test 1: Mass dependence ($\theta_E \propto \sqrt{M}$)
    - Test 2: Impact parameter dependence ($\hat{\alpha} \propto 1/b$)
    - Test 3: Source alignment and Einstein ring convergence ($\beta \to 0$)
    - Test 4: Image position exact matching
    - Test 5: Analytical magnification identity ($\mu_+ - \mu_- = 1$)
    - Test 7: Schwarzschild null geodesic capture threshold ($b_{crit} = \frac{3\sqrt{3}}{2} r_s$)

- **Storage & Reproducibility (`storage/`)**:
  - SQLite local database for simulation configurations.
  - Export simulation parameters to JSON, image tables to CSV, and research reports to Markdown.

---

## 🛠️ Installation & Quick Start

1. Install required dependencies:
```bash
python -m pip install -r requirements.txt
```

2. Run the interactive Streamlit application:
```bash
python -m streamlit run main.py
```

3. Run the automated scientific pytest test suite:
```bash
python -m pytest tests/
```

---

## 🎨 Visual Identity & Technical Standards

Built according to the visual and scientific guidelines in `GravitationalLensingFUnction.md`:
- **Primary Dark Blue**: `#2E3A8C` (Main interface & primary elements)
- **Light Blue**: `#4A5FD9` (Secondary highlights & rays)
- **Navy**: `#1A2254` (Dark background & cards)
- **White**: `#FFFFFF` (Scientific contrast & labels)
- **Typography**: Inter with full KaTeX LaTeX scientific typography.
- **Physical Constants**: IAU / CODATA recommended standards ($G = 6.67430 \times 10^{-11}\,\text{m}^3\,\text{kg}^{-1}\,\text{s}^{-2}$, $c = 2.99792458 \times 10^8\,\text{m/s}$).

