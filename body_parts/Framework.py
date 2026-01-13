class Framework():

    def __init__(self, material, color):
        self.is_activated = False
        self.material = material
        self.color = color

    def check_activation(self) -> None:
        if self.material != "" and self.color != "":
            self.is_activated = True

    def remove_parameters(self) -> None:
        self.material = ""
        self.color = ""
        self.is_activated = False
