import time
from PyQt5.QtCore import QObject, pyqtSignal, QMutex
from BodyPetriNet import body_main_petri_net

mutex = QMutex()

class Worker(QObject):
    finished_signal = pyqtSignal(int, float)
    add_text_signal = pyqtSignal(str)

    def __init__(self, available_tr):
        super().__init__()
        self._running = True

        self.started_bodys = 0
        self.bodys_in_production = 0
        self.executed_bodys = 0
        self.available_tr = available_tr

        self.list_of_times = []

    def stop(self):
        self._running = False

    def run(self):

        pn = body_main_petri_net
        tr_to_exec = []
        while self._running:

            if "T002" in self.available_tr:
                self.started_bodys += 1
                self.bodys_in_production += 1
                print("Odpalam Tranzycje T001")
                pn.fire_transition("T001")

                start_time = time.time()
                self.list_of_times.append(start_time)

                time.sleep(0.5)

            for transition in self.available_tr:
                if pn.transitions[transition].is_enabled():
                    tr_to_exec.append(transition)

            if len(tr_to_exec) != 0:
                tmp = tr_to_exec
                tr_to_exec = self.remove_duplicates(tmp)

            for transition in tr_to_exec:
                # self.add_text_signal.emit(f"\nProcessing transition {transition} for body {body.body_id}")
                if pn.transitions[transition].is_enabled():
                    print(f"Odpalam Tranzycje {transition}")
                    pn.fire_transition(transition)
                    self.available_tr.remove(transition)
                    if transition == "T002":
                        self.started_bodys -= 1

                    if transition == "T905":
                        self.executed_bodys += 1
                        duration = time.time() - self.list_of_times[self.executed_bodys - 1]
                        print(f"Korpus o indeksie: {self.executed_bodys - 1} został wykonany w czasie: {duration}")

            if not tr_to_exec:
                time.sleep(0.5)

            tr_to_exec.clear()

    def remove_duplicates(self, lst):
        seen = set()
        result = []
        for item in lst:
            if item not in seen:
                result.append(item)
                seen.add(item)
        return result
