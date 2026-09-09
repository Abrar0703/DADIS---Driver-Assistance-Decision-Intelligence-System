class CollisionProbability:

    @staticmethod
    def calculate(vehicle):

        if vehicle.ttc is None:
            return 0.0

        score = 0.0

        # ---------------- TTC ----------------
        if vehicle.ttc < 2:
            score += 0.45
        elif vehicle.ttc < 4:
            score += 0.30
        elif vehicle.ttc < 6:
            score += 0.15

        # ---------------- Distance ----------------
        if vehicle.distance < 10:
            score += 0.30
        elif vehicle.distance < 20:
            score += 0.20
        elif vehicle.distance < 30:
            score += 0.10

        # ---------------- Motion ----------------
        if vehicle.motion == "CLOSING FAST":
            score += 0.20
        elif vehicle.motion == "CLOSING":
            score += 0.10

        # ---------------- Lane ----------------
        if vehicle.lane == "CENTER":
            score += 0.05

        return round(min(score, 1.0), 2)