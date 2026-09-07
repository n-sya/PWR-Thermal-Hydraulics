# PWR Thermal-Hydraulics

A Python thermal-hydraulics model for the steady-state, single-phase analysis of a simplified Pressurised Water Reactor (PWR) coolant subchannel.

The model calculates coolant flow characteristics, convective heat transfer, channel pressure drop, and axial coolant and clad surface temperature distributions. A Tkinter GUI provides user-editable model inputs, numerical results, and interactive access to the generated plots.

# Model Overview

The model represents one coolant subchannel surrounding a fuel rod in a square fuel-rod lattice.

The analysis combines:

- Subchannel geometry calculations
- Reynolds and Prandtl number calculations
- Dittus-Boelter turbulent heat-transfer correlation
- Fanning friction-factor correlation
- Channel wall-friction pressure drop
- Cosine axial pin linear power distribution
- Steady-flow coolant energy balance
- Convective clad surface temperature calculation

The complete thermal-hydraulic analysis requires turbulent flow with:

$$Re \geq 10000$$

This restriction is applied because the heat-transfer calculation uses the Dittus-Boelter correlation.

# Model Inputs

All operating and geometric parameters are user-editable through the GUI.

Inputs include:

- Fuel rod length
- Peak pin linear power
- Subchannel mass flow rate
- Fuel rod outside diameter
- Square lattice pitch
- Coolant inlet temperature
- Coolant density
- Dynamic viscosity
- Thermal conductivity
- Specific heat capacity

Default values are provided to allow the model to be run immediately.

# Thermal-Hydraulic Calculations

The subchannel hydraulic diameter is calculated from:

$$D_h = \frac{4A_f}{P_w}$$

where the square-lattice flow area is:

$$A_f = p^2 - \frac{\pi d^2}{4}$$

The Reynolds number is:

$$Re = \frac{\rho uD_h}{\mu}$$

and the Prandtl number is:

$$Pr = \frac{\mu c_p}{k}$$

For turbulent forced convection, the Dittus-Boelter correlation is used:

$$Nu = 0.023Re^{0.8}Pr^{0.4}$$

The heat-transfer coefficient is then:

$$h = \frac{Nu\,k}{D_h}$$

The turbulent Fanning friction factor is calculated using:

$$f_F = 0.046Re^{-0.2}$$

and the channel pressure drop due to wall friction is:

$$\Delta P_{\text{channel}} = \frac{2f_FL}{D_h}\rho u^2$$

The axial pin linear power is represented by a cosine distribution:

$$q'(z) = q'_{\text{peak}}\cos\left(\frac{\pi z}{L}\right)$$

The resulting coolant temperature distribution is:

$$T(z) = T_{\text{in}} + \frac{q'_{\text{peak}}L}{\pi\dot{m}c_p}\left[\sin\left(\frac{\pi z}{L}\right)+1\right]$$

The clad surface temperature is calculated from:

$$T_c(z) = T(z) + \frac{q'(z)}{\pi dh}$$

A complete derivation of the implemented equations is provided in `DERIVATIONS.md`.

# Outputs

The GUI reports:

- Reynolds number
- Prandtl number
- Nusselt number
- Heat-transfer coefficient
- Peak heat flux
- Peak boundary layer temperature difference
- Fanning friction factor
- Channel pressure drop
- Coolant outlet temperature
- Channel temperature rise

The model also generates three axial plots:

- Coolant and clad surface temperature
- Pin linear power
- Cumulative channel pressure drop

# GUI

The graphical interface allows the model parameters to be modified without changing the source code.

After selecting the required inputs, press **Run Analysis** to calculate the thermal-hydraulic results and update all three plots.

![PWR Thermal-Hydraulics GUI](images/PWR-Thermal-Hyrdraulics.png)

# Installation

Clone the repository and move into the project directory:

```bash
git clone https://github.com/n-sya/PWR-Thermal-Hydraulics.git
cd PWR-Thermal-Hydraulics
```

Install the required packages:

```bash
pip install -r requirements.txt
```

# Running the Model

To launch the graphical interface:

```bash
python gui.py
```

The calculation model can also be run directly:

```bash
python main.py
```

# Testing

The project contains both unit and functional tests.

Unit tests validate individual thermal-hydraulic calculations, while functional tests verify the behaviour of the complete analysis pipeline.

Run all tests using:

```bash
pytest
```

The current test suite contains 32 tests.

# Project Structure

```text
PWR-Thermal-Hydraulics/
│
├── calculations.py
├── variables.py
├── main.py
├── visualisation.py
├── gui.py
├── DERIVATIONS.md
├── README.md
├── requirements.txt
├── .gitignore
│
├── tests/
│   ├── __init__.py
│   └── test_calculations.py
│
└── functional_tests/
    ├── __init__.py
    └── test_full_analysis.py
```

# Model Assumptions and Limitations

The model is intended as an engineering and numerical modelling project rather than a detailed reactor-core analysis.

The current implementation assumes:

- Steady-state operation
- Single-phase liquid coolant
- One representative PWR subchannel
- Square fuel-rod lattice
- Constant coolant thermophysical properties
- Turbulent forced convection
- Cosine axial pin linear power distribution
- Smooth-channel friction correlation
- Channel wall-friction pressure drop only
- No spacer-grid pressure losses
- No inlet or outlet local losses
- No elevation pressure change
- No acceleration pressure drop
- No boiling
- No cross-flow between adjacent subchannels

Coolant properties are held constant throughout the channel. Therefore, changes in density, viscosity, thermal conductivity, and specific heat capacity with temperature and pressure are not currently represented.

# Future Development

Possible extensions include temperature-dependent coolant properties, spacer-grid and local pressure losses, additional heat-transfer correlations, and more detailed subchannel modelling.

