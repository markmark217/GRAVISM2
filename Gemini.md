# GRAVISIM: Interactive Gravitational Lensing Simulation and Computational Physics Laboratory

## 1. Project Overview

### Project Title

**GRAVISIM: Development of an Interactive Computational Simulation of Gravitational Lensing Using Python for Physics Education and Astrophysical Visualization**

### Project Description

GRAVISIM is a Python-based computational physics application designed to simulate, visualize, analyze, and explain gravitational lensing. It allows users to investigate how massive astronomical objects bend light and affect the appearance, position, brightness, and shape of distant light sources.

The application combines gravitational physics, numerical computation, astronomy, data visualization, and educational tools.

Users can:
- Simulate gravitational lensing in 2D.
- Explore interactive 3D visualizations of gravitational fields and light paths.
- Adjust the mass and position of lensing objects.
- Change the distance between the observer, lens, and source.
- Observe Einstein rings, multiple images, arcs, and magnification.
- Compare point-mass, galaxy, galaxy-cluster, and black-hole models.
- Explore gravitational lensing using astronomical observations and publicly available data.
- Analyze numerical results through graphs, tables, and scientific measurements.
- Learn the mathematical and physical principles behind each simulation.

### Main Research Goal

To develop and evaluate an interactive computational simulation that demonstrates gravitational lensing through numerical modeling, 2D and 3D visualization, and comparison with established theoretical predictions and available astronomical observations.

---

# 2. Navigation Structure

## Main Navigation Tabs

1. **Dashboard** – Overview of the simulation and project.
2. **2D Simulation** – Interactive gravitational-lensing simulations.
3. **3D Visualization** – Three-dimensional gravitational fields and light paths.
4. **Astronomical Data** – Real astronomical data and object information.
5. **Analysis Laboratory** – Scientific calculations, graphs, and numerical experiments.
6. **Learning & Research** – Physics explanations, tutorials, experiments, and research documentation.

## Header Elements

- Dark and light mode.
- Application settings.
- Search for astronomical objects and simulation models.
- Simulation notifications and computation status.
- Current simulation mode.
- Help and documentation.
- About the project.
- Export and save simulation results.

---

# 3. Dashboard Page

The Dashboard serves as the main control center.

## A. Main Information Cards

### Card 1: Current Lens Model
- Display the selected lens model.
- Examples: Point Mass, Galaxy, Galaxy Cluster, Binary Lens, Black Hole.
- Show the number of active lensing objects.
- Display the current model's assumptions.

### Card 2: Einstein Radius
- Display the calculated Einstein angle.
- Show its value in arcseconds or radians.
- Update automatically when mass or distance changes.
- Explain what the Einstein radius represents.

### Card 3: Light Deflection
- Display the calculated deflection angle.
- Show the deflection in radians or arcseconds.
- Compare the deflection at different impact parameters.

### Card 4: Magnification
- Display the calculated magnification.
- Show whether the source appears brighter or fainter.
- Display the number of predicted images when applicable.
- Explain the relationship between magnification and alignment.

## B. Simulation Preview

Display a small preview of the current gravitational-lensing simulation.

Include:
- Background source.
- Foreground lensing object.
- Observer position.
- Deflected light paths.
- Image positions.
- Einstein ring when the geometry produces one.

Allow users to open the full simulation.

## C. Simulation Activity

Display:
- Recently opened simulations.
- Saved simulation configurations.
- Recently used lens models.
- Previous numerical experiments.
- Last computed results.

## D. Quick Simulation Controls

Provide shortcuts for:
- Point-mass lens.
- Einstein ring.
- Multiple-image formation.
- Galaxy lens.
- Binary lens.
- Black-hole visualization.

## E. Scientific Information Panel

Display useful information about:
- Gravitational lensing.
- General relativity.
- Gravitational deflection of light.
- Dark matter and gravitational lensing.
- Strong and weak lensing.
- Microlensing.
- Einstein rings and Einstein crosses.

---

# 4. 2D Simulation Page

This is the primary simulation environment and should be fully functional in the first major version.

## A. Simulation Canvas

Display a two-dimensional simulation of gravitational lensing.

### Required visual elements
- Observer.
- Background light source.
- Foreground lensing object.
- Optical axis.
- Image plane.
- Source plane.
- Deflected light rays.
- Predicted image positions.
- Einstein ring.
- Coordinate grid.
- Angular scale.

Users should be able to:
- Zoom in and out.
- Move the simulation view.
- Select the lensing object.
- Move the source position.
- Change the lens position.
- Toggle coordinate grids.
- Show or hide individual light paths.
- Reset the simulation.

