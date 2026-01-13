class MiddlePanel():

    def __init__(self, functionality):
        self.is_activated = False
        self.functionality = functionality

    def check_activation(self) -> None:
        if self.functionality != "":
            self.is_activated = True

    def remove_parameters(self) -> None:
        self.functionality = ""
        self.is_activated = False
