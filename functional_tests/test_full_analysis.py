import math

import pytest

from main import run_analysis


def test_full_analysis_returns_expected_outputs():
    results = run_analysis(
        fuel_rod_length=3.66,
        peak_linear_power=25000.0,
        mass_flow_rate=0.3,
        fuel_rod_diameter=0.0095,
        lattice_pitch=0.0126,
        inlet_temperature=573.0,
        coolant_density=725.6,
        dynamic_viscosity=8.833e-5,
        thermal_conductivity=0.5614,
        specific_heat_capacity=5476.0,
    )

    expected_outputs = {
        "flow_area",
        "wetted_perimeter",
        "hydraulic_diameter",
        "coolant_velocity",
        "reynolds_number",
        "prandtl_number",
        "nusselt_number",
        "heat_transfer_coefficient",
        "peak_heat_flux",
        "peak_boundary_layer_temperature_difference",
        "fanning_friction_factor",
        "channel_pressure_drop",
        "outlet_temperature",
        "temperature_rise",
    }

    assert set(results.keys()) == expected_outputs


def test_full_analysis_produces_physically_consistent_results():
    inlet_temperature = 573.0
    peak_linear_power = 25000.0
    fuel_rod_diameter = 0.0095

    results = run_analysis(
        fuel_rod_length=3.66,
        peak_linear_power=peak_linear_power,
        mass_flow_rate=0.3,
        fuel_rod_diameter=fuel_rod_diameter,
        lattice_pitch=0.0126,
        inlet_temperature=inlet_temperature,
        coolant_density=725.6,
        dynamic_viscosity=8.833e-5,
        thermal_conductivity=0.5614,
        specific_heat_capacity=5476.0,
    )

    assert results["flow_area"] > 0
    assert results["hydraulic_diameter"] > 0
    assert results["coolant_velocity"] > 0
    assert results["reynolds_number"] >= 10000
    assert results["prandtl_number"] > 0
    assert results["nusselt_number"] > 0
    assert results["heat_transfer_coefficient"] > 0
    assert results["fanning_friction_factor"] > 0
    assert results["channel_pressure_drop"] > 0
    assert results["outlet_temperature"] > inlet_temperature
    assert results["temperature_rise"] > 0

    expected_peak_heat_flux = peak_linear_power / (
        math.pi * fuel_rod_diameter
    )

    assert results["peak_heat_flux"] == pytest.approx(
        expected_peak_heat_flux
    )

    expected_boundary_layer_temperature_difference = (
        results["peak_heat_flux"]
        / results["heat_transfer_coefficient"]
    )

    assert results[
        "peak_boundary_layer_temperature_difference"
    ] == pytest.approx(
        expected_boundary_layer_temperature_difference
    )


def test_channel_temperature_rise_matches_outlet_minus_inlet():
    inlet_temperature = 573.0

    results = run_analysis(
        fuel_rod_length=3.66,
        peak_linear_power=25000.0,
        mass_flow_rate=0.3,
        fuel_rod_diameter=0.0095,
        lattice_pitch=0.0126,
        inlet_temperature=inlet_temperature,
        coolant_density=725.6,
        dynamic_viscosity=8.833e-5,
        thermal_conductivity=0.5614,
        specific_heat_capacity=5476.0,
    )

    expected_temperature_rise = (
        results["outlet_temperature"] - inlet_temperature
    )

    assert results["temperature_rise"] == pytest.approx(
        expected_temperature_rise
    )


def test_increasing_mass_flow_rate_reduces_temperature_rise():
    low_flow_results = run_analysis(
        fuel_rod_length=3.66,
        peak_linear_power=25000.0,
        mass_flow_rate=0.3,
        fuel_rod_diameter=0.0095,
        lattice_pitch=0.0126,
        inlet_temperature=573.0,
        coolant_density=725.6,
        dynamic_viscosity=8.833e-5,
        thermal_conductivity=0.5614,
        specific_heat_capacity=5476.0,
    )

    high_flow_results = run_analysis(
        fuel_rod_length=3.66,
        peak_linear_power=25000.0,
        mass_flow_rate=0.6,
        fuel_rod_diameter=0.0095,
        lattice_pitch=0.0126,
        inlet_temperature=573.0,
        coolant_density=725.6,
        dynamic_viscosity=8.833e-5,
        thermal_conductivity=0.5614,
        specific_heat_capacity=5476.0,
    )

    assert (
        high_flow_results["temperature_rise"]
        < low_flow_results["temperature_rise"]
    )


def test_increasing_mass_flow_rate_increases_pressure_drop():
    low_flow_results = run_analysis(
        fuel_rod_length=3.66,
        peak_linear_power=25000.0,
        mass_flow_rate=0.3,
        fuel_rod_diameter=0.0095,
        lattice_pitch=0.0126,
        inlet_temperature=573.0,
        coolant_density=725.6,
        dynamic_viscosity=8.833e-5,
        thermal_conductivity=0.5614,
        specific_heat_capacity=5476.0,
    )

    high_flow_results = run_analysis(
        fuel_rod_length=3.66,
        peak_linear_power=25000.0,
        mass_flow_rate=0.6,
        fuel_rod_diameter=0.0095,
        lattice_pitch=0.0126,
        inlet_temperature=573.0,
        coolant_density=725.6,
        dynamic_viscosity=8.833e-5,
        thermal_conductivity=0.5614,
        specific_heat_capacity=5476.0,
    )

    assert (
        high_flow_results["channel_pressure_drop"]
        > low_flow_results["channel_pressure_drop"]
    )