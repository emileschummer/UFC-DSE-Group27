import pandas as pd
import os
import matplotlib.pyplot as plt

def plot_cl_vs_cd(csv_file, cl_column='CL_corrected', cd_column='CD_vlm', Plot = False, output_folder="Final_UAV_Sizing/Output/Wing_Sizing"):
    """
    Plots CD vs CL from a CSV file.

    Args:
        csv_file (str): Path to the CSV file.
        cl_column (str): Name of the column for CL. Default is 'CL_corrected'.
        cd_column (str): Name of the column for CD. Default is 'CD_vlm'.
    """
    data = pd.read_csv(csv_file)
    plt.figure(figsize=(8, 6))
    plt.plot(data[cd_column], data[cl_column], marker='o', linestyle='-')
    plt.xlabel('Drag Coefficient (CD)')
    plt.ylabel('Lift Coefficient (CL) - Corrected with Re Effects')
    plt.legend()
    plt.title('CL vs CD')
    plt.grid(True)
    plt.savefig(os.path.join(output_folder, "CL_vs_CD.png"))
    if Plot == True:
        plt.show()
    plt.close()

csv_path = r'Final_UAV_Sizing/Output/Final_Runs/Seventh_Final_Run_on_06-17_19-24/RS_2/Wing_Sizing/aero_specific_06-17.csv'
output_folder = r'Final_UAV_Sizing/Output/Final_Runs/Seventh_Final_Run_on_06-17_19-24/RS_2/Wing_Sizing'

plot_cl_vs_cd(
    csv_file=csv_path,
    cl_column='CL_corrected',
    cd_column='CD_vlm',
    Plot=False,
    output_folder=output_folder
)