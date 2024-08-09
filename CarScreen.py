class CarScreen():

    def __init__(self, type, size) -> None:
        self.is_activated = False
        self.type = type
        self.size = size

    def check_activation(self):
        if self.type != "" and self.size != "":
            self.is_activated = True