## B. Lens Model Selection

Provide these lensing models:

### 1. Point-Mass Lens
- Model a compact object as a point mass.
- Calculate its Einstein radius.
- Calculate light deflection.
- Determine image positions.
- Calculate image magnification.
- Demonstrate the formation of an Einstein ring.

### 2. Extended Mass Distribution
- Model a lens with a spatially distributed mass.
- Display surface mass density.
- Calculate convergence.
- Calculate deflection angles.
- Display magnification maps.

### 3. Singular Isothermal Sphere (SIS)
- Simulate an idealized galaxy-scale lens.
- Adjust velocity dispersion.
- Calculate Einstein radius.
- Show multiple images and arcs.

### 4. Elliptical Galaxy Lens
- Simulate a non-spherical galaxy mass distribution.
- Adjust ellipticity and orientation.
- Display distorted background sources.
- Demonstrate arc and multiple-image formation.

### 5. Binary Lens
- Simulate two gravitational lensing objects.
- Adjust the mass ratio.
- Change their separation.
- Move the source.
- Display caustics and critical curves.
- Demonstrate microlensing behavior.

### 6. Galaxy Cluster Lens
- Simulate a massive galaxy cluster.
- Display an extended mass distribution.
- Demonstrate strong lensing arcs.
- Include an optional simplified dark-matter component.

## C. Adjustable Simulation Parameters

Users must be able to modify the following:

| Parameter | Description |
|---|---|
| Lens mass | Mass of the foreground object |
| Source position | Position of the background source |
| Lens position | Position of the lens |
| Observer-lens distance | Distance from observer to lens |
| Observer-source distance | Distance from observer to source |
| Lens-source distance | Distance between lens and source |
| Impact parameter | Closest distance of the light ray to the lens |
| Source radius | Physical or angular size of the source |
| Source brightness | Initial brightness of the source |
| Lens ellipticity | Shape of the lens mass distribution |
| Mass ratio | Relative masses in a binary lens |
| Lens orientation | Orientation of the lens model |
| Grid resolution | Number of computational points |

All parameters must have appropriate physical units and valid numerical ranges.

## D. Simulation Results

Display:
- Deflection angle.
- Einstein radius.
- Image positions.
- Number of images.
- Magnification.
- Source-plane coordinates.
- Image-plane coordinates.
- Critical curves.
- Caustics.
- Convergence maps.
- Magnification maps.

## E. Simulation Modes

### Mode 1: Basic
For students learning the fundamentals.

### Mode 2: Intermediate
For users exploring multiple images, magnification, and extended mass distributions.

### Mode 3: Advanced
For users studying caustics, numerical ray tracing, binary lenses, and complex mass distributions.

---

# 5. 3D Visualization Page

This is one of the main features that makes GRAVISIM visually interesting for demonstrations and research competitions.

## A. Three-Dimensional Spacetime Visualization

Display a three-dimensional representation of gravitational-field geometry.

Include:
- A grid representing a conceptual spatial slice.
- A massive object positioned in the visualization.
- A deformation of the grid around the object.
- A visual representation of the gravitational field.
- A coordinate system.
- An adjustable mass parameter.

Users can:
- Rotate the 3D view.
- Zoom in and out.
- Change the viewing angle.
- Increase or decrease the displayed mass.
- Change the object's position.
- Compare different mass configurations.

**Scientific note:** The familiar stretched-grid or rubber-sheet visualization is an explanatory representation, not a complete solution of Einstein's field equations. The application must label it accordingly.

## B. Three-Dimensional Light-Path Visualization

Display light paths in three dimensions.

Include:
- Observer.
- Background source.
- Lensing object.
- Light trajectory.
- Deflection region.
- Coordinate axes.
- Optional spacetime visualization.

Users can:
- Change the source position.
- Change the lens mass.
- Adjust the impact parameter.
- Display multiple light rays.
- Compare straight-line and deflected paths.
- Animate the light trajectory.

For the standard lensing model, this should be a geometrical visualization of the lens equation and ray mapping. It must not be presented as a full relativistic ray-tracing calculation.

## C. Black-Hole Visualization

Create a dedicated black-hole mode.

Display:
- Black-hole mass.
- Schwarzschild radius.
- Photon-sphere radius.
- Event-horizon boundary.
- Light trajectories.
- Strong gravitational deflection.
- Optional photon-ring visualization.

