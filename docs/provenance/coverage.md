# Source coverage

Per-source inventory of where relationships can be found, what has been examined and what
remains. Generated from local working manifests; counts only, no source content.

- **Discovered**: candidate records found in the source (all kinds).
- **Verified / Ambiguous / Unverified / Duplicate / Deferred**: technical gate of those records
  (Unverified includes candidates not yet checked; Deferred = does not fit the scalar schema).
- **Implemented**: catalog formulas discovered in or supported by the source.
- **Estimate**: a path-based prior from the inventory (module or chapter names and sizes),
  not a count of checked formulas. Expect only part of it to pass verification and licensing.
- **Examined units**: units with at least one recorded candidate (a lower bound).

## Mathematics and statistics

| Source | Revision | Units (in scope / examined) | Discovered | Verified | Ambiguous | Unverified | Duplicate | Deferred | Implemented | Estimate (all units) | Estimate remaining |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `MATHLIB` | `4a3cff2c` | 45 / 20 | 47 | 40 | 0 | 0 | 2 | 5 | 78 | 536-1670 | 204-619 |
| `SYMPY` | `16fa8553` | 54 / 16 | 47 | 34 | 0 | 5 | 1 | 6 | 11 | 982-2223 | 655-1490 |
| `SELINGER_LA` | `d74bc3a9` | 23 / 7 | 31 | 23 | 0 | 0 | 0 | 8 | 26 | 100-222 | 63-148 |
| `SCIPY` | `e4e854ea` | 53 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2055-4715 | 2020-4615 |
| `STATSMODELS` | `278ff995` | 37 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1135-2610 | 1110-2535 |
| `NUMPY` | `dd88c0c1` | 29 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 690-1580 | 675-1535 |
| `MOORE_ODE_PDE` | `f19856e2` | 14 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 86-199 | 85-195 |
| `ENVX_STATS` | `9f5ed9ce` | 26 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 100-216 | 100-216 |
| `YAU_BIOSTATS` | `4b97fd54` | 9 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 43-91 | 42-88 |
| `DEVITO_PDE_BOOK` | `34acdb47` | 19 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 92-223 | 90-218 |
| `OPENMDAO` | `e57af304` | 19 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 415-935 | 410-920 |
| **Total** | | 328 / 43 | 125 | 97 | 0 | 5 | 3 | 19 | 83 | 6234-14684 | 5454-12579 |

## Engineering and physics

| Source | Revision | Units (in scope / examined) | Discovered | Verified | Ambiguous | Unverified | Duplicate | Deferred | Implemented | Estimate (all units) | Estimate remaining |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `FLUIDS_CHEDL` | `652a0134` | 30 / 7 | 66 | 17 | 2 | 34 | 11 | 2 | 0 | 410-1015 | 255-650 |
| `HT_CHEDL` | `85e0ee68` | 20 / 6 | 27 | 16 | 2 | 6 | 2 | 1 | 0 | 236-565 | 146-360 |
| `THERMO_CHEDL` | `2bb466e9` | 26 / 3 | 5 | 1 | 1 | 1 | 1 | 1 | 0 | 398-955 | 313-745 |
| `MODELICA_MSL` | `4c40388d` | 39 / 6 | 29 | 7 | 0 | 15 | 6 | 1 | 0 | 845-1975 | 710-1660 |
| `PYNITE` | `ae8c4049` | 15 / 5 | 19 | 9 | 0 | 2 | 4 | 4 | 0 | 163-400 | 98-245 |
| `COOLPROP` | `ae81610e` | 18 / 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 395-950 | 385-900 |
| `AEROSANDBOX` | `edad83dd` | 21 / 7 | 45 | 14 | 0 | 18 | 4 | 9 | 0 | 338-800 | 225-520 |
| `ROCKETPY` | `9bd6ad3a` | 14 / 5 | 31 | 16 | 2 | 6 | 1 | 6 | 0 | 237-548 | 140-320 |
| `OREKIT` | `6fdf97c1` | 28 / 4 | 22 | 14 | 1 | 0 | 3 | 4 | 0 | 665-1505 | 545-1230 |
| `OPENFAST` | `2895884d` | 18 / 3 | 24 | 1 | 2 | 14 | 0 | 7 | 0 | 360-875 | 295-710 |
| `POLIASTRO` | `21fd7719` | 15 / 5 | 14 | 11 | 0 | 2 | 0 | 1 | 0 | 237-528 | 150-330 |
| `PANDAPOWER` | `d5c3f376` | 14 / 2 | 29 | 7 | 0 | 19 | 0 | 3 | 0 | 270-620 | 215-485 |
| `PYBAMM` | `29bd758f` | 17 / 4 | 24 | 2 | 3 | 15 | 1 | 3 | 0 | 375-855 | 280-635 |
| `CANTERA` | `e906c2f9` | 15 / 3 | 41 | 10 | 0 | 22 | 3 | 6 | 0 | 605-1420 | 380-895 |
| `ENERGYPLUS` | `01c3cbad` | 24 / 2 | 46 | 0 | 5 | 29 | 7 | 5 | 0 | 875-2065 | 835-1975 |
| **Total** | | 314 / 62 | 422 | 125 | 18 | 183 | 43 | 53 | 0 | 6409-15076 | 4972-11660 |

