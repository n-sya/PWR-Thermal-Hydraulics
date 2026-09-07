import math


# Calculate the coolant flow area for one square-lattice subchannel
def calculate_flow_area(lattice_pitch, fuel_rod_diameter):
    if lattice_pitch <= 0:
        raise ValueError("Lattice pitch must be greater than zero.")

    if fuel_rod_diameter <= 0:
        raise ValueError("Fuel rod diameter must be greater than zero.")

    flow_area = lattice_pitch**2 - (
        math.pi * fuel_rod_diameter**2
    ) / 4

    if flow_area <= 0:
        raise ValueError(
            "Flow area must be greater than zero. Check lattice pitch and fuel rod diameter."
        )

    return flow_area


# Calculate the wetted perimeter of one fuel rod
def calculate_wetted_perimeter(fuel_rod_diameter):
    if fuel_rod_diameter <= 0:
        raise ValueError("Fuel rod diameter must be greater than zero.")

    return math.pi * fuel_rod_diameter


# Calculate the hydraulic diameter
def calculate_hydraulic_diameter(flow_area, wetted_perimeter):
    if flow_area <= 0:
        raise ValueError("Flow area must be greater than zero.")

    if wetted_perimeter <= 0:
        raise ValueError("Wetted perimeter must be greater than zero.")

    return 4 * flow_area / wetted_perimeter


# Calculate the mean coolant velocity
def calculate_coolant_velocity(
    mass_flow_rate,
    coolant_density,
    flow_area,
):
    if mass_flow_rate <= 0:
        raise ValueError("Mass flow rate must be greater than zero.")

    if coolant_density <= 0:
        raise ValueError("Coolant density must be greater than zero.")

    if flow_area <= 0:
        raise ValueError("Flow area must be greater than zero.")

    return mass_flow_rate / (coolant_density * flow_area)


# Calculate the Reynolds number
def calculate_reynolds_number(
    coolant_density,
    coolant_velocity,
    hydraulic_diameter,
    dynamic_viscosity,
):
    if coolant_density <= 0:
        raise ValueError("Coolant density must be greater than zero.")

    if coolant_velocity < 0:
        raise ValueError("Coolant velocity must not be negative.")

    if hydraulic_diameter <= 0:
        raise ValueError("Hydraulic diameter must be greater than zero.")

    if dynamic_viscosity <= 0:
        raise ValueError("Dynamic viscosity must be greater than zero.")

    return (
        coolant_density
        * coolant_velocity
        * hydraulic_diameter
        / dynamic_viscosity
    )


# Calculate the Prandtl number
def calculate_prandtl_number(
    dynamic_viscosity,
    specific_heat_capacity,
    thermal_conductivity,
):
    if dynamic_viscosity <= 0:
        raise ValueError("Dynamic viscosity must be greater than zero.")

    if specific_heat_capacity <= 0:
        raise ValueError(
            "Specific heat capacity must be greater than zero."
        )

    if thermal_conductivity <= 0:
        raise ValueError(
            "Thermal conductivity must be greater than zero."
        )

    return (
        dynamic_viscosity
        * specific_heat_capacity
        / thermal_conductivity
    )


# Calculate the Nusselt number using the Dittus-Boelter correlation
def calculate_nusselt_number(reynolds_number, prandtl_number):
    if reynolds_number <= 0:
        raise ValueError("Reynolds number must be greater than zero.")

    if prandtl_number <= 0:
        raise ValueError("Prandtl number must be greater than zero.")

    return (
        0.023
        * reynolds_number**0.8
        * prandtl_number**0.4
    )


# Calculate the convective heat transfer coefficient
def calculate_heat_transfer_coefficient(
    nusselt_number,
    thermal_conductivity,
    hydraulic_diameter,
):
    if nusselt_number <= 0:
        raise ValueError("Nusselt number must be greater than zero.")

    if thermal_conductivity <= 0:
        raise ValueError(
            "Thermal conductivity must be greater than zero."
        )

    if hydraulic_diameter <= 0:
        raise ValueError("Hydraulic diameter must be greater than zero.")

    return (
        nusselt_number
        * thermal_conductivity
        / hydraulic_diameter
    )


