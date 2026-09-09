class DecisionEngine:

    @staticmethod
    def analyze(scene):

        front = scene["front_vehicle"]

        # ==================================================
        # No vehicle in our lane
        # ==================================================

        if front is None:

            return {

                "status": "CLEAR",

                "reason": "Lane Clear",

                "vehicle": None,

                "color": (0,255,0)

            }

        # ==================================================
        # Information about neighbouring lanes
        # ==================================================

        left_vehicle = scene["nearest_left"]
        right_vehicle = scene["nearest_right"]

        left_clear = scene["left_lane_clear"]
        right_clear = scene["right_lane_clear"]

        left_distance = (
            left_vehicle.distance
            if left_vehicle is not None
            else 999
        )

        right_distance = (
            right_vehicle.distance
            if right_vehicle is not None
            else 999
        )

        # ==================================================
        # Emergency Brake
        # ==================================================

        if (
            front.collision_probability >= 0.90
            or
            (
                front.ttc is not None
                and front.ttc < 2
            )
        ):

            return {

                "status": "BRAKE",

                "reason": f"{front.cls} Ahead",

                "vehicle": front,

                "color": (0,0,255)

            }

        # ==================================================
        # High Threat
        # ==================================================

        if (
            front.collision_probability >= 0.60
            or
            front.motion == "CLOSING FAST"
        ):

            # -------------------------------
            # Both lanes are free
            # -------------------------------

            if left_clear and right_clear:

                if left_distance > right_distance:

                    return {

                        "status": "CHANGE LEFT",

                        "reason": "Left lane has more space",

                        "vehicle": front,

                        "color": (0,220,255)

                    }

                else:

                    return {

                        "status": "CHANGE RIGHT",

                        "reason": "Right lane has more space",

                        "vehicle": front,

                        "color": (0,220,255)

                    }

            # -------------------------------
            # Only left is free
            # -------------------------------

            elif left_clear:

                return {

                    "status": "CHANGE LEFT",

                    "reason": "Right lane occupied",

                    "vehicle": front,

                    "color": (0,220,255)

                }

            # -------------------------------
            # Only right is free
            # -------------------------------

            elif right_clear:

                return {

                    "status": "CHANGE RIGHT",

                    "reason": "Left lane occupied",

                    "vehicle": front,

                    "color": (0,220,255)

                }

            # -------------------------------
            # No lane available
            # -------------------------------

            else:

                return {

                    "status": "BRAKE",

                    "reason": "No Safe Lane",

                    "vehicle": front,

                    "color": (0,0,255)

                }

        # ==================================================
        # Moderate Threat
        # ==================================================

        if (
            front.collision_probability >= 0.35
            or
            front.motion == "CLOSING"
        ):

            return {

                "status": "CAUTION",

                "reason": f"{front.cls} Ahead",

                "vehicle": front,

                "color": (0,255,255)

            }

        # ==================================================
        # Safe Following
        # ==================================================

        return {

            "status": "CLEAR",

            "reason": "Safe Distance",

            "vehicle": front,

            "color": (0,255,0)

        }