Adjustable parameters:
- Black-hole mass.
- Initial photon position.
- Initial photon direction.
- Impact parameter.
- Observer distance.
- Integration resolution.

### Advanced General Relativity Extension

Implement numerical integration of null geodesics in the Schwarzschild spacetime.

This mode must be separated from the weak-field thin-lens model.

The application should distinguish:
1. Weak-field gravitational lensing.
2. Strong-field gravitational lensing near a compact object.
3. Schwarzschild null-geodesic ray tracing.

Do not use the weak-field point-mass equation as an accurate model of light paths near the event horizon.

## D. 3D Mass Distribution

Display different mass distributions:
- Point mass.
- Spherical mass distribution.
- Elliptical galaxy.
- Binary lens.
- Galaxy cluster.

Allow users to change the mass distribution and compare the resulting gravitational-lensing patterns.

---

# 6. Astronomical Data Page

This page connects the simulation to real astronomy.

The system should use free or openly accessible astronomical data wherever possible.

## A. Astronomical Object Database

Store information about selected objects.

### Required object information

- Object ID.
- Object name.
- Object type.
- Right ascension.
- Declination.
- Redshift, if available.
- Estimated mass, if available.
- Mass uncertainty, if available.
- Distance or cosmological distance information.
- Image or observation file reference.
- Telescope or survey.
- Observation date.
- Data source.
- Data access URL.
- Citation or attribution.
- Data-license or reuse information, where applicable.

### Object categories

- Stars.
- Planets.
- Black holes.
- Galaxies.
- Galaxy clusters.
- Quasars.
- Gravitational-lens systems.
- Supernovae.
- Other relevant astronomical objects.

**Important:** Not every object has a measured mass, redshift, or distance. Missing values must be stored as unknown rather than invented. Planets can be included as educational examples or as possible microlensing objects, but galaxy-scale lensing and observed strong-lens systems should be the primary astronomical focus.

## B. Free Astronomical Data Sources

Use these sources as the starting data catalog:

1. **NASA/IPAC Extragalactic Database (NED)** – Extragalactic object information and literature references.
   https://ned.ipac.caltech.edu/

2. **Mikulski Archive for Space Telescopes (MAST)** – Astronomical observations and mission data, including Hubble-related data.
   https://archive.stsci.edu/

3. **ESA/Hubble** – Public astronomy images and information.
   https://esahubble.org/

4. **Sloan Digital Sky Survey (SDSS)** – Images, spectra, and astronomical catalogs.
   https://www.sdss.org/

5. **NASA Exoplanet Archive** – Planetary-system data for optional astronomy demonstrations.
   https://exoplanetarchive.ipac.caltech.edu/

6. **Astropy** – Python tools for astronomy, physical units, coordinates, and cosmological calculations.
   https://www.astropy.org/

7. **lenstronomy** – An established open-source lens-modeling package for independent comparison and validation.
   https://lenstronomy.readthedocs.io/

## C. Data Import

Support:
- CSV files.
- FITS astronomical images.
- JSON metadata.
- Manually entered simulation parameters.
- Publicly accessible catalog data.

## D. Data Management

For every imported dataset, save:
- Original source.
- Object identification.
- File format.
- Download or access date.
- Units.
- Coordinate system.
- Redshift information.
- Measurement uncertainty.
- Processing steps.
- Attribution and usage conditions.

Never silently replace missing observations with assumed values.

## E. Real Observation Comparison

Where a suitable gravitational-lens observation is available:
- Display the original observation.
- Display the simulated lensing result.
- Compare image positions and shapes.
- Identify differences between the idealized model and the observation.
- Record model assumptions and possible sources of error.

The first version may use selected public observations instead of attempting to automatically download every astronomical image.

---

# 7. Analysis Laboratory Page

This page is the scientific analysis center of GRAVISIM.

## A. Gravitational Deflection Calculator

Calculate the weak-field deflection angle:

\[
\hat{\alpha}=\frac{4GM}{c^2b}
\]

Inputs:
- Lens mass.
- Impact parameter.

Outputs:
- Deflection angle in radians.
- Deflection angle in arcseconds.
- Comparison with a reference example.

## B. Einstein Radius Calculator

Calculate:

\[
\theta_E=
\sqrt{
\frac{4GM}{c^2}
\frac{D_{LS}}{D_LD_S}
}
\]

Inputs:
- Lens mass.
- Observer-to-lens angular-diameter distance.
- Observer-to-source angular-diameter distance.
- Lens-to-source angular-diameter distance.

Outputs:
- Einstein angle.
- Einstein radius in the image plane, when the required distance is available.
- Angular scale in arcseconds.