# Calculate the Fanning friction factor
def calculate_fanning_friction_factor(reynolds_number):
    if reynolds_number <= 0:
        raise ValueError("Reynolds number must be greater than zero.")

    if reynolds_number < 2300:
        return 16 / reynolds_number

    return 0.046 * reynolds_number**-0.2


# Calculate the channel pressure drop due to wall friction
def calculate_channel_pressure_drop(
    fanning_friction_factor,
    channel_length,
    hydraulic_diameter,
    coolant_density,
    coolant_velocity,
):
    if fanning_friction_factor <= 0:
        raise ValueError(
            "Fanning friction factor must be greater than zero."
        )

    if channel_length <= 0:
        raise ValueError("Channel length must be greater than zero.")

    if hydraulic_diameter <= 0:
        raise ValueError("Hydraulic diameter must be greater than zero.")

    if coolant_density <= 0:
        raise ValueError("Coolant density must be greater than zero.")

    if coolant_velocity < 0:
        raise ValueError("Coolant velocity must not be negative.")

    return (
        2
        * fanning_friction_factor
        * channel_length
        * coolant_density
        * coolant_velocity**2
        / hydraulic_diameter
    )


# Calculate the axial pin linear power
def calculate_linear_power(
    axial_position,
    channel_length,
    peak_linear_power,
):
    if channel_length <= 0:
        raise ValueError("Channel length must be greater than zero.")

    if peak_linear_power < 0:
        raise ValueError("Peak linear power must not be negative.")

    if abs(axial_position) > channel_length / 2:
        raise ValueError(
            "Axial position must lie within the fuel rod length."
        )

    return peak_linear_power * math.cos(
        math.pi * axial_position / channel_length
    )


# Calculate the coolant temperature at an axial position
def calculate_coolant_temperature(
    axial_position,
    channel_length,
    peak_linear_power,
    mass_flow_rate,
    specific_heat_capacity,
    inlet_temperature,
):
    if channel_length <= 0:
        raise ValueError("Channel length must be greater than zero.")

    if peak_linear_power < 0:
        raise ValueError("Peak linear power must not be negative.")

    if mass_flow_rate <= 0:
        raise ValueError("Mass flow rate must be greater than zero.")

    if specific_heat_capacity <= 0:
        raise ValueError(
            "Specific heat capacity must be greater than zero."
        )

    if abs(axial_position) > channel_length / 2:
        raise ValueError(
            "Axial position must lie within the fuel rod length."
        )

    temperature_rise = (
        peak_linear_power
        * channel_length
        / (
            math.pi
            * mass_flow_rate
            * specific_heat_capacity
        )
        * (
            math.sin(
                math.pi
                * axial_position
                / channel_length
            )
            + 1
        )
    )

    return inlet_temperature + temperature_rise


# Calculate the coolant outlet temperature
def calculate_outlet_temperature(
    channel_length,
    peak_linear_power,
    mass_flow_rate,
    specific_heat_capacity,
    inlet_temperature,
):
    temperature_rise = (
        2
        * peak_linear_power
        * channel_length
        / (
            math.pi
            * mass_flow_rate
            * specific_heat_capacity
        )
    )

    return inlet_temperature + temperature_rise


# Calculate the clad surface temperature
def calculate_clad_surface_temperature(
    coolant_temperature,
    linear_power,
    fuel_rod_diameter,
    heat_transfer_coefficient,
):
    if fuel_rod_diameter <= 0:
        raise ValueError("Fuel rod diameter must be greater than zero.")

    if heat_transfer_coefficient <= 0:
        raise ValueError(
            "Heat transfer coefficient must be greater than zero."
        )

    if linear_power < 0:
        raise ValueError("Linear power must not be negative.")

    return (
        coolant_temperature
        + linear_power
        / (
            math.pi
            * fuel_rod_diameter
            * heat_transfer_coefficient
        )
    )