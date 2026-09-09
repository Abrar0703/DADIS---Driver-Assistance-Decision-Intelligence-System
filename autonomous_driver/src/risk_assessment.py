class RiskAssessment:

    DYNAMIC_CLASSES = {
        "car",
        "truck",
        "bus",
        "motor",
        "bike",
        "person",
        "rider",
        "train"
    }

    @staticmethod
    def calculate(vehicle):

        # ---------------------------------
        # Ignore Static Infrastructure
        # ---------------------------------
        if vehicle.cls.lower() not in RiskAssessment.DYNAMIC_CLASSES:
            return 0.0

        if vehicle.distance is None:
            return 0.0

        # ---------------------------------
        # Distance Score
        # ---------------------------------
        if vehicle.distance < 8:
            distance_score = 1.0

        elif vehicle.distance < 15:
            distance_score = 0.8

        elif vehicle.distance < 25:
            distance_score = 0.5

        else:
            distance_score = 0.2

        # ---------------------------------
        # Lane Score
        # ---------------------------------
        if vehicle.lane == "CENTER":
            lane_score = 1.0

        elif vehicle.lane in ["LEFT", "RIGHT"]:
            lane_score = 0.4

        else:
            lane_score = 0.1

        # ---------------------------------
        # Object Importance
        # ---------------------------------
        cls = vehicle.cls.lower()

        if cls == "truck":
            type_score = 1.0

        elif cls == "bus":
            type_score = 0.9

        elif cls == "train":
            type_score = 1.0

        elif cls in ["person", "rider"]:
            type_score = 0.9

        elif cls in ["motor", "bike"]:
            type_score = 0.8

        else:   # Car
            type_score = 0.7

        # ---------------------------------
        # TTC Score
        # ---------------------------------
        if vehicle.ttc is None:

            ttc_score = 0.2

        elif vehicle.ttc < 2:

            ttc_score = 1.0

        elif vehicle.ttc < 4:

            ttc_score = 0.8

        elif vehicle.ttc < 6:

            ttc_score = 0.5

        else:

            ttc_score = 0.2

        # ---------------------------------
        # Collision Probability
        # ---------------------------------
        collision_score = vehicle.collision_probability

        # ---------------------------------
        # Final Risk
        # ---------------------------------
        risk = (

            distance_score * 0.20 +

            lane_score * 0.15 +

            type_score * 0.10 +

            ttc_score * 0.20 +

            collision_score * 0.35

        )

        return round(min(risk, 1.0), 2)