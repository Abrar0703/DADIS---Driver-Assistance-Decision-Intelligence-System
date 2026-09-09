class WorldModel:

    def __init__(self):
        self.vehicles = []

    def clear(self):
        self.vehicles = []

    def add_vehicle(
        self,
        vehicle_id,
        vehicle_class,
        box,
        confidence
    ):

        from vehicle import Vehicle

        self.vehicles.append(

            Vehicle(

                vehicle_id,

                vehicle_class,

                box,

                confidence

            )

        )

    def get_vehicles(self):
        return self.vehicles