For cosmological lensing, use consistent angular-diameter distances.

## C. Lens Equation Calculator

For a point-mass lens:

\[
\vec{\beta}=
\vec{\theta}-
\theta_E^2
\frac{\vec{\theta}-\vec{\theta}_L}
{|\vec{\theta}-\vec{\theta}_L|^2}
\]

Calculate:
- Source position.
- Image position.
- Deflection vector.
- Lens position.
- Multiple image solutions.

## D. Image Magnification Calculator

Calculate:

\[
\mu=\frac{1}{\det A}
\]

where:

\[
A=\frac{\partial\vec{\beta}}{\partial\vec{\theta}}
\]

Display:
- Signed magnification.
- Absolute magnification.
- Image parity.
- Magnification maps.
- Areas of high magnification.

The application must handle critical curves, where the idealized magnification can become mathematically very large.

## E. Critical Curves and Caustics

Display:
- Critical curves in the image plane.
- Caustics in the source plane.
- Source movement across caustics.
- Changes in image number.
- Magnification near caustics.

## F. Time-Delay Analysis

Add an advanced module for gravitational time delays.

Display:
- Arrival-time differences between multiple images.
- Fermat-potential contributions.
- Time-delay distance.
- Effects of changing lens and source geometry.

Clearly identify which assumptions and cosmological parameters are used.

## G. Numerical Analysis

Include:
- Numerical integration.
- Finite-difference derivatives.
- Grid-resolution comparison.
- Interpolation.
- Error estimation.
- Convergence tests.
- Numerical stability checks.
- Computational execution time.

## H. Parameter Sensitivity

Allow users to investigate how changes in:
- Lens mass.
- Source position.
- Lens-source distance.
- Impact parameter.
- Mass distribution.
- Redshift and cosmological assumptions.

affect:
- Deflection.
- Einstein radius.
- Image positions.
- Magnification.
- Image shapes.

---

# 8. Scientific Graphs and Visualization

All graphs must update when the user changes simulation parameters.

## A. Deflection vs. Impact Parameter

- X-axis: Impact parameter.
- Y-axis: Deflection angle.
- Show the theoretical relationship.
- Compare different lens masses.

## B. Einstein Radius vs. Lens Mass

- X-axis: Lens mass.
- Y-axis: Einstein angle.
- Demonstrate the square-root relationship under fixed geometry.

## C. Magnification Map

- Two-dimensional color map.
- Show regions of high and low magnification.
- Display source position.
- Display critical curves where appropriate.

## D. Image Position Graph

- Show predicted image positions.
- Compare image positions as the source moves.
- Display the Einstein radius as a reference.

## E. Mass Distribution Graph

- Display mass density.
- Compare point-mass and extended-mass models.
- Display the projected surface mass density.

## F. Time-Delay Graph

- Compare arrival-time differences between images.
- Show how changing the model affects predicted delays.

## G. Numerical Convergence Graph

- X-axis: Grid resolution or integration step.
- Y-axis: Selected numerical result or error.
- Demonstrate whether the simulation approaches a stable solution.

## H. Simulation Comparison

Allow side-by-side comparisons of:
- Point-mass lens.
- Galaxy lens.
- Binary lens.
- Galaxy-cluster lens.
- Black-hole ray tracing.

---

# 9. Learning and Research Page

This page turns GRAVISIM into an educational computational physics laboratory.

## A. Learning Modules

### Module 1: Introduction to General Relativity
- Gravity and spacetime.
- Equivalence principle.
- Curved spacetime.
- Light propagation in gravitational fields.

### Module 2: Gravitational Lensing
- Gravitational deflection of light.
- Lens, source, and observer geometry.
- Weak and strong lensing.
- Einstein rings.
- Multiple images.
- Microlensing.

### Module 3: Mathematical Foundations
- Vectors.
- Coordinate geometry.
- Calculus.
- Partial derivatives.
- Numerical integration.
- Differential equations.
- Matrix operations.

### Module 4: Computational Physics
- Python programming.
- Numerical methods.
- Scientific computing.
- Data visualization.
- Error analysis.
- Model validation.

### Module 5: Advanced Lensing
- Extended mass profiles.
- Critical curves.
- Caustics.
- Magnification.
- Time delays.
- Schwarzschild geometry.
- Null geodesics.

## B. Interactive Lessons

Each lesson should include:
- Simple explanation.
- Mathematical equation.
- Definition of variables.
- Units.
- Worked example.
- Interactive simulation.
- Graph or visualization.
- Short knowledge check.

