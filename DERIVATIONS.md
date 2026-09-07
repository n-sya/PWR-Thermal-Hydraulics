# PWR Thermal-Hydraulics Model

This model performs a steady-state, single-phase thermal-hydraulic analysis of a simplified PWR coolant subchannel.

# Inputs

- Fuel rod length, $L$
- Peak pin linear power, $q'_{\text{peak}}$
- Subchannel mass flow rate, $\dot{m}$
- Fuel rod outside diameter, $d$
- Fuel assembly square lattice pitch, $p$
- Coolant inlet temperature, $T_{\text{in}}$
- Coolant pressure, $P$
- Coolant density, $\rho$
- Dynamic viscosity, $\mu$
- Thermal conductivity, $k$
- Specific heat capacity, $c_p$

All inputs are user-editable in the GUI. Default values may be provided.

# Subchannel Geometry

For a square lattice, the coolant flow area associated with one fuel rod is:

$$A_f = p^2 - \frac{\pi d^2}{4}$$

The wetted perimeter is:

$$P_w = \pi d$$

The hydraulic diameter is:

$$D_h = \frac{4A_f}{P_w}$$

# Coolant Velocity

The mean coolant velocity is:

$$u = \frac{\dot{m}}{\rho A_f}$$

# Reynolds Number

The Reynolds number is:

$$Re = \frac{\rho u D_h}{\mu}$$

Substituting for coolant velocity gives:

$$Re = \frac{\dot{m}D_h}{\mu A_f}$$

# Prandtl Number

The Prandtl number is:

$$Pr = \frac{\mu c_p}{k}$$

# Nusselt Number

For turbulent forced convection, the Dittus-Boelter correlation is used:

$$Nu = 0.023Re^{0.8}Pr^{0.4}$$

# Heat Transfer Coefficient

The convective heat transfer coefficient is obtained from:

$$Nu = \frac{hD_h}{k}$$

Therefore:

$$h = \frac{Nu\,k}{D_h}$$

# Peak Heat Flux

The local heat flux at the fuel rod surface is related to the linear power by:

$$q''(z) = \frac{q'(z)}{\pi d}$$

The peak heat flux therefore occurs at the peak linear power:

$$q''_{\text{peak}} = \frac{q'_{\text{peak}}}{\pi d}$$

# Peak Boundary Layer Temperature Difference

The temperature difference between the clad surface and bulk coolant due to convection is:

$$\Delta T_{\text{BL}} = \frac{q''}{h}$$

Therefore, the peak boundary layer temperature difference is:

$$\Delta T_{\text{BL,peak}} = \frac{q''_{\text{peak}}}{h}$$

# Fanning Friction Factor

For turbulent flow:

$$f_F = 0.046Re^{-0.2}$$

For laminar flow:

$$f_F = \frac{16}{Re}$$

# Channel Pressure Drop

The channel pressure drop due to wall friction is calculated using the Fanning friction factor:

$$\Delta P_{\text{channel}} = \frac{2f_FL}{D_h}\rho u^2$$

For constant coolant properties, the pressure drop from the inlet to any axial position $x$ is:

$$\Delta P(x) = \frac{2f_Fx}{D_h}\rho u^2$$

where $x=0$ at the channel inlet and $x=L$ at the channel outlet.

# Axial Pin Linear Power

The axial pin linear power distribution is represented using a cosine profile:

$$q'(z) = q'_{\text{peak}}\cos\left(\frac{\pi z}{L}\right)$$

where:

$$-\frac{L}{2} \leq z \leq \frac{L}{2}$$

and the peak linear power occurs at:

$$z = 0$$

# Coolant Temperature Distribution

A steady-flow energy balance gives:

$$\dot{m}c_p\frac{dT}{dz} = q'(z)$$

Integrating from the channel inlet at $z=-L/2$ gives:

$$T(z) - T_{\text{in}} = \frac{1}{\dot{m}c_p}\int_{-L/2}^{z}q'(\xi)\,d\xi$$

Substituting the cosine power distribution:

$$T(z) = T_{\text{in}} + \frac{q'_{\text{peak}}L}{\pi\dot{m}c_p}\left[\sin\left(\frac{\pi z}{L}\right)+1\right]$$

At the outlet:

$$T_{\text{out}} - T_{\text{in}} = \frac{2q'_{\text{peak}}L}{\pi\dot{m}c_p}$$

# Clad Surface Temperature

The local heat flux at the cladding surface is related to the linear power by:

$$q''(z) = \frac{q'(z)}{\pi d}$$

Using convection:

$$q''(z) = h[T_c(z)-T(z)]$$

Therefore:

$$T_c(z) = T(z) + \frac{q'(z)}{\pi dh}$$

# Model Outputs

The model calculates:

- Flow area
- Wetted perimeter
- Hydraulic diameter
- Coolant velocity
- Reynolds number
- Prandtl number
- Nusselt number
- Heat transfer coefficient
- Fanning friction factor
- Channel pressure drop
- Coolant outlet temperature
- Coolant temperature rise
- Axial pin linear power distribution
- Axial coolant temperature distribution
- Axial clad surface temperature distribution

# Model Assumptions

The model assumes:

- Steady-state operation
- Single-phase liquid coolant
- One representative PWR subchannel
- Square fuel-rod lattice
- Constant coolant properties
- Forced convection
- Cosine axial linear power distribution
- Smooth-channel friction correlation
- Channel wall-friction pressure drop only
- No spacer-grid losses
- No inlet or outlet local losses
- No elevation pressure change
- No acceleration pressure drop
- No boiling
- No cross-flow between adjacent subchannels