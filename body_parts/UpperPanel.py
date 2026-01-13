class UpperPanel():

    def __init__(self, is_controlable, ac_type):
        self.is_activated = False
        self.is_controlable = is_controlable
        self.ac_type = ac_type

    def check_activation(self) -> None:
        if self.is_controlable != "" and self.ac_type != "":
            self.is_activated = True

    def remove_parameters(self) -> None:
        self.is_controlable = ""
        self.ac_type = ""
        self.is_activated = False
