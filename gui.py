import tkinter as tk
from tkinter import messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from calculations import calculate_axial_profiles
from main import run_analysis
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
from visualisation import (
    plot_linear_power,
    plot_pressure_drop,
    plot_temperature_distribution,
)


class PWRThermalHydraulicsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PWR Thermal-Hydraulics")
        self.root.geometry("1400x850")
        self.root.minsize(1200, 700)

        self.input_entries = {}
        self.result_labels = {}
        self.plot_canvases = []

        self.create_layout()

    def create_layout(self):
        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_plot_area()

    def create_sidebar(self):
        sidebar = ttk.Frame(self.root, padding=15)
        sidebar.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        title = ttk.Label(
            sidebar,
            text="PWR Thermal-Hydraulics",
            font=("Segoe UI", 16, "bold"),
        )
        title.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=(0, 15),
        )

        input_frame = ttk.LabelFrame(
            sidebar,
            text="Model Inputs",
            padding=10,
        )
        input_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
        )

        inputs = [
            (
                "Fuel Rod Length (m)",
                "fuel_rod_length",
                DEFAULT_FUEL_ROD_LENGTH,
            ),
            (
                "Peak Linear Power (W/m)",
                "peak_linear_power",
                DEFAULT_PEAK_LINEAR_POWER,
            ),
            (
                "Mass Flow Rate (kg/s)",
                "mass_flow_rate",
                DEFAULT_SUBCHANNEL_MASS_FLOW_RATE,
            ),
            (
                "Fuel Rod Diameter (m)",
                "fuel_rod_diameter",
                DEFAULT_FUEL_ROD_DIAMETER,
            ),
            (
                "Lattice Pitch (m)",
                "lattice_pitch",
                DEFAULT_LATTICE_PITCH,
            ),
            (
                "Inlet Temperature (K)",
                "inlet_temperature",
                DEFAULT_COOLANT_INLET_TEMPERATURE,
            ),
            (
                "Coolant Density (kg/m³)",
                "coolant_density",
                DEFAULT_COOLANT_DENSITY,
            ),
            (
                "Dynamic Viscosity (kg/m·s)",
                "dynamic_viscosity",
                DEFAULT_DYNAMIC_VISCOSITY,
            ),
            (
                "Thermal Conductivity (W/m·K)",
                "thermal_conductivity",
                DEFAULT_THERMAL_CONDUCTIVITY,
            ),
            (
                "Specific Heat Capacity (J/kg·K)",
                "specific_heat_capacity",
                DEFAULT_SPECIFIC_HEAT_CAPACITY,
            ),
        ]

        for row, (label_text, variable_name, default_value) in enumerate(
            inputs
        ):
            label = ttk.Label(
                input_frame,
                text=label_text,
            )
            label.grid(
                row=row,
                column=0,
                sticky="w",
                padx=(0, 10),
                pady=3,
            )

            entry = ttk.Entry(
                input_frame,
                width=15,
            )
            entry.insert(0, str(default_value))
            entry.grid(
                row=row,
                column=1,
                sticky="ew",
                pady=3,
            )

            self.input_entries[variable_name] = entry

        run_button = ttk.Button(
            sidebar,
            text="Run Analysis",
            command=self.run_analysis,
        )
        run_button.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=12,
        )

        results_frame = ttk.LabelFrame(
            sidebar,
            text="Results",
            padding=10,
        )
        results_frame.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
        )

        results = [
            ("Reynolds Number", "reynolds_number"),
            ("Prandtl Number", "prandtl_number"),
            ("Nusselt Number", "nusselt_number"),
            (
                "Heat Transfer Coefficient",
                "heat_transfer_coefficient",
            ),
            (
                "Fanning Friction Factor",
                "fanning_friction_factor",
            ),
            (
                "Pressure Drop",
                "channel_pressure_drop",
            ),
            (
                "Outlet Temperature",
                "outlet_temperature",
            ),
            (
                "Temperature Rise",
                "temperature_rise",
            ),
        ]

        for row, (label_text, result_name) in enumerate(results):
            label = ttk.Label(
                results_frame,
                text=f"{label_text}:",
            )
            label.grid(
                row=row,
                column=0,
                sticky="w",
                padx=(0, 10),
                pady=2,
            )

            value_label = ttk.Label(
                results_frame,
                text="--",
            )
            value_label.grid(
                row=row,
                column=1,
                sticky="e",
                pady=2,
            )

            self.result_labels[result_name] = value_label

    def create_plot_area(self):
        plot_frame = ttk.Frame(
            self.root,
            padding=(0, 15, 15, 15),
        )
        plot_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)

        self.notebook = ttk.Notebook(plot_frame)
        self.notebook.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        self.temperature_tab = ttk.Frame(self.notebook)
        self.linear_power_tab = ttk.Frame(self.notebook)
        self.pressure_drop_tab = ttk.Frame(self.notebook)

        self.notebook.add(
            self.temperature_tab,
            text="Temperature Distribution",
        )
        self.notebook.add(
            self.linear_power_tab,
            text="Linear Power",
        )
        self.notebook.add(
            self.pressure_drop_tab,
            text="Pressure Drop",
        )

        for tab in (
            self.temperature_tab,
            self.linear_power_tab,
            self.pressure_drop_tab,
        ):
            tab.columnconfigure(0, weight=1)
            tab.rowconfigure(0, weight=1)

        placeholder = ttk.Label(
            self.temperature_tab,
            text="Run the analysis to display results.",
            anchor="center",
        )
        placeholder.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

    def get_inputs(self):
        return {
            name: float(entry.get())
            for name, entry in self.input_entries.items()
        }

    def run_analysis(self):
        try:
            inputs = self.get_inputs()

            results = run_analysis(
                fuel_rod_length=inputs["fuel_rod_length"],
                peak_linear_power=inputs["peak_linear_power"],
                mass_flow_rate=inputs["mass_flow_rate"],
                fuel_rod_diameter=inputs["fuel_rod_diameter"],
                lattice_pitch=inputs["lattice_pitch"],
                inlet_temperature=inputs["inlet_temperature"],
                coolant_density=inputs["coolant_density"],
                dynamic_viscosity=inputs["dynamic_viscosity"],
                thermal_conductivity=inputs["thermal_conductivity"],
                specific_heat_capacity=inputs[
                    "specific_heat_capacity"
                ],
            )

            profiles = calculate_axial_profiles(
                channel_length=inputs["fuel_rod_length"],
                peak_linear_power=inputs["peak_linear_power"],
                mass_flow_rate=inputs["mass_flow_rate"],
                specific_heat_capacity=inputs[
                    "specific_heat_capacity"
                ],
                inlet_temperature=inputs["inlet_temperature"],
                fuel_rod_diameter=inputs["fuel_rod_diameter"],
                heat_transfer_coefficient=results[
                    "heat_transfer_coefficient"
                ],
                channel_pressure_drop=results[
                    "channel_pressure_drop"
                ],
            )

            self.update_results(results)
            self.update_plots(profiles)

            self.notebook.select(self.temperature_tab)

        except ValueError as error:
            messagebox.showerror(
                "Invalid Input",
                str(error),
            )

    def update_results(self, results):
        display_values = {
            "reynolds_number": f'{results["reynolds_number"]:.3e}',
            "prandtl_number": f'{results["prandtl_number"]:.3f}',
            "nusselt_number": f'{results["nusselt_number"]:.3f}',
            "heat_transfer_coefficient": (
                f'{results["heat_transfer_coefficient"]:.3f} W/m²·K'
            ),
            "fanning_friction_factor": (
                f'{results["fanning_friction_factor"]:.5f}'
            ),
            "channel_pressure_drop": (
                f'{results["channel_pressure_drop"] / 1000:.3f} kPa'
            ),
            "outlet_temperature": (
                f'{results["outlet_temperature"]:.3f} K'
            ),
            "temperature_rise": (
                f'{results["temperature_rise"]:.3f} K'
            ),
        }

        for name, value in display_values.items():
            self.result_labels[name].config(text=value)

    def update_plots(self, profiles):
        for canvas in self.plot_canvases:
            canvas.get_tk_widget().destroy()

        self.plot_canvases.clear()

        temperature_figure = plot_temperature_distribution(profiles)
        linear_power_figure = plot_linear_power(profiles)
        pressure_drop_figure = plot_pressure_drop(profiles)

        figures_and_tabs = [
            (
                temperature_figure,
                self.temperature_tab,
            ),
            (
                linear_power_figure,
                self.linear_power_tab,
            ),
            (
                pressure_drop_figure,
                self.pressure_drop_tab,
            ),
        ]

        for figure, tab in figures_and_tabs:
            for widget in tab.winfo_children():
                widget.destroy()

            canvas = FigureCanvasTkAgg(
                figure,
                master=tab,
            )
            canvas.draw()
            canvas.get_tk_widget().grid(
                row=0,
                column=0,
                sticky="nsew",
            )

            self.plot_canvases.append(canvas)


def main():
    root = tk.Tk()
    PWRThermalHydraulicsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()