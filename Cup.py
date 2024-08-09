class Cup():

    def __init__(self, material, size) -> None:
        self.is_activated = False
        self.material = material
        self.size = size

    def check_activation(self):
        if self.material != "" and self.size != "":
            self.is_activated = True