## Largest remaining units per source

- `MATHLIB`: Univariate and multivariate polynomials, roots, and Sturm sequences (15-45); International Mathematical Olympiad competition problems (10-35); Ordered groups, rings, fields, and Chebyshev inequalities (12-35); Trigonometric, inverse trigonometric, and Chebyshev functions (15-35); Riemann zeta, Hurwitz zeta, Dirichlet L-series, and Euler products (12-35)
- `SYMPY`: Number Theory, Factorization, and Prime Relations (30-65); Polynomial Arithmetic, Factorization, and Roots (30-65); Fundamental Arithmetic, Numbers, and Core Expressions (25-60); Quantum Mechanics and Quantum Computing (25-60); Physical Units, Dimensions, and Constants (25-60)
- `SELINGER_LA`: Linear Transformations in R^n & Computer Graphics (5-12); Eigenvalue Applications (Powers, Recurrences, ODE Systems & Matrix Exp) (5-12); Inner Product Spaces, Gram-Schmidt & Fourier Series (5-12); Orthogonal Maps, Symmetric Diagonalization & Quadratic Forms (5-12); Systems of Linear Equations (Elimination & Row Reduction) (4-10)
- `SCIPY`: Continuous Univariate Probability Distributions (180-400); Physical and Mathematical Constants (CODATA) (100-250); Bessel, Hankel, Airy, and Struve Functions (60-140); Discrete Univariate Probability Distributions (60-140); Parametric and Nonparametric Statistical Hypothesis Tests (60-130)
- `STATSMODELS`: Generalized Linear Models (GLM) and Exponential Dispersion Families (45-100); State Space Representation, Kalman Filtering, and RTS Smoothing (45-100); Vector Autoregression (VAR), Vector Error Correction (VECM), and Cointegration (45-100); Multivariate Analysis: PCA, Factor Analysis, MANOVA, and GPA Rotation (40-90); ARIMA and Seasonal SARIMAX Models (40-90)
- `NUMPY`: Random Variate Generators and Continuous/Discrete Distributions (50-110); Linear Algebra: Solvers, Inverses, Eigenvalues, and Decompositions (45-100); Universal Functions (ufuncs) Engine and Mathematical Scalar Kernels (40-90); Basic Mathematical Reductions, Differences, and Convolutions (35-80); Hermite (Physicist's) and HermiteE (Probabilist's) Polynomials (30-70)
- `MOORE_ODE_PDE`: Chapter 08: Analytical PDE Solutions & Separation of Variables (8-18); Chapter 03: Higher-Order Linear ODEs & Systems (8-16); Chapter 11: Finite Difference Methods for Hyperbolic PDEs (Wave & Advection) (7-16); Chapter 02: First-Order ODEs (Separable, Linear & Exact) (7-15); Chapter 10: Finite Difference Methods for Parabolic PDEs (Diffusion) (6-15)
- `ENVX_STATS`: Course Tutorials (Worksheets & Solutions) (6-15); Lecture 07: Simple Linear Regression & Correlation (6-14); Lecture 03: Hypothesis Testing, T-Tests & Confidence Intervals (6-12); Lecture 04: One-Way ANOVA & F-Tests (5-12); Lecture 08: Multiple Linear Regression & Model Selection (5-12)
- `YAU_BIOSTATS`: Chapter 7: Scaling Up (ANOVA, Post-Hoc & Chi-Square Tests) (6-14); Chapter 8: Looking to the Future (Regression & Survival Analysis) (6-14); Chapter 6: Comparing Two Groups (t-Tests & Non-Parametric) (6-12); Chapter 2: Seeking the Middle (Central Tendency & Dispersion) (5-10); Chapter 9: Review & Clinical Epidemiology Metrics (5-10)
- `DEVITO_PDE_BOOK`: Chapter 03: Wave Equations & Absorbing Boundary Conditions (8-20); Chapter 02: Diffusion & Heat Equations (Theory, Stencils & Analysis) (8-18); Appendix: Finite Difference & Mathematical Formulas (6-16); Chapter 04: Advection Equations, Upwinding & Dispersion Relations (6-15); Chapter 08: Electromagnetics & Maxwell's Equations (6-15)
- `OPENMDAO`: Multidisciplinary Engineering Benchmark Models (40-90); Multidisciplinary Design Optimization (MDO) Total Derivatives and Adjoint Equations (30-70); Multidimensional Table Interpolation Algorithms (25-60); Vector, Tensor, and Matrix Algebraic Operation Components (25-55); Nonlinear Solvers and Multidisciplinary Coupling Iterations (25-55)
- `FLUIDS_CHEDL`: Two-phase pressure drop correlations (25-60); Crane Technical Paper 410 solved textbook problems (20-50); Pressure relief valve sizing (API 520 / API 526) (15-40); Two-phase flow void fraction correlations (15-40); Control valve sizing and flow coefficients (IEC 60534) (15-35)
- `HT_CHEDL`: Thermal radiation, view factors, and radiative transfer (20-45); Crossflow heat transfer and pressure drop across tube banks (15-35); Flow boiling inside tubes and channels (15-35); Pool boiling, nucleate boiling, and critical heat flux (15-35); Film and dropwise condensation heat transfer (15-35)
- `THERMO_CHEDL`: Cubic and non-cubic equations of state (25-60); Activity coefficient models (NRTL, UNIQUAC, Wilson, Margules) (25-55); Group contribution property estimation (Joback, Bondi, Fedors, PPR78) (20-50); Alpha temperature-dependent functions for cubic EOS (20-45); Heat capacity correlations for gases, liquids, and solids (20-45)
- `MODELICA_MSL`: Fluid friction pressure drop and convective heat transfer correlations (40-100); Power electronic converter topologies (rectifiers, inverters, choppers) (35-80); Electromechanical machines (induction, synchronous, DC, transformers) (30-70); Mathematical library (Matrices, Vectors, LAPACK, FFT, Special functions) (30-70); 3D rigid body dynamics, orientation quaternions, and inertia tensors (30-70)
- `PYNITE`: Quadrilateral plate bending and membrane element stiffness (DKMQ and MITC4) (15-35); Frame, beam, truss, modal, and pushover structural examples (15-35); Structural solver algorithms (linear static, P-Delta, modal eigenvalues) (10-25); Reinforced concrete shear wall macro-element modeling (10-25); Symbolic derivations of quadrilateral and rectangular plate element stiffness (10-25)
- `COOLPROP`: Pure fluid Helmholtz equation of state JSON definitions (30-80); Multi-parameter Helmholtz energy fundamental equation of state engine (30-70); IAPWS-IF97 industrial formulation for water and steam (30-65); Mixture Helmholtz EOS, departure functions, and phase envelope algorithms (25-60); AbstractState polymorphic coordinator and thermodynamic property derivations (25-60)
- `AEROSANDBOX`: Aircraft Structural Weight Regressions (25-60); 3D Aerodynamics & Vortex Lattice Methods (20-50); Calculus, Numerical Integration & Rotation Operators (25-50); 2D Aerodynamics & Airfoil Solvers (15-40); Differentiable Array Operations & Smooth Functions (20-40)
- `ROCKETPY`: 6-DOF Rocket Trajectory Simulation (25-60); Liquid & Hybrid Rocket Engines & Tank Dynamics (25-55); Mathematical Utilities, Interpolation & Vector Algebra (25-55); Stochastic Rocket & Environment Models (15-35); Flight Sensors (IMU, Barometer, GNSS) (15-30)
- `OREKIT`: Draper Semi-analytical Satellite Theory (DSST) (40-90); Tracking Observables & Measurement Models (35-80); Gravitational Field & Tidal Perturbations (35-80); Spacetime Reference Frames & Celestial Mechanics Transforms (35-80); Celestial Bodies & Planetary Shapes (30-70)
- `OPENFAST`: Offshore Hydrodynamics & Wave Loading (30-75); NWTC Mathematical & Mesh Mapping Library (35-75); Geometrically Exact Beam Theory (GEBT) Blade Dynamics (25-60); Multibody Structural Dynamics (ElastoDyn) (25-60); Substructure Dynamics & Craig-Bampton Reduction (20-50)
- `POLIASTRO`: Two-Body Analytical & Numerical Orbit Propagators (30-65); Special Perturbations (J2, J3, Drag, Radiation, 3-Body) (15-35); Initial Orbit Determination (Lambert, Gibbs) (15-35); Atmospheric Density Models (COESA, Jacchia) (15-35); Periodic Orbits & Halo Orbit Families in CR3BP (15-35)
- `PANDAPOWER`: AC & DC Power Flow Solvers (30-70); IEC 60909 Short-Circuit Calculations (25-55); Power System State Estimation (20-45); Network Element Parameter Builders (20-45); Optimal Power Flow (OPF) (15-35)
- `PYBAMM`: Lithium-Ion Battery Models (DFN, SPMe, SPM, MPM, MSMR) (35-80); Symbolic Expression Tree for Battery Equations (25-60); Thermal Energy Balances & Heat Generation (25-60); Battery Aging & Degradation Mechanisms (25-60); Solid-Phase Particle Diffusion & Intercalation (25-55)
- `CANTERA`: Molecular Transport Properties & Collision Dynamics (45-110); 1D Reacting Flows & Laminar Flame Solvers (45-105); 0D Reactor Networks & Flow Devices (40-95); Python Cython C-API Bindings & Mechanism Utilities (40-90); Pure Substance Multiparameter Equations of State (35-80)
- `ENERGYPLUS`: Building Envelope & Zone Heat Balance Engine (65-150); Window Optics, Heat Transfer & TARCOG Engine (60-140); Plant Loops, Hydronic Network & Thermal Dispatch (55-130); Renewable Power, Solar Thermal & On-Site Cogeneration (55-130); Cooling/Heating Coils & Air-to-Air Heat Exchangers (50-120)
