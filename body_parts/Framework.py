class Framework():

    def __init__(self, material, color) -> None:
        self.is_activated = False
        self.material = material
        self.color = color

    def check_activation(self):
        if self.material != "" and self.color != "":
            self.is_activated = True

    def remove_parameters(self):
        self.material = ""
        self.color = ""
        self.is_activated = False
