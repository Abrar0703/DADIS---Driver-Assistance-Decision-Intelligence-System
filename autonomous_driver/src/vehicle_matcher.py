import math


class VehicleMatcher:

    def __init__(self):
        self.previous = []

    def match(self, vehicles):

        matches = {}

        for current in vehicles:

            cx = (current.box[0] + current.box[2]) / 2
            cy = (current.box[1] + current.box[3]) / 2

            best = None
            best_distance = float("inf")

            for previous in self.previous:

                px = (previous.box[0] + previous.box[2]) / 2
                py = (previous.box[1] + previous.box[3]) / 2

                d = math.hypot(cx - px, cy - py)

                if d < best_distance:
                    best_distance = d
                    best = previous

            matches[current] = best

        self.previous = vehicles.copy()

        return matches