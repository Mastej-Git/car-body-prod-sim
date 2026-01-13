class CupHolder():

    def __init__(self, usb_socket, color):
        self.is_activated = False
        self.usb_socket = usb_socket
        self.color = color

    def check_activation(self) -> None:
        if self.usb_socket != "" and self.color != "":
            self.is_activated = True

    def remove_parameters(self) -> None:
        self.usb_socket = ""
        self.color = ""
        self.is_activated = False
