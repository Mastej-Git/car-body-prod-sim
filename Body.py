from Cup import Cup
from AirConditioning import AirConditioning

class Body():

    def __init__(self, cup: Cup, air_conditioning: AirConditioning) -> None:
        self.cup = cup
        self.air_conditioning = air_conditioning 