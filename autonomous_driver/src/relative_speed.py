class RelativeSpeedEstimator:

    def __init__(self):
        self.previous_distances = {}

    def estimate(self, vehicle):

        vehicle_id = vehicle.cls

        current = vehicle.distance

        if current is None:
            return 0.0

        if vehicle_id not in self.previous_distances:

            self.previous_distances[vehicle_id] = current
            return 0.0

        previous = self.previous_distances[vehicle_id]

        speed = previous - current

        self.previous_distances[vehicle_id] = current

        return round(speed, 2)