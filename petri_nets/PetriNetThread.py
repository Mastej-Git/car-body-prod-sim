import time

from PyQt5.QtCore import QThread, pyqtSignal, QMutex

from Body import Body

from CupPetriNet import cup_main_petri_net

from other.MatPlotlibWidget import MatplotlibWidget
from other.Enums import CupMaterial

mutex = QMutex()

class PetriNetThread(QThread):

    finished_signal = pyqtSignal(int)

    def __init__(self, thread_id, body: Body, mpl_widget: MatplotlibWidget):
        super().__init__()
        self._running = True
        # self.finished_signal.connect(self.stop)
        self.petri_net = cup_main_petri_net
        self.body = body
        self.thread_id = thread_id
        self.available_transitions = []
        self.executed_transitions = []
        self.mpl_widget = mpl_widget

        if self.body.cup.material == CupMaterial.ALUMINUM:
            self.available_transitions = ["T2", "T3", "T6", "T9", "T12",
                                          "T15", "T18", "T21", "T24", "T27",
                                          "T28"]
        elif self.body.cup.material == CupMaterial.STAINLESS_STEEL:
            self.available_transitions = ["T2", "T4", "T7", "T10", "T13", 
                                          "T16", "T19", "T22", "T25", "T27", 
                                          "T28"]  

        self.petri_net.fire_transition("T1")

        print(self.thread_id)

    def run(self):
        i = 0

        while self._running:
            mutex.lock()
            try:
                if self.petri_net.transitions[self.available_transitions[i]].is_enabled():
                    print(f"\nThread id: {self.thread_id} - Firing Transition {self.available_transitions[i]}")
                    self.petri_net.fire_transition(self.available_transitions[i])
                    self.executed_transitions.append(self.available_transitions[i])
                    self.mpl_widget.plot()
                    i += 1

                if self.executed_transitions == self.available_transitions:
                    break
            finally:
                mutex.unlock()

            time.sleep(2)

        self.finished_signal.emit(self.thread_id)

    def stop(self):
        self._running = False