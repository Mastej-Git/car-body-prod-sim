import time

from PyQt5.QtCore import QThread, pyqtSignal, QMutex

from Body import Body

from BodyPetriNet import body_main_petri_net

from other.MatPlotlibWidget import MatplotlibWidget

mutex = QMutex()

class PetriNetThread(QThread):

    finished_signal = pyqtSignal(int)

    def __init__(self, body: Body, mpl_widget: MatplotlibWidget):
        super().__init__()
        self._running = True
        # self.finished_signal.connect(self.stop)
        self.petri_net = body_main_petri_net
        self.body = body
        self.available_transitions = []
        self.executed_transitions = []
        self.mpl_widget = mpl_widget

        self.available_transitions.append("T2")

        if self.body.upper_panel.is_controlable == "Tak":
            if self.body.upper_panel.type == "4-strefowa":
                self.available_transitions.extend(["T3", "T4", "T5"])
            elif self.body.upper_panel.type == "2-strefowa":
                self.available_transitions.extend(["T3", "T9", "T10"])
        elif self.body.upper_panel.is_controlable == "Nie":
            self.available_transitions.extend(["T11", "T12"])

        if self.body.middle_panel.functionality == "Interfejs multimedialny":
            self.available_transitions.extend(["T13", "T14"])
        elif self.body.middle_panel.functionality == "Schowek":
            self.available_transitions.extend(["T15", "T16"])

        if self.body.lower_panel.functionality == "Ładowarka bezprzewodowa":
            self.available_transitions.extend(["T17", "T18"])
        elif self.body.lower_panel.functionality == "Półka":
            self.available_transitions.extend(["T23", "T24"])
        if self.body.lower_panel.is_cup == "Tak":
            self.available_transitions.extend(["T19", "T20"])
        elif self.body.lower_panel.is_cup == "Nie":
            self.available_transitions.extend(["T25", "T26"])
        if self.body.lower_panel.color == "Czerwony":
            self.available_transitions.extend(["T21", "T22"])
        elif self.body.lower_panel.color == "Zielony":
            self.available_transitions.extend(["T27", "T28"])
        elif self.body.lower_panel.color == "Niebieski":
            self.available_transitions.extend(["T29", "T30"])

        self.available_transitions.extend(["T6", "T7", "T8"])  

        self.petri_net.fire_transition("T1")

        print(self.available_transitions)

    def run(self):
        i = 0

        while self._running:
            mutex.lock()
            try:
                if self.petri_net.transitions[self.available_transitions[i]].is_enabled():
                    print(
                        f"\nThread id: {self.body.id} - Odpalam Tranzycje {self.available_transitions[i]}"
                    )
                    # print(self.petri_net)
                    self.petri_net.fire_transition(self.available_transitions[i])
                    self.executed_transitions.append(self.available_transitions[i])
                    self.mpl_widget.plot()
                    i += 1

                if self.executed_transitions == self.available_transitions:
                    break
            finally:
                mutex.unlock()

            time.sleep(2)

        self.finished_signal.emit(self.body.id)

    def stop(self):
        self._running = False
