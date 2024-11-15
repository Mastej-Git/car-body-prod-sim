from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class Place(QObject):
    tokens_changed = pyqtSignal()

    def __init__(self, name, description="", tokens=0, ready_tokens=0, max_tokens=1, cooldown_ms=1):
        super().__init__()
        self.name = name
        self.description = description
        self._tokens = tokens
        self.ready_tokens = ready_tokens
        self.cooldown_ms = cooldown_ms
        self.max_tokens = max_tokens

        self.info_terminal = None

        self.tokens_changed.connect(self.on_tokens_changed)

    @property
    def tokens(self):
        return self._tokens

    @tokens.setter
    def tokens(self, value):
        if value != self._tokens:
            self._tokens = value
            
            self.tokens_changed.emit()

    def on_tokens_changed(self):
        QTimer.singleShot(self.cooldown_ms, self.print_info)

    def set_terminal(self, terminal):
        self.info_terminal = terminal

    def print_info(self):
        self.ready_tokens += self._tokens
        self._tokens = 0

        # if self.info_terminal != None:
        #     self.info_terminal.add_text_info(f"Dla Miejsca: {self.name} znaczniki są gotowe")

    def __str__(self) -> str:
        return f"Place({self.name}, tokens={self._tokens}, ready_tokens={self.ready_tokens}, max_tokens={self.max_tokens}, cooldown_ms={self.cooldown_ms})"
    