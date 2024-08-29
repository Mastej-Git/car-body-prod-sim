class UpperPanel():

    def __init__(self, is_controlable, type) -> None:
        self.is_activated = False
        self.is_controlable = is_controlable
        self.type = type

    def check_activation(self):
        if self.is_controlable != "" and self.type != "":
            self.is_activated = True

    def remove_parameters(self):
        self.is_controlable = ""
        self.type = ""
        self.is_activated = False