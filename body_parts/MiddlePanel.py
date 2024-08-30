class MiddlePanel():

    def __init__(self, functionality) -> None:
        self.is_activated = False
        self.functionality = functionality

    def check_activation(self):
        if self.functionality != "":
            self.is_activated = True

    def remove_parameters(self):
        self.functionality = ""
        self.is_activated = False