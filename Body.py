from Cup import Cup
from AirConditioning import AirConditioning
from CarScreen import CarScreen

class Body():

    def __init__(self, cup: Cup, air_conditioning: AirConditioning, car_screen: CarScreen) -> None:
        self.cup = cup
        self.car_screen = car_screen
        self.air_conditioning = air_conditioning

    def set_cup(self, cup: Cup):
        self.cup = cup