class MotionState:

    @staticmethod
    def classify(vehicle):

        if vehicle.relative_speed > 1.5:
            return "CLOSING FAST"

        elif vehicle.relative_speed > 0.5:
            return "CLOSING"

        elif vehicle.relative_speed < -0.5:
            return "MOVING AWAY"

        return "STABLE"