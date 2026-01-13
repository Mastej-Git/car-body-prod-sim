class Armrest():

    def __init__(self, heating, material, color):
        self.is_activated = False
        self.heating = heating
        self.material = material
        self.color = color

    def check_activation(self) -> None:
        if self.heating != "" and self.material != "" and self.color != "":
            self.is_activated = True

    def remove_parameters(self) -> None:
        self.heating = ""
        self.material = ""
        self.color = ""
        self.is_activated = False
