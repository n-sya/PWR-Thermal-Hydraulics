import math

import pytest

from calculations import (
    calculate_channel_pressure_drop,
    calculate_clad_surface_temperature,
    calculate_coolant_temperature,
    calculate_coolant_velocity,
    calculate_fanning_friction_factor,
    calculate_flow_area,
    calculate_heat_transfer_coefficient,
    calculate_hydraulic_diameter,
    calculate_linear_power,
    calculate_nusselt_number,
    calculate_outlet_temperature,
    calculate_prandtl_number,
    calculate_reynolds_number,
    calculate_wetted_perimeter,
)


def test_calculate_flow_area():
    lattice_pitch = 0.0126
    fuel_rod_diameter = 0.0095

    expected = lattice_pitch**2 - math.pi * fuel_rod_diameter**2 / 4

    result = calculate_flow_area(lattice_pitch, fuel_rod_diameter)

    assert result == pytest.approx(expected)


def test_calculate_wetted_perimeter():
    fuel_rod_diameter = 0.0095

    expected = math.pi * fuel_rod_diameter

    result = calculate_wetted_perimeter(fuel_rod_diameter)

    assert result == pytest.approx(expected)


def test_calculate_hydraulic_diameter():
    flow_area = 8.786e-5
    wetted_perimeter = 0.02985

    expected = 4 * flow_area / wetted_perimeter

    result = calculate_hydraulic_diameter(
        flow_area,
        wetted_perimeter,
    )

    assert result == pytest.approx(expected)


def test_calculate_coolant_velocity():
    mass_flow_rate = 0.3
    coolant_density = 725.6
    flow_area = 8.786e-5

    expected = mass_flow_rate / (
        coolant_density * flow_area
    )

    result = calculate_coolant_velocity(
        mass_flow_rate,
        coolant_density,
        flow_area,
    )

    assert result == pytest.approx(expected)


def test_calculate_reynolds_number():
    coolant_density = 725.6
    coolant_velocity = 4.7
    hydraulic_diameter = 0.0118
    dynamic_viscosity = 8.833e-5

    expected = (
        coolant_density
        * coolant_velocity
        * hydraulic_diameter
        / dynamic_viscosity
    )

    result = calculate_reynolds_number(
        coolant_density,
        coolant_velocity,
        hydraulic_diameter,
        dynamic_viscosity,
    )

    assert result == pytest.approx(expected)


def test_calculate_prandtl_number():
    dynamic_viscosity = 8.833e-5
    specific_heat_capacity = 5476.0
    thermal_conductivity = 0.5614

    expected = (
        dynamic_viscosity
        * specific_heat_capacity
        / thermal_conductivity
    )

    result = calculate_prandtl_number(
        dynamic_viscosity,
        specific_heat_capacity,
        thermal_conductivity,
    )

    assert result == pytest.approx(expected)


def test_calculate_nusselt_number():
    reynolds_number = 100000.0
    prandtl_number = 0.862

    expected = (
        0.023
        * reynolds_number**0.8
        * prandtl_number**0.4
    )

    result = calculate_nusselt_number(
        reynolds_number,
        prandtl_number,
    )

    assert result == pytest.approx(expected)


def test_nusselt_number_rejects_non_turbulent_flow():
    with pytest.raises(ValueError):
        calculate_nusselt_number(5000.0, 1.0)


def test_calculate_heat_transfer_coefficient():
    nusselt_number = 200.0
    thermal_conductivity = 0.5614
    hydraulic_diameter = 0.0118

    expected = (
        nusselt_number
        * thermal_conductivity
        / hydraulic_diameter
    )

    result = calculate_heat_transfer_coefficient(
        nusselt_number,
        thermal_conductivity,
        hydraulic_diameter,
    )

    assert result == pytest.approx(expected)


def test_calculate_fanning_friction_factor_turbulent():
    reynolds_number = 100000.0

    expected = 0.046 * reynolds_number**-0.2

    result = calculate_fanning_friction_factor(
        reynolds_number
    )

    assert result == pytest.approx(expected)


def test_calculate_fanning_friction_factor_laminar():
    reynolds_number = 1000.0

    expected = 16 / reynolds_number

    result = calculate_fanning_friction_factor(
        reynolds_number
    )

    assert result == pytest.approx(expected)


def test_calculate_channel_pressure_drop():
    fanning_friction_factor = 0.005
    channel_length = 3.66
    hydraulic_diameter = 0.0118
    coolant_density = 725.6
    coolant_velocity = 4.7

    expected = (
        2
        * fanning_friction_factor
        * channel_length
        * coolant_density
        * coolant_velocity**2
        / hydraulic_diameter
    )

    result = calculate_channel_pressure_drop(
        fanning_friction_factor,
        channel_length,
        hydraulic_diameter,
        coolant_density,
        coolant_velocity,
    )

    assert result == pytest.approx(expected)


def test_linear_power_is_peak_at_channel_centre():
    channel_length = 3.66
    peak_linear_power = 25000.0

    result = calculate_linear_power(
        0.0,
        channel_length,
        peak_linear_power,
    )

    assert result == pytest.approx(peak_linear_power)


def test_linear_power_is_zero_at_channel_ends():
    channel_length = 3.66
    peak_linear_power = 25000.0

    inlet = calculate_linear_power(
        -channel_length / 2,
        channel_length,
        peak_linear_power,
    )

    outlet = calculate_linear_power(
        channel_length / 2,
        channel_length,
        peak_linear_power,
    )

    assert inlet == pytest.approx(0.0, abs=1e-10)
    assert outlet == pytest.approx(0.0, abs=1e-10)


def test_coolant_temperature_equals_inlet_temperature_at_inlet():
    channel_length = 3.66
    inlet_temperature = 573.0

    result = calculate_coolant_temperature(
        -channel_length / 2,
        channel_length,
        25000.0,
        0.3,
        5476.0,
        inlet_temperature,
    )

    assert result == pytest.approx(inlet_temperature)


def test_outlet_temperature_matches_axial_temperature_function():
    channel_length = 3.66
    peak_linear_power = 25000.0
    mass_flow_rate = 0.3
    specific_heat_capacity = 5476.0
    inlet_temperature = 573.0

    axial_result = calculate_coolant_temperature(
        channel_length / 2,
        channel_length,
        peak_linear_power,
        mass_flow_rate,
        specific_heat_capacity,
        inlet_temperature,
    )

    outlet_result = calculate_outlet_temperature(
        channel_length,
        peak_linear_power,
        mass_flow_rate,
        specific_heat_capacity,
        inlet_temperature,
    )

    assert outlet_result == pytest.approx(axial_result)


def test_clad_temperature_is_above_coolant_when_power_is_positive():
    coolant_temperature = 600.0
    linear_power = 25000.0
    fuel_rod_diameter = 0.0095
    heat_transfer_coefficient = 30000.0

    result = calculate_clad_surface_temperature(
        coolant_temperature,
        linear_power,
        fuel_rod_diameter,
        heat_transfer_coefficient,
    )

    assert result > coolant_temperature