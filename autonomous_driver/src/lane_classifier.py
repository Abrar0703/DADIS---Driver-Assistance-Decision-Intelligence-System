class LaneClassifier:

    @staticmethod
    def classify(vehicle,
                 left_boundary,
                 right_boundary):

        if len(left_boundary) == 0:
            return "UNKNOWN"

        x1, y1, x2, y2 = vehicle.box

        vehicle_x = (x1 + x2) // 2
        vehicle_y = y2

        left = min(
            left_boundary,
            key=lambda p: abs(p[1] - vehicle_y)
        )

        right = min(
            right_boundary,
            key=lambda p: abs(p[1] - vehicle_y)
        )

        left_x = left[0]
        right_x = right[0]

        if left_x <= vehicle_x <= right_x:
            return "CENTER"

        elif vehicle_x < left_x:
            return "LEFT"

        else:
            return "RIGHT"