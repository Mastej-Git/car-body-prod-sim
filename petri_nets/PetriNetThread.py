import time

from PyQt5.QtCore import QThread, pyqtSignal, QMutex

from Body import Body

from BodyPetriNet import body_main_petri_net

mutex = QMutex()

class PetriNetThread(QThread):

    finished_signal = pyqtSignal(int)

    def __init__(self, body: Body):
        super().__init__()
        self._running = True
        # self.finished_signal.connect(self.stop)
        self.petri_net = body_main_petri_net
        self.body = body
        self.available_transitions = []

        self.available_body_parts_transitions = {
            "upper_panel": [],
            "middle_panel": [],
            "lower_panel": [],
            "armrest": [],
            "cup_holder": [],
            "framework": []}

        self.executed_transitions = []

        self.define_available_tr()

        self.available_transitions.extend(["T002", "T003", "T004", "T901", "T902", "T903", "T904"])  

        self.petri_net.fire_transition("T001")
        # self.petri_net.fire_transition("T002")
        # self.petri_net.fire_transition("T003")
        # self.petri_net.fire_transition("T004")

        print(self.available_transitions)

        self.pn_up_thread = PetriNetSubThread(float(self.body.body_id) + 0.1, "Górny panel", self.available_body_parts_transitions["upper_panel"])
        self.pn_mp_thread = PetriNetSubThread(float(self.body.body_id) + 0.2, "Środkowy panel", self.available_body_parts_transitions["middle_panel"])
        self.pn_lp_thread = PetriNetSubThread(float(self.body.body_id) + 0.3, "Dolny panel", self.available_body_parts_transitions["lower_panel"])
        self.pn_ar_thread = PetriNetSubThread(float(self.body.body_id) + 0.4, "Podłokietnik", self.available_body_parts_transitions["armrest"])
        self.pn_ch_thread = PetriNetSubThread(float(self.body.body_id) + 0.5, "Uchwyt", self.available_body_parts_transitions["cup_holder"])
        self.pn_fw_thread = PetriNetSubThread(float(self.body.body_id) + 0.6, "Szkielet", self.available_body_parts_transitions["framework"])
        self.pn_mp_thread.finished_signal.connect(self.on_thread_finished)
        self.pn_up_thread.finished_signal.connect(self.on_thread_finished)
        self.pn_lp_thread.finished_signal.connect(self.on_thread_finished)
        self.pn_ar_thread.finished_signal.connect(self.on_thread_finished)
        self.pn_ch_thread.finished_signal.connect(self.on_thread_finished)
        self.pn_fw_thread.finished_signal.connect(self.on_thread_finished)
        self.pn_mp_thread.start()
        self.pn_up_thread.start()
        self.pn_lp_thread.start()
        self.pn_ar_thread.start()
        self.pn_ch_thread.start()
        self.pn_fw_thread.start()

    def run(self):
        i = 0

        while self._running:
            # print(self.available_transitions)
            # if self.check_sub_thread_finish():
            mutex.lock()
            try:
                if self.petri_net.transitions[self.available_transitions[i]].is_enabled():
                    print(
                        f"\nThread thread_id: {self.body.body_id} - Odpalam Tranzycje {self.available_transitions[i]}"
                    )
                    self.petri_net.fire_transition(self.available_transitions[i])
                    self.executed_transitions.append(self.available_transitions[i])
                    i += 1

                if self.executed_transitions == self.available_transitions:
                    break
            finally:
                mutex.unlock()

            time.sleep(0.5)

        self.finished_signal.emit(self.body.body_id)

    def stop(self):
        self._running = False

    def thread_finder(self, thread_id):
        if round(thread_id - int(thread_id), 10) == 0.1:
            return self.pn_up_thread
        if round(thread_id - int(thread_id), 10) == 0.2:
            return self.pn_mp_thread
        if round(thread_id - int(thread_id), 10) == 0.3:
            return self.pn_lp_thread
        if round(thread_id - int(thread_id), 10) == 0.4:
            return self.pn_ar_thread
        if round(thread_id - int(thread_id), 10) == 0.5:
            return self.pn_ch_thread
        if round(thread_id - int(thread_id), 10) == 0.6:
            return self.pn_fw_thread
        return None

    def on_thread_finished(self, thread_id, thread_name):
        thread = self.thread_finder(thread_id)
        thread._running = False
        print(f"Sub-Thread {thread_id} - {thread_name} has finished.")

    def check_sub_thread_finish(self):
        if (self.pn_up_thread._running is False and 
            self.pn_mp_thread._running is False and 
            self.pn_lp_thread._running is False and 
            self.pn_ar_thread._running is False and
            self.pn_ch_thread._running is False and
            self.pn_fw_thread._running is False):
            return True
        return False
        
    def define_available_tr(self):

        if self.body.upper_panel.is_controlable == "Tak":
            if self.body.upper_panel.ac_type == "4-strefowa":
                self.available_body_parts_transitions["upper_panel"].extend(["T101", "T102", "T103"])
            elif self.body.upper_panel.ac_type == "2-strefowa":
                self.available_body_parts_transitions["upper_panel"].extend(["T101", "T104", "T105"])
        elif self.body.upper_panel.is_controlable == "Nie":
            self.available_body_parts_transitions["upper_panel"].extend(["T106", "T107"])

        if self.body.middle_panel.functionality == "Interfejs multimedialny":
            self.available_body_parts_transitions["middle_panel"].extend(["T201", "T202"])
        elif self.body.middle_panel.functionality == "Schowek":
            self.available_body_parts_transitions["middle_panel"].extend(["T203", "T204"])

        if self.body.lower_panel.functionality == "Ładowarka bezprzewodowa":
            self.available_body_parts_transitions["lower_panel"].extend(["T301", "T302"])
        elif self.body.lower_panel.functionality == "Półka":
            self.available_body_parts_transitions["lower_panel"].extend(["T303", "T304"])
        if self.body.lower_panel.is_cup == "Tak":
            self.available_body_parts_transitions["lower_panel"].extend(["T305", "T306"])
        elif self.body.lower_panel.is_cup == "Nie":
            self.available_body_parts_transitions["lower_panel"].extend(["T307", "T308"])
        if self.body.lower_panel.color == "Czerwony":
            self.available_body_parts_transitions["lower_panel"].extend(["T309", "T310"])
        elif self.body.lower_panel.color == "Zielony":
            self.available_body_parts_transitions["lower_panel"].extend(["T311", "T312"])
        elif self.body.lower_panel.color == "Niebieski":
            self.available_body_parts_transitions["lower_panel"].extend(["T313", "T314"])

        if self.body.armrest.material == "Skóra":
            self.available_body_parts_transitions["armrest"].extend(["T401", "T402"])
        elif self.body.armrest.material == "Eko skóra":
            self.available_body_parts_transitions["armrest"].extend(["T403", "T404"])
        elif self.body.armrest.material == "Sztuczna skóra":
            self.available_body_parts_transitions["armrest"].extend(["T405", "T406"])
        if self.body.armrest.heating == "Tak":
            self.available_body_parts_transitions["armrest"].extend(["T407", "T408"])
        elif self.body.armrest.heating == "Nie":
            self.available_body_parts_transitions["armrest"].extend(["T409", "T410"])
        if self.body.armrest.color == "Czerwony":
            self.available_body_parts_transitions["armrest"].extend(["T411", "T412"])
        elif self.body.armrest.color == "Zielony":
            self.available_body_parts_transitions["armrest"].extend(["T413", "T414"])
        elif self.body.armrest.color == "Niebieski":
            self.available_body_parts_transitions["armrest"].extend(["T415", "T416"])

        self.available_body_parts_transitions["cup_holder"].extend(["T501", "T502"])
        if self.body.cup_holder.usb_socket == "Tak":
            self.available_body_parts_transitions["cup_holder"].extend(["T503", "T504"])
        elif self.body.cup_holder.usb_socket == "Nie":
            self.available_body_parts_transitions["cup_holder"].extend(["T505", "T506"])
        if self.body.cup_holder.color == "Czerwony":
            self.available_body_parts_transitions["cup_holder"].extend(["T507", "T508"])
        elif self.body.cup_holder.color == "Zielony":
            self.available_body_parts_transitions["cup_holder"].extend(["T509", "T510"])
        elif self.body.cup_holder.color == "Niebieski":
            self.available_body_parts_transitions["cup_holder"].extend(["T511", "T512"])

        self.available_body_parts_transitions["framework"].extend(["T601", "T602"])
        if self.body.framework.material == "Skóra":
            self.available_body_parts_transitions["framework"].extend(["T603", "T604"])
        elif self.body.framework.material == "Eko skóra":
            self.available_body_parts_transitions["framework"].extend(["T605", "T606"])
        elif self.body.framework.material == "Sztuczna skóra":
            self.available_body_parts_transitions["framework"].extend(["T607", "T608"])
        if self.body.framework.color == "Czerwony":
            self.available_body_parts_transitions["framework"].extend(["T609", "T610"])
        elif self.body.framework.color == "Zielony":
            self.available_body_parts_transitions["framework"].extend(["T611", "T612"])
        elif self.body.framework.color == "Niebieski":
            self.available_body_parts_transitions["framework"].extend(["T613", "T614"])

class PetriNetSubThread(QThread):

    finished_signal = pyqtSignal(float, str)

    def __init__(self, thread_id: float, name: str,available_transitions: list):
        super().__init__()
        self._running = True
        # self.finished_signal.connect(self.stop)
        self.thread_id = thread_id
        self.name = name
        self.petri_net = body_main_petri_net
        self.available_transitions = available_transitions
        self.executed_transitions = []

        print(self.available_transitions)

    def run(self):
        i = 0

        while self._running:
            mutex.lock()
            try:
                if self.petri_net.transitions[self.available_transitions[i]].is_enabled():
                    print(
                        f"\nSub-Thread thread_id: {self.thread_id}, part: {self.name} - Odpalam Tranzycje {self.available_transitions[i]}"
                    )
                    self.petri_net.fire_transition(self.available_transitions[i])
                    self.executed_transitions.append(self.available_transitions[i])
                    i += 1

                if self.executed_transitions == self.available_transitions:
                    break
            finally:
                mutex.unlock()

            time.sleep(0.5)

        self.finished_signal.emit(self.thread_id, self.name)
