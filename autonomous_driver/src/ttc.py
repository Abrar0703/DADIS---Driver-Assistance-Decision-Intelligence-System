class TimeToCollision:

    @staticmethod
    def calculate(vehicle):

        # No distance available
        if vehicle.distance is None:
            return None

        # Vehicle moving away or stationary
        if vehicle.relative_speed <= 0:
            return None

        ttc = vehicle.distance / vehicle.relative_speed

        return round(ttc, 2)