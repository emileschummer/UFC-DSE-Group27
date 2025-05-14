from drone import Drone

def optimise_drones_for_race(race_duration_hours, drone_flight_time, drone_recharge_time):
    drones_needed = 1
    total_time = 0

    while total_time < race_duration_hours * 60:
        total_time += drone_flight_time
        if total_time < race_duration_hours * 60:
            total_time += drone_recharge_time
            drones_needed += 1

    return drones_needed


if __name__ == "__main__":
    race_duration = 7  # in hours
    drone = Drone()  # Assuming the Drone class has flight_time and recharge_time attributes
    flight_time = drone.flight_time  # in minutes
    recharge_time = drone.recharge_time  # in minutes

    drones_required = optimise_drones_for_race(race_duration, flight_time, recharge_time)
    print(f"Number of drones needed: {drones_required}")