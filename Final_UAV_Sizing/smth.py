import matplotlib.pyplot as plt
import os
def plot_results(M_dict):
    relay_station_counts = list(M_dict.keys())
    n_relays = len(relay_station_counts)
    fig, axs = plt.subplots(1, n_relays, figsize=(5 * n_relays, 5), sharey=True)

    # If only one relay station, axs is not a list
    if n_relays == 1:
        axs = [axs]

    for idx, number_relay_stations in enumerate(relay_station_counts):
        axs[idx].plot(M_dict[number_relay_stations][1:], marker='o')
        axs[idx].set_title(f"{round(7/(number_relay_stations+1), 2)}h Endurance")
        axs[idx].set_xlabel("Iteration")
        axs[idx].set_ylabel("Mass (kg)")
        axs[idx].grid(True)

    plt.tight_layout()
    output_dir = 'Final_UAV_Sizing'
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "mass_through_iterations.png"))
    plt.show()
    plt.close()
plot_results({1: [16.767, 18.63, 26.79346365456272, 29.876722035749868, 32.66162590330749, 35.258784603290025, 37.97664478515107, 41.32241761860031], 2: [16.767, 18.63, 22.206744731335917, 22.298856177786856, 24.60589624047422, 23.84089936818679, 23.426767138951845], 3: [16.767, 18.63, 19.91184967540707, 20.54583964356725, 20.589764788924313], 4: [16.767, 18.63, 18.843805380171514, 18.810569457409382, 18.606073087883402], 5: [16.767, 18.63, 17.940858941709195, 17.21841919981386, 16.745885264334753]})
