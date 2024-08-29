class LowerPanel():

    def __init__(self, functionality, is_cup, color) -> None:
        self.is_activated = False
        self.functionality = functionality
        self.is_cup = is_cup
        self.color = color

    def check_activation(self):
        if self.functionality != "" and self.is_cup != "" and self.color != "":
            self.is_activated = True

    def remove_parameters(self):
        self.functionality = ""
        self.is_cup = ""
        self.color = ""
        self.is_activated = False