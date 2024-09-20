class Armrest():

    def __init__(self, heating, material, color) -> None:
        self.is_activated = False
        self.heating = heating
        self.material = material
        self.color = color

    def check_activation(self):
        if self.heating != "" and self.material != "" and self.color != "":
            self.is_activated = True

    def remove_parameters(self):
        self.heating = ""
        self.material = ""
        self.color = ""
        self.is_activated = False
