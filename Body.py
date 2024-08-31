from body_parts.UpperPanel import UpperPanel
from body_parts.MiddlePanel import MiddlePanel
from body_parts.LowerPanel import LowerPanel
from body_parts.Armrest import Armrest
from body_parts.CupHolder import CupHolder

class Body():

    def __init__(self,
                upper_panel: UpperPanel, 
                middle_panel:MiddlePanel, 
                lower_panel: LowerPanel,
                armrest: Armrest,
                cup_holder: CupHolder) -> None:
        
        self.upper_panel = upper_panel
        self.middle_panel = middle_panel
        self.lower_panel = lower_panel
        self.armrest = armrest
        self.cup_holder = cup_holder

    def remove_parameters(self):

        self.upper_panel.remove_parameters()
        self.middle_panel.remove_parameters()
        self.lower_panel.remove_parameters()
        self.armrest.remove_parameters()
        self.cup_holder.remove_parameters()