from calculations import (
    calculate_axial_profiles,
    calculate_channel_pressure_drop,
    calculate_coolant_velocity,
    calculate_fanning_friction_factor,
    calculate_flow_area,
    calculate_heat_transfer_coefficient,
    calculate_hydraulic_diameter,
    calculate_nusselt_number,
    calculate_outlet_temperature,
    calculate_prandtl_number,
    calculate_reynolds_number,
    calculate_wetted_perimeter,
)
from variables import (
    DEFAULT_COOLANT_DENSITY,
    DEFAULT_COOLANT_INLET_TEMPERATURE,
    DEFAULT_DYNAMIC_VISCOSITY,
    DEFAULT_FUEL_ROD_DIAMETER,
    DEFAULT_FUEL_ROD_LENGTH,
    DEFAULT_LATTICE_PITCH,
    DEFAULT_PEAK_LINEAR_POWER,
    DEFAULT_SPECIFIC_HEAT_CAPACITY,
    DEFAULT_SUBCHANNEL_MASS_FLOW_RATE,
    DEFAULT_THERMAL_CONDUCTIVITY,
)
from visualisation import show_all_plots


# Run the complete PWR subchannel thermal-hydraulics calculation
def run_analysis(
    fuel_rod_length,
    peak_linear_power,
    mass_flow_rate,
    fuel_rod_diameter,
    lattice_pitch,
    inlet_temperature,
    coolant_density,
    dynamic_viscosity,
    thermal_conductivity,
    specific_heat_capacity,
):
    flow_area = calculate_flow_area(
        lattice_pitch,
        fuel_rod_diameter,
    )

    wetted_perimeter = calculate_wetted_perimeter(
        fuel_rod_diameter,
    )

    hydraulic_diameter = calculate_hydraulic_diameter(
        flow_area,
        wetted_perimeter,
    )

    coolant_velocity = calculate_coolant_velocity(
        mass_flow_rate,
        coolant_density,
        flow_area,
    )

    reynolds_number = calculate_reynolds_number(
        coolant_density,
        coolant_velocity,
        hydraulic_diameter,
        dynamic_viscosity,
    )

    prandtl_number = calculate_prandtl_number(
        dynamic_viscosity,
        specific_heat_capacity,
        thermal_conductivity,
    )

    nusselt_number = calculate_nusselt_number(
        reynolds_number,
        prandtl_number,
    )

    heat_transfer_coefficient = calculate_heat_transfer_coefficient(
        nusselt_number,
        thermal_conductivity,
        hydraulic_diameter,
    )

    fanning_friction_factor = calculate_fanning_friction_factor(
        reynolds_number,
    )

    channel_pressure_drop = calculate_channel_pressure_drop(
        fanning_friction_factor,
        fuel_rod_length,
        hydraulic_diameter,
        coolant_density,
        coolant_velocity,
    )

    outlet_temperature = calculate_outlet_temperature(
        fuel_rod_length,
        peak_linear_power,
        mass_flow_rate,
        specific_heat_capacity,
        inlet_temperature,
    )

    temperature_rise = outlet_temperature - inlet_temperature

    return {
        "flow_area": flow_area,
        "wetted_perimeter": wetted_perimeter,
        "hydraulic_diameter": hydraulic_diameter,
        "coolant_velocity": coolant_velocity,
        "reynolds_number": reynolds_number,
        "prandtl_number": prandtl_number,
        "nusselt_number": nusselt_number,
        "heat_transfer_coefficient": heat_transfer_coefficient,
        "fanning_friction_factor": fanning_friction_factor,
        "channel_pressure_drop": channel_pressure_drop,
        "outlet_temperature": outlet_temperature,
        "temperature_rise": temperature_rise,
    }


if __name__ == "__main__":
    results = run_analysis(
        fuel_rod_length=DEFAULT_FUEL_ROD_LENGTH,
        peak_linear_power=DEFAULT_PEAK_LINEAR_POWER,
        mass_flow_rate=DEFAULT_SUBCHANNEL_MASS_FLOW_RATE,
        fuel_rod_diameter=DEFAULT_FUEL_ROD_DIAMETER,
        lattice_pitch=DEFAULT_LATTICE_PITCH,
        inlet_temperature=DEFAULT_COOLANT_INLET_TEMPERATURE,
        coolant_density=DEFAULT_COOLANT_DENSITY,
        dynamic_viscosity=DEFAULT_DYNAMIC_VISCOSITY,
        thermal_conductivity=DEFAULT_THERMAL_CONDUCTIVITY,
        specific_heat_capacity=DEFAULT_SPECIFIC_HEAT_CAPACITY,
    )

    for name, value in results.items():
        print(f"{name}: {value:.6g}")

    profiles = calculate_axial_profiles(
        channel_length=DEFAULT_FUEL_ROD_LENGTH,
        peak_linear_power=DEFAULT_PEAK_LINEAR_POWER,
        mass_flow_rate=DEFAULT_SUBCHANNEL_MASS_FLOW_RATE,
        specific_heat_capacity=DEFAULT_SPECIFIC_HEAT_CAPACITY,
        inlet_temperature=DEFAULT_COOLANT_INLET_TEMPERATURE,
        fuel_rod_diameter=DEFAULT_FUEL_ROD_DIAMETER,
        heat_transfer_coefficient=results["heat_transfer_coefficient"],
        channel_pressure_drop=results["channel_pressure_drop"],
    )

    show_all_plots(profiles)