from body_parts.UpperPanel import UpperPanel
from body_parts.MiddlePanel import MiddlePanel
from body_parts.LowerPanel import LowerPanel
from body_parts.Armrest import Armrest
from body_parts.CupHolder import CupHolder

class Body():

    def __init__(self, id,
                upper_panel: UpperPanel,
                middle_panel: MiddlePanel, 
                lower_panel: LowerPanel,
                armrest: Armrest,
                cup_holder: CupHolder):
        
        self.id = id

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

    def check_parts_activation(self):
        self.upper_panel.check_activation()
        self.middle_panel.check_activation()
        self.lower_panel.check_activation()
        self.armrest.check_activation()
        self.cup_holder.check_activation()

    def __str__(self) -> str:
        self.check_parts_activation()

        label = f"ID:{self.id}: Korpus zawiera następujące elementy:\n"

        if self.upper_panel.is_activated is True:
            label += f"▸  Panel gorny:\n\t ▪ Sterowanie klimatyzacja: {self.upper_panel.is_controlable}\n\t ▪ Typ: {self.upper_panel.type}\n"
        if self.middle_panel.is_activated is True:
            label += f"▸  Panel środkowy:\n\t ▪ Funkcjonalność: {self.middle_panel.functionality}\n"
        if self.lower_panel.is_activated is True:
            label += (f"▸  Panel dolny:\n\t ▪ Funkcjonalność: {self.lower_panel.functionality}\n\t "
                      f"▪ Chwytaki na kubki: {self.lower_panel.is_cup}\n\t" 
                      f" ▪ Kolor: {self.lower_panel.color}\n")
        if self.armrest.is_activated is True:
            label += (f"▸  Podłokietnik:\n\t ▪ Podgrzewanie: {self.armrest.heating}\n\t "
                      f"▪ Materiał: {self.armrest.material}\n\t" 
                      f" ▪ Kolor: {self.armrest.color}\n")
        if self.cup_holder.is_activated is True:
            label += f"▸  Miejsce na kubki:\n\t ▪ Wejście USB: {self.cup_holder.usb_socket}\n\t ▪ Kolor: {self.cup_holder.color}\n"

        return label