## C. Experiment Mode

Users should be able to perform guided experiments.

Example experiments:

1. How does lens mass affect the Einstein radius?
2. How does the impact parameter affect deflection?
3. What happens when the source aligns with the lens?
4. How does an extended galaxy mass distribution affect the image?
5. How do two lensing objects change the caustic structure?
6. How does a black hole affect light trajectories in the strong-field regime?

## D. Research Notes

Allow users to record:
- Experiment title.
- Hypothesis.
- Initial parameters.
- Simulation settings.
- Observed results.
- Calculations.
- Interpretation.
- Conclusion.

## E. Knowledge Assessment

Include:
- Multiple-choice questions.
- Concept questions.
- Numerical exercises.
- Simulation-based challenges.
- Short explanations.

---

# 10. Simulation Management

## A. Save Simulation

Users can save:
- Lens model.
- Mass.
- Distances.
- Source position.
- Lens position.
- Grid resolution.
- Numerical settings.
- Visualization settings.
- Computed outputs.

## B. Load Simulation

Allow previously saved simulations to be reopened.

## C. Compare Simulations

Compare two or more simulations using:
- Same mass, different geometry.
- Same geometry, different mass.
- Point mass versus extended mass.
- Different source positions.
- Different numerical resolutions.

## D. Export Results

Support:
- PNG images.
- PDF reports.
- CSV numerical results.
- JSON simulation configurations.
- Scientific graphs.
- Experiment summaries.

Every export should include units, parameter values, model assumptions, and data provenance where relevant.

---

# 11. Core Data Models

All stored values must use consistent units and documented definitions.

## A. Simulation

```json
{
  "id": "string",
  "name": "string",
  "modelType": "point_mass | sis | galaxy | binary | cluster | schwarzschild",
  "description": "string",
  "createdAt": "timestamp",
  "updatedAt": "timestamp",
  "lensObjectIds": ["string"],
  "sourceObjectId": "string | null",
  "observer": {},
  "geometry": {},
  "cosmology": {},
  "numericalSettings": {},
  "visualizationSettings": {},
  "resultsId": "string | null"
}
```

## B. Lens Object

```json
{
  "id": "string",
  "name": "string",
  "objectType": "star | planet | black_hole | galaxy | cluster | custom",
  "massKg": "number | null",
  "massUncertaintyKg": "number | null",
  "position": {
    "x": "number",
    "y": "number",
    "z": "number"
  },
  "redshift": "number | null",
  "massProfile": "point | sis | sersic | nfw | custom",
  "parameters": {},
  "sourceReference": "string | null"
}
```

## C. Background Source

```json
{
  "id": "string",
  "name": "string",
  "sourceType": "star | galaxy | quasar | supernova | custom",
  "position": {
    "betaX": "number",
    "betaY": "number"
  },
  "angularSizeArcsec": "number | null",
  "brightness": "number | null",
  "redshift": "number | null",
  "imageReference": "string | null"
}
```

## D. Observer and Geometry

```json
{
  "id": "string",
  "observerLensDistanceMpc": "number",
  "observerSourceDistanceMpc": "number",
  "lensSourceDistanceMpc": "number",
  "distanceDefinition": "angular_diameter | physical | other",
  "coordinateSystem": "angular | physical | custom"
}
```

The distances must be physically consistent. For cosmological systems, calculate or validate the lens-source distance using the adopted cosmology rather than treating all distances as independent arbitrary inputs.

## E. Cosmology

```json
{
  "id": "string",
  "model": "FlatLambdaCDM | custom",
  "H0": "number",
  "H0Unit": "km/s/Mpc",
  "Om0": "number",
  "Ode0": "number | null",
  "Tcmb0": "number | null"
}
```

## F. Simulation Results

```json
{
  "id": "string",
  "simulationId": "string",
  "deflectionAngleRad": "number | null",
  "einsteinAngleRad": "number | null",
  "imagePositions": [],
  "magnifications": [],
  "criticalCurves": [],
  "caustics": [],
  "timeDelays": [],
  "computationTimeSeconds": "number",
  "gridResolution": "number",
  "numericalErrorEstimate": "number | null",
  "createdAt": "timestamp"
}
```

## G. Astronomical Dataset

