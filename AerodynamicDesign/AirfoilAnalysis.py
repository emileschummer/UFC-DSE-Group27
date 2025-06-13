import aerosandbox as asb
import numpy as np
from matplotlib import pyplot as plt
from aerosandbox import Airfoil as ASBAirfoil  # avoid conflict with local Airfoil.py
from Functions import load_airfoil_dat      # your DAT loader
import os

def main():
    # --- Parameters ---
    airfoil_data_dir = r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData"
    xfoil_path       = r"C:\Users\marco\Downloads\xfoil\XFOIL6.99\xfoil.exe"
    
    reynolds_numbers   = np.linspace(100000, 300000, 2)   # 5 points
    alpha_range_polars = np.linspace(-10, 20, 31)        # -10° to +20° in 1° steps

    airfoils_to_analyze = []

    # --- 1) Load airfoils from .dat/.txt ---
    print("Loading airfoils...")

    for fn in os.listdir(airfoil_data_dir):
        if fn.lower().endswith((".dat", ".txt")):
            path = os.path.join(airfoil_data_dir, fn)
            coords = load_airfoil_dat(path)
            name   = os.path.splitext(fn)[0]
            
            af = ASBAirfoil(name=name, coordinates=coords)
            airfoils_to_analyze.append(af)
            print(f"  Loaded: {name}")

    # --- 2) Generate polars via XFoil/AeroSandbox ---
    print("\nGenerating polars...")
    # prepare storage
    polar_results = {
        af.name: {Re: {'alpha': [], 'cl': [], 'cd': [], 'cm': []}
                  for Re in reynolds_numbers}
        for af in airfoils_to_analyze
    }

    for af in airfoils_to_analyze:
        print(f"\nProcessing {af.name}:")
        for Re in reynolds_numbers:
            print(f"  Re = {Re:,.0f}...", end="")
            # capture the returned dict
            polars_dict = af.XFoil(
                alphas=alpha_range_polars,
                Res=np.array([Re]),
                xfoil_kwargs={
                    "xfoil_command": xfoil_path,
                    "max_iter": 20,
                    "verbose": False,
                    "timeout": 60
                },
                include_compressibility_effects=False
            )
            
            if polars_dict is None:
                print(" no data generated.") # Indicates that XFoil might have failed for this Re
                continue # Skip to the next Reynolds number if polars_dict is None
            
            # If Re is not in polars_dict, df will cause an error later.
            # This is per the request to remove error handling.
            # The check above handles polars_dict being None.
            # If polars_dict is not None, but Re is still not a key (which would be unexpected
            # given Res=np.array([Re])), a KeyError might occur here as per original design.
            df = polars_dict[Re]  # typically a pandas DataFrame

            # extract arrays robustly
            alpha = np.array(df["alpha"])
            cl    = np.array(df.get("CL", []))
            cd    = np.array(df.get("CD", [])) # Retained for potential internal use or future modification
            # try common moment keys
            if "CM" in df.columns:
                cm = np.array(df["CM"])
            elif "Cm" in df.columns:
                cm = np.array(df["Cm"])
            elif "Cm_c_4" in df.columns:
                cm = np.array(df["Cm_c_4"])
            else:
                cm = np.array([]) # Retained for potential internal use or future modification

            polar_results[af.name][Re]['alpha'] = alpha
            polar_results[af.name][Re]['cl']    = cl
            polar_results[af.name][Re]['cd']    = cd
            polar_results[af.name][Re]['cm']    = cm

            print(" done.")

    # --- 3) Plotting routines ---

    # 3.2 All shapes in one 2×4 grid (or similar, depending on number of airfoils)
    n      = len(airfoils_to_analyze)
    ncols  = 2 
    nrows  = int(np.ceil(n / ncols)) if n > 0 else 1
    if n > 0: # Only plot if there are airfoils
        fig, axs = plt.subplots(nrows, ncols, figsize=(12, 4 * nrows))
        axs_flat = axs.flat if n > 1 else [axs] # Handle single airfoil case for axs
        for idx, af in enumerate(airfoils_to_analyze):
            ax = axs_flat[idx]
            ax.plot(af.coordinates[:, 0], af.coordinates[:, 1], lw=1.5)
            ax.set_aspect('equal', 'box')
            ax.set_title(af.name)
            ax.set_xlabel('x/c')
            ax.set_ylabel('y/c')
            ax.grid(True)
        # turn off extras
        for idx_off in range(n, nrows * ncols):
            if n > 1:
                axs.flat[idx_off].axis('off')
            elif nrows * ncols > 1: # handles case of 1 airfoil, but grid > 1 cell
                 axs_flat[idx_off].axis('off')


        fig.suptitle("Airfoil Shapes Comparison", fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()

    # 3.3 Helper to plot a coefficient vs α
    def plot_coeff(coeff_key, ylabel):
        # b) all airfoils in single grid
        if n > 0: # Only plot if there are airfoils
            fig_coeff, axs_coeff = plt.subplots(nrows, ncols, figsize=(12, 4 * nrows))
            axs_coeff_flat = axs_coeff.flat if n > 1 else [axs_coeff] # Handle single airfoil case

            for idx, af_plot in enumerate(airfoils_to_analyze):
                ax_c = axs_coeff_flat[idx]
                for Re_plot in reynolds_numbers:
                    data  = polar_results[af_plot.name][Re_plot]
                    alpha_plot = data['alpha']
                    y     = data[coeff_key]
                    if len(alpha_plot) > 0 and len(y) > 0: # Check if data exists before plotting
                        ax_c.plot(alpha_plot, y,
                                marker='.', markersize=3, linestyle='-',
                                label=f"Re={Re_plot:.0f}")
                ax_c.set_title(af_plot.name)
                ax_c.set_xlabel("α [deg]")
                ax_c.set_ylabel(ylabel)
                ax_c.grid(True)
                ax_c.legend(fontsize='x-small')
            
            for idx_off in range(n, nrows * ncols):
                if n > 1:
                    axs_coeff.flat[idx_off].axis('off')
                elif nrows * ncols > 1: # handles case of 1 airfoil, but grid > 1 cell
                    axs_coeff_flat[idx_off].axis('off')

            fig_coeff.suptitle(f"{ylabel} vs α for All Airfoils", fontsize=16)
            plt.tight_layout(rect=[0, 0, 1, 0.96])
            plt.show()

    # 3.4 Now plot Cl
    plot_coeff('cl', 'Cl')

    print("\nAnalysis complete.")

if __name__ == "__main__":
    main()