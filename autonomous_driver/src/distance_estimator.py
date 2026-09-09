class DistanceEstimator:

    # Approximate real-world object heights (meters)
    REAL_HEIGHTS = {

        "car": 1.50,

        "truck": 3.50,

        "bus": 3.20,

        "motor": 1.40,

        "bike": 1.40,

        "person": 1.70,

        "rider": 1.70,

        "train": 4.20,

        "traffic light": 3.00,

        "traffic sign": 2.20

    }

    # Camera focal length (needs calibration later)
    FOCAL_LENGTH = 1000

    @staticmethod
    def estimate(vehicle):

        x1, y1, x2, y2 = vehicle.box

        pixel_height = y2 - y1

        if pixel_height <= 0:
            return None

        cls = vehicle.cls.lower()

        real_height = DistanceEstimator.REAL_HEIGHTS.get(cls)

        # Unknown class
        if real_height is None:
            return None

        distance = (

            real_height *

            DistanceEstimator.FOCAL_LENGTH

        ) / pixel_height

        return round(distance, 1)