```json
{
  "id": "string",
  "objectName": "string",
  "objectType": "string",
  "rightAscensionDeg": "number | null",
  "declinationDeg": "number | null",
  "redshift": "number | null",
  "massKg": "number | null",
  "massUncertaintyKg": "number | null",
  "distance": "number | null",
  "distanceUnit": "string | null",
  "imageFile": "string | null",
  "fileFormat": "FITS | CSV | JSON | other",
  "survey": "string",
  "observationDate": "string | null",
  "sourceUrl": "string",
  "accessDate": "timestamp",
  "licenseOrUsageTerms": "string | null",
  "citation": "string | null"
}
```

## H. Experiment Record

```json
{
  "id": "string",
  "title": "string",
  "hypothesis": "string",
  "simulationId": "string",
  "parameters": {},
  "observations": "string",
  "resultsId": "string",
  "interpretation": "string",
  "conclusion": "string",
  "createdAt": "timestamp"
}
```

## I. User Settings

```json
{
  "theme": "dark | light",
  "preferredUnits": "SI | astronomical",
  "defaultSimulationMode": "basic | intermediate | advanced",
  "defaultLensModel": "point_mass",
  "showGrid": true,
  "showLabels": true,
  "language": "English"
}
```

---

# 12. Core Physics and Computational Requirements

The following equations form the foundation of the simulation.

## A. Weak-Field Light Deflection

\[
\hat{\alpha}=\frac{4GM}{c^2b}
\]

Where:
- \(G\): gravitational constant.
- \(M\): lens mass.
- \(c\): speed of light.
- \(b\): impact parameter.

## B. Einstein Radius

\[
\theta_E=
\sqrt{
\frac{4GM}{c^2}
\frac{D_{LS}}{D_LD_S}
}
\]

Where:
- \(D_L\): observer-to-lens angular-diameter distance.
- \(D_S\): observer-to-source angular-diameter distance.
- \(D_{LS}\): lens-to-source angular-diameter distance.

## C. Point-Mass Lens Equation

\[
\vec{\beta}=
\vec{\theta}-
\theta_E^2
\frac{\vec{\theta}}{|\vec{\theta}|^2}
\]

This simplified equation assumes that the lens is at the coordinate origin.

## D. Point-Mass Image Positions

For a source aligned along one coordinate axis:

\[
\theta_\pm=
\frac{\beta\pm\sqrt{\beta^2+4\theta_E^2}}{2}
\]

## E. Magnification

\[
\mu=\frac{1}{\det A}
\]

Where \(A\) is the Jacobian matrix of the lens mapping.

## F. Schwarzschild Radius

\[
r_s=\frac{2GM}{c^2}
\]

## G. Photon-Sphere Radius

\[
r_{ph}=\frac{3GM}{c^2}
\]

## H. Advanced Black-Hole Model

Use the Schwarzschild metric and integrate null geodesics for the non-rotating black-hole extension.

The numerical solver should track the photon trajectory and its conserved quantities, use appropriate initial conditions, and check integration accuracy.

---

# 13. Technology Stack

## Main Programming Language
- Python 3.

## Scientific Computing
- NumPy.
- SciPy.
- Astropy.

## 2D Visualization
- Matplotlib.
- Plotly.

## 3D Visualization
- Plotly 3D.
- Optional PyVista for more advanced 3D rendering.

## User Interface
- Streamlit.

## Data Handling
- Pandas.
- Astropy FITS tools.
- JSON.
- CSV.

## Testing
- pytest.

## Development Environment
- Visual Studio Code.
- Jupyter Notebook.
- Git and GitHub for version control.

## Suggested Installation

```bash
pip install numpy scipy matplotlib pandas astropy
pip install plotly streamlit
pip install pytest
```

Optional advanced packages:

```bash
pip install lenstronomy
pip install pyvista
```

The core point-mass solver should be implemented independently. Use established software such as lenstronomy as an external comparison and validation tool, not as a replacement for the thesis's own central numerical method.

---

# 14. Suggested Project Folder Structure

