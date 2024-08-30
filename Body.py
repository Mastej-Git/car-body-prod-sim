from body_parts.Cup import Cup
from body_parts.AirConditioning import AirConditioning
from body_parts.CarScreen import CarScreen

from body_parts.UpperPanel import UpperPanel
from body_parts.MiddlePanel import MiddlePanel
from body_parts.LowerPanel import LowerPanel
from body_parts.Armrest import Armrest

class Body():

    def __init__(self, 
                cup: Cup,
                air_conditioning: AirConditioning,
                car_screen: CarScreen, 
                upper_panel: UpperPanel, 
                middle_panel:MiddlePanel, 
                lower_panel: LowerPanel,
                armrest: Armrest) -> None:
        
        self.cup = cup
        self.car_screen = car_screen
        self.air_conditioning = air_conditioning
        self.upper_panel = upper_panel
        self.middle_panel = middle_panel
        self.lower_panel = lower_panel
        self.armrest = armrest

    def set_cup(self, cup: Cup):
        self.cup = cup