class Drone:
    def __init__(self, drone_id, max_endurance_hrs, recharge_time_hrs):
        self.drone_id = drone_id
        self.max_endurance_hrs = max_endurance_hrs
        self.endurance_hrs = self.max_endurance_hrs
        self.recharge_time_hrs = recharge_time_hrs
        self.available_time = 0.0  # When the drone will be available next
        self.is_flying = False  # Whether the drone is currently flying

    def charge(self, time):
        """
        Charge the drone and set its available time.
        """
        self.is_flying = False
        self.available_time = time + self.recharge_time_hrs
        self.endurance_hrs = self.max_endurance_hrs  # Reset endurance after charging