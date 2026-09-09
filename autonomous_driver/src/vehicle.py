class Vehicle:

    def __init__(self,
                 vehicle_id,
                 vehicle_class,
                 box,
                 confidence):

        self.id = vehicle_id

        self.cls = vehicle_class

        self.box = box

        self.confidence = confidence

        self.distance = None

        self.lane = None

        self.risk = 0.0

        self.speed = None

        self.relative_speed = 0.0

        self.ttc = None

        self.motion = "UNKNOWN"

        self.collision_probability = 0.0