```text
GRAVISIM/
│
├── main.py
├── requirements.txt
├── README.md
│
├── physics/
│   ├── constants.py
│   ├── deflection.py
│   ├── einstein_radius.py
│   ├── lens_equation.py
│   ├── magnification.py
│   ├── mass_profiles.py
│   ├── cosmology.py
│   └── time_delay.py
│
├── simulation/
│   ├── point_mass.py
│   ├── galaxy_lens.py
│   ├── binary_lens.py
│   ├── cluster_lens.py
│   ├── ray_tracing.py
│   └── source_models.py
│
├── relativity/
│   ├── schwarzschild.py
│   ├── geodesics.py
│   ├── photon_orbits.py
│   └── black_hole_raytracing.py
│
├── visualization/
│   ├── plots_2d.py
│   ├── lensing_maps.py
│   ├── visualization_3d.py
│   ├── light_paths.py
│   └── spacetime_grid.py
│
├── data/
│   ├── objects/
│   ├── observations/
│   ├── imported/
│   └── metadata/
│
├── analysis/
│   ├── numerical_methods.py
│   ├── convergence.py
│   ├── error_analysis.py
│   └── comparison.py
│
├── interface/
│   ├── dashboard.py
│   ├── simulation_2d.py
│   ├── visualization_3d.py
│   ├── astronomical_data.py
│   ├── analysis_lab.py
│   └── learning.py
│
├── storage/
│   ├── database.py
│   ├── simulations.py
│   └── exports.py
│
└── tests/
    ├── test_deflection.py
    ├── test_einstein_radius.py
    ├── test_lens_equation.py
    ├── test_magnification.py
    └── test_geodesics.py
```

---

# 15. Core Functionalities

## A. Physics Engine
- Calculate gravitational deflection.
- Calculate Einstein radius.
- Solve lens equations.
- Calculate image positions.
- Calculate magnification.
- Support different mass profiles.
- Calculate critical curves and caustics.
- Calculate time delays in supported models.
- Integrate black-hole null geodesics in the advanced mode.

## B. Interactive Simulation
- Update simulation when parameters change.
- Support multiple lens models.
- Display light paths.
- Display image formation.
- Animate selected processes.
- Support 2D and 3D modes.

## C. Astronomical Data
- Import public datasets.
- Read FITS files.
- Store astronomical object information.
- Preserve measurement units and uncertainties.
- Preserve data source and citation.
- Compare idealized models with selected observations.

## D. Scientific Analysis
- Generate graphs.
- Calculate numerical results.
- Compare theoretical and numerical solutions.
- Perform grid-convergence tests.
- Estimate numerical error.
- Export results.

## E. Educational Features
- Explain equations.
- Define variables.
- Show units.
- Provide worked examples.
- Provide guided experiments.
- Include quizzes and learning activities.

## F. Data Storage
- Save simulations locally.
- Save experiment records.
- Store imported dataset metadata.
- Load previous simulations.
- Export data for research documentation.

---

# 16. Minimum Viable Product (MVP)

The MVP should be realistic for an undergraduate thesis and must demonstrate a complete, working scientific application.

## Required MVP Features

1. Interactive dashboard.
2. Point-mass gravitational-lensing model.
3. Einstein-radius calculator.
4. Light-deflection calculator.
5. Point-mass lens equation solver.
6. Multiple-image visualization.
7. Einstein-ring visualization.
8. Source-position adjustment.
9. Lens-mass adjustment.
10. 2D ray-mapping visualization.
11. Basic 3D lensing visualization.
12. Magnification calculation.
13. Deflection and magnification graphs.
14. Save and load simulation settings.
15. Export simulation results.
16. Physics explanation and learning modules.
17. Numerical validation against analytical point-mass solutions.

## Advanced Features

Implement after the MVP is stable:

- Extended galaxy mass distributions.
- Elliptical lenses.
- Binary lenses.
- Critical curves and caustics.
- Galaxy-cluster models.
- Real astronomical image comparison.
- Time-delay calculations.
- Advanced Schwarzschild null-geodesic ray tracing.
- More detailed 3D visualizations.

---

# 17. Features to Exclude from the First Version

To prevent the project from becoming too large, do not require these for the initial MVP:

- Full cosmological N-body simulations.
- Full numerical solutions of Einstein's field equations.
- Rotating Kerr black-hole ray tracing.
- Real-time telescope control.
- Automatic discovery of new gravitational lenses.
- Automatic prediction of when or where black holes will form.
- Massive distributed computing.
- Paid astronomical APIs.
- Cloud accounts and multi-user collaboration.
- Real-time access to every astronomical catalog.
- Machine-learning lens discovery.

These can be proposed as future research directions.

---

# 18. Data Storage and Performance Requirements

## Data Storage
- Store simulation configurations locally using JSON or SQLite.
- Store numerical outputs in CSV, JSON, or NumPy formats.
- Store observation metadata separately from original image files.
- Preserve original imported data.
- Allow users to export their work.
- Structure the data so that future cloud migration is possible.

## Performance
- The basic point-mass simulation should run smoothly on an ordinary student laptop.
- Use NumPy vectorization for grid calculations.
- Allow users to select grid resolution.
- Avoid unnecessary recalculation.
- Cache reusable computations when appropriate.
- Display computation status for advanced simulations.
- Allow high-resolution calculations to run separately from interactive preview calculations.

