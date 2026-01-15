import time
from PyQt5.QtCore import QObject, pyqtSignal, QMutex
from petri_nets.BodyPetriNet import body_main_petri_net

mutex = QMutex()

class Worker(QObject):
    finished_signal = pyqtSignal()
    add_text_signal = pyqtSignal(str)

    def __init__(self, available_tr, info_terminal):
        super().__init__()
        self._running = True

        self.started_bodys = 0
        self.bodys_in_production = 0
        self.executed_bodys = 0
        self.available_tr = available_tr
        self.info_terminal = info_terminal

        self.list_of_times = []
        self.list_of_durations = []

    def stop(self):
        self._running = False

    def run(self) -> None:

        interator = 0
        iterator = 0

        pn = body_main_petri_net
        tr_to_exec = []
        while self._running:

            if "T002" in self.available_tr and iterator != 30:
                iterator += 1
                self.started_bodys += 1
                self.bodys_in_production += 1
                print(f"Rozpoczynam produkcję korpusu id: {self.started_bodys - 1}")
                self.add_text_signal.emit(f"Rozpoczynam produkcję korpusu id: {self.started_bodys - 1}")
                pn.fire_transition("T001")

                time.sleep(0.5)

            for transition in self.available_tr:
                if pn.transitions[transition].is_enabled():
                    tr_to_exec.append(transition)

            if len(tr_to_exec) != 0:
                tmp = tr_to_exec
                tr_to_exec = self.remove_duplicates(tmp)
                # tmp.reverse()
                tr_to_exec = self.get_lpt(tr_to_exec, pn)
                tr_to_exec.reverse()

            for transition in tr_to_exec:
                # self.add_text_signal.emit(f"\nProcessing transition {transition} for body {body.body_id}")
                if pn.transitions[transition].is_enabled() and pn.transitions[transition].can_fire():
                    pn.fire_transition(transition)
                    self.available_tr.remove(transition)
                    if transition == "T002":
                        self.bodys_in_production -= 1

                    if transition == "T004":
                        interator += 1
                        start_time = time.time()
                        self.list_of_times.append(start_time)

                    if transition == "T905":
                        self.executed_bodys += 1
                        duration = time.time() - self.list_of_times[self.executed_bodys - 1]
                        self.finished_signal.emit()
                        print(f"Korpus o indeksie: {self.executed_bodys - 1} został wykonany w czasie: {duration}")
                        self.list_of_durations.append(round(duration, 2))
                        self.add_text_signal.emit(f"Korpus o indeksie: {self.executed_bodys - 1} został wykonany w czasie: {duration}")


            if not tr_to_exec:
                time.sleep(0.5)

            if self.executed_bodys == 30:
                print(interator)
                print(self.list_of_durations)

            tr_to_exec.clear()

    def remove_duplicates(self, lst) -> list[str]:
        seen = set()
        result = []
        for item in lst:
            if item not in seen:
                result.append(item)
                seen.add(item)
        return result

    def get_lpt(self, lst, pn) -> list[str]:

        tmp = {}
        for transition in lst:
            sum = 0
            tr = pn.transitions[transition]
            for place in tr.outputs:
                sum += place.cooldown_ms
            tmp[transition] = sum

        sorted_tr = sorted(tmp.items(), key=lambda item: item[1])

        sorted_names = [name for name, _ in sorted_tr]
        return sorted_names
    