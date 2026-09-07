import matplotlib.pyplot as plt


# Plot the axial pin linear power distribution
def plot_linear_power(profiles):
    axial_position = profiles["axial_position"]
    linear_power = profiles["linear_power"]

    figure, axis = plt.subplots()

    axis.plot(
        axial_position,
        linear_power / 1000,
    )

    axis.set_xlabel("Axial Position (m)")
    axis.set_ylabel("Linear Power (kW/m)")
    axis.set_title("Axial Pin Linear Power Distribution")
    axis.grid(True)

    figure.tight_layout()

    return figure


# Plot the cumulative channel pressure drop
def plot_pressure_drop(profiles):
    distance_from_inlet = profiles["distance_from_inlet"]
    pressure_drop = profiles["pressure_drop"]

    figure, axis = plt.subplots()

    axis.plot(
        distance_from_inlet,
        pressure_drop / 1000,
    )

    axis.set_xlabel("Distance from Inlet (m)")
    axis.set_ylabel("Pressure Drop (kPa)")
    axis.set_title("Channel Pressure Drop")
    axis.grid(True)

    figure.tight_layout()

    return figure


# Plot the coolant and clad surface temperature distributions
def plot_temperature_distribution(profiles):
    axial_position = profiles["axial_position"]
    coolant_temperature = profiles["coolant_temperature"]
    clad_surface_temperature = profiles["clad_surface_temperature"]

    figure, axis = plt.subplots()

    axis.plot(
        axial_position,
        coolant_temperature,
        label="Coolant",
    )

    axis.plot(
        axial_position,
        clad_surface_temperature,
        label="Clad Surface",
    )

    axis.set_xlabel("Axial Position (m)")
    axis.set_ylabel("Temperature (K)")
    axis.set_title("Axial Temperature Distribution")
    axis.legend()
    axis.grid(True)

    figure.tight_layout()

    return figure


# Display all thermal-hydraulic plots
def show_all_plots(profiles):
    plot_linear_power(profiles)
    plot_pressure_drop(profiles)
    plot_temperature_distribution(profiles)

    plt.show()