## Numerical Reliability
- Validate physical units.
- Check input ranges.
- Avoid division by zero at singular points.
- Handle critical curves carefully.
- Track integration errors in geodesic calculations.
- Record the numerical method and settings used for every saved result.

---

# 19. Scientific Validation and Testing

The application must not be evaluated only on appearance. It must be tested scientifically.

## Test 1: Mass Dependence

At fixed geometry:

\[
\theta_E\propto\sqrt{M}
\]

If the mass increases by a factor of four, the Einstein angle should increase by a factor of two.

## Test 2: Impact Parameter Dependence

For the weak-field point-mass model:

\[
\hat{\alpha}\propto\frac{1}{b}
\]

Increasing the impact parameter should decrease the deflection angle.

## Test 3: Source Alignment

Move the source toward perfect alignment with a point-mass lens.

The images should approach the Einstein ring in the idealized point-source model.

## Test 4: Image Position

Compare numerical image positions against the analytical point-mass solutions.

## Test 5: Magnification

Compare numerical magnification with analytical point-mass magnification for suitable non-singular configurations.

## Test 6: Grid Resolution

Repeat simulations using different grid resolutions.

Measure how the results change as resolution increases.

## Test 7: Black-Hole Geodesics

Compare selected numerical null-geodesic results with known Schwarzschild predictions and verify that results are stable under changes in integration tolerance and step size.

## Test 8: External Model Comparison

Compare selected outputs with an established lens-modeling package such as lenstronomy.

Document differences in conventions, parameters, assumptions, and numerical methods.

---

# 20. Thesis Research Structure

## Chapter 1: Introduction
- Background of the study.
- Research problem.
- Objectives.
- Significance.
- Scope and limitations.

## Chapter 2: Review of Related Literature
- General relativity.
- Gravitational lensing.
- Point-mass lensing.
- Extended mass distributions.
- Numerical methods.
- Computational visualization.
- Existing gravitational-lensing software.

## Chapter 3: Methodology
- Research design.
- Software architecture.
- Mathematical model.
- Numerical algorithms.
- Data sources.
- Visualization methods.
- Validation procedures.
- Evaluation criteria.

## Chapter 4: Results and Discussion
- Simulation outputs.
- Einstein-ring formation.
- Multiple-image formation.
- Parameter sensitivity.
- Numerical accuracy.
- Comparison with analytical solutions.
- Comparison with selected astronomical observations.
- Application performance.

## Chapter 5: Conclusion and Recommendations
- Summary of results.
- Conclusions.
- Limitations.
- Recommendations.
- Future development.

---

# 21. Competition Demonstration Plan

The application should have a short demonstration that communicates both the science and the innovation.

## Demonstration 1: Point-Mass Lens
Change the mass and show how the Einstein radius changes.

## Demonstration 2: Einstein Ring
Move the source into alignment and show the ring formation.

## Demonstration 3: Multiple Images
Move the source away from alignment and demonstrate the formation of multiple images.

## Demonstration 4: Galaxy Lens
Change the mass profile and demonstrate how an extended galaxy can produce arcs and distorted images.

## Demonstration 5: 3D Visualization
Show the 3D geometry and light paths, clearly identifying the visualization's physical assumptions.

## Demonstration 6: Black-Hole Extension
Show how strong-field light trajectories differ from the weak-field approximation.

## Demonstration 7: Scientific Validation
Show a graph comparing the program's numerical results with analytical predictions.

The strongest competition feature is not simply a beautiful simulation. It is the combination of interactive physics, numerical computation, scientific validation, and an understandable educational interface.

---

# 22. Final System Objective

GRAVISIM should function as a complete computational physics laboratory for gravitational lensing.

It should allow students and researchers to:

1. Understand the physics of gravitational lensing.
2. Change the physical parameters of a lensing system.
3. Calculate deflection angles and Einstein radii.
4. Visualize light paths in two and three dimensions.
5. Investigate multiple-image formation.
6. Study magnification, critical curves, and caustics.
7. Compare different mass distributions.
8. Explore strong-field black-hole lensing as an advanced extension.
9. Import and analyze selected astronomical data.
10. Compare numerical simulations with theoretical predictions.
11. Record and export scientific experiments.
12. Learn the physics and computational methods behind the results.

**The central contribution of this thesis is the development of an independently implemented, scientifically validated, interactive gravitational-lensing simulation that combines computational physics, astronomical visualization, and physics education.**