import os
import numpy as np
from matplotlib import pyplot as plt
from aerosandbox import Airfoil
import tqdm  # for progress bars, optional

def main():
    # --- Parameters ---
    airfoil_data_dir = r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData"
    xfoil_path       = r"C:\Users\marco\Downloads\xfoil\XFOIL6.99\xfoil.exe"
    
    reynolds_numbers   = np.linspace(1e5, 5e5, 10)   # 2 points
    alpha_range_polars = np.linspace(-10, 30, 41)  # -10° to +30° in 1° steps

    # --- 1) Load airfoils from .dat/.txt ---
    print("Loading airfoils...")
    airfoils = []
    for fn in os.listdir(airfoil_data_dir): 
        if fn.lower().endswith((".dat", ".txt")):
            path = os.path.join(airfoil_data_dir, fn)
            name = os.path.splitext(fn)[0]
            # Airfoil will auto-load from a file if you pass the filepath
            af = Airfoil(name=name, coordinates=path)
            airfoils.append(af)
            print(f"  Loaded: {name}")

    # Prepare storage
    polar_results = {
        af.name: {
            Re: {"alpha": [], "cl": [], "cd": [], "cm": []}
            for Re in reynolds_numbers
        }
        for af in airfoils
    }

    # --- 2) Generate polars via XFoil/AeroSandbox ---
    print("\nGenerating polars (this may take a minute)…")
    for af in airfoils:
        print(f"  → {af.name}:")
        af.generate_polars(
            alphas=alpha_range_polars,
            Res=reynolds_numbers,
            xfoil_kwargs={
                "xfoil_command": xfoil_path,
                "max_iter": 20,
                "verbose": False,
                "timeout": 60
            },
            include_compressibility_effects=False
        )

        # Now slice the raw data by each Re
        data = af.xfoil_data
        for Re in reynolds_numbers:
            mask = data["Re"] == Re
            polar_results[af.name][Re]["alpha"] = data["alpha"][mask]
            polar_results[af.name][Re]["cl"]    = data["CL"][mask]
            polar_results[af.name][Re]["cd"]    = data["CD"][mask]
            polar_results[af.name][Re]["cm"]    = data.get("CM", np.array([]))[mask]

    # --- 3) Plotting routines ---
    n_all_airfoils = len(airfoils) # Renamed for clarity
    ncols_global   = 2 
    nrows_global   = int(np.ceil(n_all_airfoils / ncols_global)) if n_all_airfoils > 0 else 1
    
    if n_all_airfoils > 0:
        # 3.1 Airfoil Shapes
        fig, axs = plt.subplots(nrows_global, ncols_global, figsize=(12, 4 * nrows_global))
        axs_flat = axs.flat if n_all_airfoils > 1 else [axs]
        for idx, af in enumerate(airfoils):
            ax = axs_flat[idx]
            ax.plot(af.coordinates[:, 0], af.coordinates[:, 1], lw=1.5)
            ax.set_aspect('equal', 'box')
            ax.set_title(af.name)
            ax.set_xlabel('x/c'); ax.set_ylabel('y/c')
            ax.grid(True)
        for idx_off in range(n_all_airfoils, nrows_global * ncols_global):
            axs_flat[idx_off].axis('off')
        # fig.suptitle("Airfoil Shapes Comparison", fontsize=16)
        plt.tight_layout(pad=3.0)  # Increased padding
        plt.show()

        # 3.2 Helper to plot coefficient vs α
        def plot_coeff(coeff_key, ylabel, fig_title):
            airfoils_to_plot = []
            if coeff_key in ["cd", "cm"]:
                target_names = ["S1223", "FX 74-Cl5-140MOD"]
                airfoils_to_plot = [af for af in airfoils if af.name in target_names]
            else:
                airfoils_to_plot = airfoils

            n_plot = len(airfoils_to_plot)
            if n_plot == 0:
                print(f"No airfoils selected for plotting {coeff_key}.")
                return

            ncols_plot = 2
            nrows_plot = int(np.ceil(n_plot / ncols_plot)) if n_plot > 0 else 1
            
            fig_c, axs_c = plt.subplots(nrows_plot, ncols_plot, figsize=(12, 4 * nrows_plot), squeeze=False)
            axs_flat_c = axs_c.flat

            for idx, af in enumerate(airfoils_to_plot):
                ax = axs_flat_c[idx]
                for Re in reynolds_numbers:
                    a = polar_results[af.name][Re]["alpha"]
                    y = polar_results[af.name][Re][coeff_key]
                    if a.size and y.size:
                        ax.plot(a, y, marker='.', ms=3, ls='-',
                                label=f"Re={Re/1e5:.1f}e5")
                ax.set_title(af.name)
                ax.set_xlabel("α [deg]"); ax.set_ylabel(ylabel)
                ax.grid(True)
                ax.legend(fontsize='x-small', loc='upper left')  # Legend in the top left corner
            
            for idx_off in range(n_plot, nrows_plot * ncols_plot):
                axs_flat_c[idx_off].axis('off')
            # fig_c.suptitle(fig_title, fontsize=16)
            plt.tight_layout(pad=3.0)  # Increased padding
            plt.show()

        # Plot Cl in one figure
        plot_coeff("cl", "Cl", "Cl vs α for All Airfoils")

        # Plot Cd in another figure
        plot_coeff("cd", "Cd", "Cd vs α for All Airfoils")

        # Plot Cm in a third figure
        plot_coeff("cm", "Cm", "Cm vs α for All Airfoils")

    print("\nAnalysis complete.")

if __name__ == "__main__":
    main()
