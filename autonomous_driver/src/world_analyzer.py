class WorldAnalyzer:

    VEHICLE_CLASSES = {
        "car",
        "truck",
        "bus",
        "motor",
        "bike",
        "train",
        "rider",
        "person"
    }

    @staticmethod
    def analyze(vehicles):

        front_vehicle = None

        nearest_left = None
        nearest_right = None

        left_lane_clear = True
        right_lane_clear = True

        dynamic_objects = []

        # -----------------------------------
        # Analyze Dynamic Road Users
        # -----------------------------------
        for vehicle in vehicles:

            if vehicle.cls.lower() not in WorldAnalyzer.VEHICLE_CLASSES:
                continue

            dynamic_objects.append(vehicle)

            if vehicle.distance is None:
                continue

            # ---------------- Front Lane ----------------
            if vehicle.lane == "CENTER":

                if (
                    front_vehicle is None or
                    vehicle.distance < front_vehicle.distance
                ):
                    front_vehicle = vehicle

            # ---------------- Left Lane ----------------
            elif vehicle.lane == "LEFT":

                if (
                    nearest_left is None or
                    vehicle.distance < nearest_left.distance
                ):
                    nearest_left = vehicle

            # ---------------- Right Lane ----------------
            elif vehicle.lane == "RIGHT":

                if (
                    nearest_right is None or
                    vehicle.distance < nearest_right.distance
                ):
                    nearest_right = vehicle

        # -----------------------------------
        # Lane Occupancy
        # -----------------------------------
        if nearest_left and nearest_left.distance < 20:
            left_lane_clear = False

        if nearest_right and nearest_right.distance < 20:
            right_lane_clear = False

        # -----------------------------------
        # Threat Ranking
        # -----------------------------------
        threats = sorted(
            dynamic_objects,
            key=lambda v: v.risk,
            reverse=True
        )

        highest = threats[0] if threats else None

        # -----------------------------------
        # Scene Summary
        # -----------------------------------
        return {

            "front_vehicle": front_vehicle,

            "front_distance":
                front_vehicle.distance if front_vehicle else None,

            "nearest_left": nearest_left,

            "nearest_right": nearest_right,

            "left_lane_clear": left_lane_clear,

            "right_lane_clear": right_lane_clear,

            "dynamic_objects": dynamic_objects

        }