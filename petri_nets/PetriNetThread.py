import time

from PyQt5.QtCore import QThread, pyqtSignal, QMutex

from Body import Body
from qt_classes.InfoTerminal import InfoTerminal

from BodyPetriNet import body_main_petri_net

mutex = QMutex()

class PetriNetThread(QThread):

    finished_signal = pyqtSignal(int, float)
    add_text_signal = pyqtSignal(str)

    def __init__(self, body: Body, info_terminal: InfoTerminal):
        super().__init__()
        self._running = True

        self.start_time = time.time()
        # self.finished_signal.connect(self.stop)
        self.petri_net = body_main_petri_net
        self.body = body
        self.info_terminal = info_terminal
        self.available_transitions = []

        self.available_body_parts_transitions = {
            "upper_panel": [],
            "middle_panel": [],
            "lower_panel": [],
            "armrest": [],
            "cup_holder": [],
            "framework": [], 
            "end": []}

        self.executed_transitions = []

        self.available_transitions.extend(["T002", "T003", "T004"])  

        self.define_available_tr()

        self.petri_net.fire_transition("T001")

        # for value in self.available_body_parts_transitions.values():
        #     self.available_transitions.extend(value)

        self.available_transitions.extend(["T901", "T902", "T903", "T904", "T905"])
        self.info_terminal.add_text_info(str(self.available_transitions))

        self.pn_up_thread = PetriNetSubThread(float(self.body.body_id) + 0.1, "Górny panel", self.available_body_parts_transitions["upper_panel"], self.info_terminal)
        self.pn_mp_thread = PetriNetSubThread(float(self.body.body_id) + 0.2, "Środkowy panel", self.available_body_parts_transitions["middle_panel"], self.info_terminal)
        self.pn_lp_thread = PetriNetSubThread(float(self.body.body_id) + 0.3, "Dolny panel", self.available_body_parts_transitions["lower_panel"], self.info_terminal)
        self.pn_ar_thread = PetriNetSubThread(float(self.body.body_id) + 0.4, "Podłokietnik", self.available_body_parts_transitions["armrest"], self.info_terminal)
        self.pn_ch_thread = PetriNetSubThread(float(self.body.body_id) + 0.5, "Uchwyt", self.available_body_parts_transitions["cup_holder"], self.info_terminal)
        self.pn_fw_thread = PetriNetSubThread(float(self.body.body_id) + 0.6, "Szkielet", self.available_body_parts_transitions["framework"], self.info_terminal)

        self.pn_up_thread.finished_signal.connect(self.on_thread_finished)
        self.pn_up_thread.add_sub_thread_text_signal.connect(self.add_sub_thread_text_emit)
        self.pn_mp_thread.finished_signal.connect(self.on_thread_finished)
        self.pn_mp_thread.add_sub_thread_text_signal.connect(self.add_sub_thread_text_emit)
        self.pn_lp_thread.finished_signal.connect(self.on_thread_finished)
        self.pn_lp_thread.add_sub_thread_text_signal.connect(self.add_sub_thread_text_emit)
        self.pn_ar_thread.finished_signal.connect(self.on_thread_finished)
        self.pn_ar_thread.add_sub_thread_text_signal.connect(self.add_sub_thread_text_emit)
        self.pn_ch_thread.finished_signal.connect(self.on_thread_finished)
        self.pn_ch_thread.add_sub_thread_text_signal.connect(self.add_sub_thread_text_emit)
        self.pn_fw_thread.finished_signal.connect(self.on_thread_finished)
        self.pn_fw_thread.add_sub_thread_text_signal.connect(self.add_sub_thread_text_emit)

        self.pn_up_thread.start()
        self.pn_mp_thread.start()
        self.pn_lp_thread.start()
        self.pn_ar_thread.start()
        self.pn_ch_thread.start()
        self.pn_fw_thread.start()

    def run(self):
        i = 0

        while self._running:
            mutex.lock()
            try:
                if self.petri_net.transitions[self.available_transitions[i]].is_enabled():
                    # self.add_text_signal.emit(f"\nThread thread_id: {self.body.body_id} - Odpalam Tranzycje {self.available_transitions[i]}")
                    self.petri_net.fire_transition(self.available_transitions[i])
                    self.executed_transitions.append(self.available_transitions[i])
                    i += 1

                if self.executed_transitions == self.available_transitions:
                    break
            finally:
                mutex.unlock()

            # time.sleep(0.3)

        end_time = time.time()
        duration = end_time - self.start_time
        self.finished_signal.emit(self.body.body_id, duration)

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

        self.info_terminal.add_text_info(f"Podwątek {thread_id} - {thread_name} został zakończony")

    def add_sub_thread_text_emit(self, text):
        self.add_text_signal.emit(text)

    def check_sub_thread_finish(self):
        if all(i is False for i  in [self.pn_up_thread, self.pn_mp_thread, self.pn_lp_thread, self.pn_ar_thread, self.pn_ch_thread, self.pn_fw_thread]):
            return True
        return False
        
    def define_available_tr(self):

        self.available_body_parts_transitions["upper_panel"].extend(["T101", "T102"])
        if self.body.upper_panel.ac_type == "2-strefowa":
            self.available_body_parts_transitions["upper_panel"].extend(["T103", "T105", "T107"])
        elif self.body.upper_panel.ac_type == "4-strefowa":
            self.available_body_parts_transitions["upper_panel"].extend(["T104", "T106", "T108"])
        if self.body.upper_panel.is_controlable == "Tak":
            self.available_body_parts_transitions["upper_panel"].extend(["T109", "T111", "T112"])
        elif self.body.upper_panel.is_controlable == "Nie":
            self.available_body_parts_transitions["upper_panel"].extend(["T110", "T113"])

        self.available_body_parts_transitions["middle_panel"].extend(["T201", "T202"])
        if self.body.middle_panel.functionality == "Interfejs multimedialny":
            self.available_body_parts_transitions["middle_panel"].extend(["T203", "T205", "T207"])
        elif self.body.middle_panel.functionality == "Schowek":
            self.available_body_parts_transitions["middle_panel"].extend(["T204", "T206", "T208"])

        self.available_body_parts_transitions["lower_panel"].extend(["T301", "T302"])
        if self.body.lower_panel.functionality == "Ładowarka bezprzewodowa":
            self.available_body_parts_transitions["lower_panel"].extend(["T303", "T305", "T307"])
        elif self.body.lower_panel.functionality == "Półka":
            self.available_body_parts_transitions["lower_panel"].extend(["T304", "T306", "T308"])
        if self.body.lower_panel.is_cup == "Tak":
            self.available_body_parts_transitions["lower_panel"].extend(["T309", "T311", "T312"])
        elif self.body.lower_panel.is_cup == "Nie":
            self.available_body_parts_transitions["lower_panel"].extend(["T310", "T313"])
        if self.body.lower_panel.color == "Czerwony":
            self.available_body_parts_transitions["lower_panel"].extend(["T314", "T317"])
        elif self.body.lower_panel.color == "Zielony":
            self.available_body_parts_transitions["lower_panel"].extend(["T315", "T318"])
        elif self.body.lower_panel.color == "Niebieski":
            self.available_body_parts_transitions["lower_panel"].extend(["T316", "T319"])
        self.available_body_parts_transitions["lower_panel"].extend(["T320"])


        self.available_body_parts_transitions["armrest"].extend(["T401", "T402"])
        if self.body.armrest.heating == "Tak":
            self.available_body_parts_transitions["armrest"].extend(["T403", "T405", "T406"])
        elif self.body.armrest.heating == "Nie":
            self.available_body_parts_transitions["armrest"].extend(["T404", "T407"])
        if self.body.armrest.material == "Skóra":
            self.available_body_parts_transitions["armrest"].extend(["T408", "T411"])
        elif self.body.armrest.material == "Eko skóra":
            self.available_body_parts_transitions["armrest"].extend(["T409", "T412"])
        elif self.body.armrest.material == "Sztuczna skóra":
            self.available_body_parts_transitions["armrest"].extend(["T410", "T413"])
        self.available_body_parts_transitions["armrest"].extend(["T414"])
        if self.body.armrest.color == "Czerwony":
            self.available_body_parts_transitions["armrest"].extend(["T415", "T418"])
        elif self.body.armrest.color == "Zielony":
            self.available_body_parts_transitions["armrest"].extend(["T416", "T419"])
        elif self.body.armrest.color == "Niebieski":
            self.available_body_parts_transitions["armrest"].extend(["T417", "T420"])
        self.available_body_parts_transitions["armrest"].extend(["T421"])


        self.available_body_parts_transitions["cup_holder"].extend(["T501", "T502", "T503", "T504", "T505"])
        if self.body.cup_holder.usb_socket == "Tak":
            self.available_body_parts_transitions["cup_holder"].extend(["T506", "T508", "T509"])
        elif self.body.cup_holder.usb_socket == "Nie":
            self.available_body_parts_transitions["cup_holder"].extend(["T507", "T510"])
        if self.body.cup_holder.color == "Czerwony":
            self.available_body_parts_transitions["cup_holder"].extend(["T511", "T514"])
        elif self.body.cup_holder.color == "Zielony":
            self.available_body_parts_transitions["cup_holder"].extend(["T512", "T515"])
        elif self.body.cup_holder.color == "Niebieski":
            self.available_body_parts_transitions["cup_holder"].extend(["T513", "T516"])
        self.available_body_parts_transitions["cup_holder"].extend(["T517"])

    
        self.available_body_parts_transitions["framework"].extend(["T601", "T602", "T603", "T604", "T605"])
        if self.body.framework.material == "Skóra":
            self.available_body_parts_transitions["framework"].extend(["T606", "T609"])
        elif self.body.framework.material == "Eko skóra":
            self.available_body_parts_transitions["framework"].extend(["T607", "T610"])
        elif self.body.framework.material == "Sztuczna skóra":
            self.available_body_parts_transitions["framework"].extend(["T608", "T611"])
        self.available_body_parts_transitions["framework"].extend(["T612"])
        if self.body.framework.color == "Czerwony":
            self.available_body_parts_transitions["framework"].extend(["T613", "T616"])
        elif self.body.framework.color == "Zielony":
            self.available_body_parts_transitions["framework"].extend(["T614", "T617"])
        elif self.body.framework.color == "Niebieski":
            self.available_body_parts_transitions["framework"].extend(["T615", "T618"])
        self.available_body_parts_transitions["framework"].extend(["T619"])


    def define_available_tr_1(self):
        # self.available_body_parts_transitions["upper_panel"].extend(["T101", "T102"])
        # self.available_body_parts_transitions["middle_panel"].extend(["T201", "T202"])
        # self.available_body_parts_transitions["lower_panel"].extend(["T301", "T302"])
        # self.available_body_parts_transitions["armrest"].extend(["T401", "T402"])
        # self.available_body_parts_transitions["cup_holder"].extend(["T501", "T502"])
        # self.available_body_parts_transitions["framework"].extend(["T601", "T602"])
        self.available_transitions.extend(["T101", "T102"])
        self.available_transitions.extend(["T201", "T202"])
        self.available_transitions.extend(["T301", "T302"])
        self.available_transitions.extend(["T401", "T402"])
        self.available_transitions.extend(["T501", "T502"])
        self.available_transitions.extend(["T601", "T602"])


        if self.body.upper_panel.ac_type == "2-strefowa":
            self.available_transitions.extend(["T103"])
        elif self.body.upper_panel.ac_type == "4-strefowa":
            self.available_transitions.extend(["T104"])


        if self.body.middle_panel.functionality == "Interfejs multimedialny":
            self.available_transitions.extend(["T203"])
        elif self.body.middle_panel.functionality == "Schowek":
            self.available_transitions.extend(["T204"])


        if self.body.lower_panel.functionality == "Ładowarka bezprzewodowa":
            self.available_transitions.extend(["T303"])
        elif self.body.lower_panel.functionality == "Półka":
            self.available_transitions.extend(["T304"])


        if self.body.armrest.heating == "Tak":
            self.available_transitions.extend(["T403"])
        elif self.body.armrest.heating == "Nie":
            self.available_transitions.extend(["T404", "T407"])

        self.available_transitions.extend(["T503", "T504"])

        self.available_transitions.extend(["T603", "T604"])

        if self.body.upper_panel.ac_type == "2-strefowa":
            self.available_transitions.extend(["T105", "T107"])
        elif self.body.upper_panel.ac_type == "4-strefowa":
            self.available_transitions.extend(["T106", "T108"])

        if self.body.middle_panel.functionality == "Interfejs multimedialny":
            self.available_transitions.extend(["T205", "T207"])
        elif self.body.middle_panel.functionality == "Schowek":
            self.available_transitions.extend(["T206", "T208"])

        if self.body.lower_panel.functionality == "Ładowarka bezprzewodowa":
            self.available_transitions.extend(["T305", "T307"])
        elif self.body.lower_panel.functionality == "Półka":
            self.available_transitions.extend(["T306", "T308"])

        if self.body.armrest.heating == "Tak":
            self.available_transitions.extend(["T405", "T406"])

        if self.body.cup_holder.usb_socket == "Tak":
            self.available_transitions.extend(["T505", "T506"])
        elif self.body.cup_holder.usb_socket == "Nie":
            self.available_transitions.extend(["T505", "T507", "T510"])
        
        if self.body.framework.material == "Skóra":
            self.available_transitions.extend(["T605", "T606"])
        elif self.body.framework.material == "Eko skóra":
            self.available_transitions.extend(["T605", "T607"])
        elif self.body.framework.material == "Sztuczna skóra":
            self.available_transitions.extend(["T605", "T608"])

        if self.body.upper_panel.is_controlable == "Tak":
            self.available_transitions.extend(["T109"])
        elif self.body.upper_panel.is_controlable == "Nie":
            self.available_transitions.extend(["T110", "T113"])

        if self.body.lower_panel.is_cup == "Tak":
            self.available_transitions.extend(["T309"])
        elif self.body.lower_panel.is_cup == "Nie":
            self.available_transitions.extend(["T310", "T313"])
    
        if self.body.armrest.material == "Skóra":
            self.available_transitions.extend(["T408"])
        elif self.body.armrest.material == "Eko skóra":
            self.available_transitions.extend(["T409"])
        elif self.body.armrest.material == "Sztuczna skóra":
            self.available_transitions.extend(["T410"])

        if self.body.cup_holder.usb_socket == "Tak":
            self.available_transitions.extend(["T508", "T509"])

        if self.body.framework.material == "Skóra":
            self.available_transitions.extend(["T609", "T612"])
        elif self.body.framework.material == "Eko skóra":
            self.available_transitions.extend(["T610", "T612"])
        elif self.body.framework.material == "Sztuczna skóra":
            self.available_transitions.extend(["T611", "T612"])

        if self.body.upper_panel.is_controlable == "Tak":
            self.available_transitions.extend(["T111", "T112"])

        if self.body.lower_panel.is_cup == "Tak":
            self.available_transitions.extend(["T311", "T312"])

        if self.body.armrest.material == "Skóra":
            self.available_transitions.extend(["T411", "T414"])
        elif self.body.armrest.material == "Eko skóra":
            self.available_transitions.extend(["T412", "T414"])
        elif self.body.armrest.material == "Sztuczna skóra":
            self.available_transitions.extend(["T413", "T414"])

        if self.body.cup_holder.color == "Czerwony":
            self.available_transitions.extend(["T511"])
        elif self.body.cup_holder.color == "Zielony":
            self.available_transitions.extend(["T512"])
        elif self.body.cup_holder.color == "Niebieski":
            self.available_transitions.extend(["T513"])

        if self.body.framework.color == "Czerwony":
            self.available_transitions.extend(["T613"])
        elif self.body.framework.color == "Zielony":
            self.available_transitions.extend(["T614"])
        elif self.body.framework.color == "Niebieski":
            self.available_transitions.extend(["T615"])

        if self.body.lower_panel.color == "Czerwony":
            self.available_transitions.extend(["T314"])
        elif self.body.lower_panel.color == "Zielony":
            self.available_transitions.extend(["T315"])
        elif self.body.lower_panel.color == "Niebieski":
            self.available_transitions.extend(["T316"])

        if self.body.armrest.color == "Czerwony":
            self.available_transitions.extend(["T415"])
        elif self.body.armrest.color == "Zielony":
            self.available_transitions.extend(["T416"])
        elif self.body.armrest.color == "Niebieski":
            self.available_transitions.extend(["T417"])

        if self.body.cup_holder.color == "Czerwony":
            self.available_transitions.extend(["T514", "T517"])
        elif self.body.cup_holder.color == "Zielony":
            self.available_transitions.extend(["T515", "T517"])
        elif self.body.cup_holder.color == "Niebieski":
            self.available_transitions.extend(["T516", "T517"])

        if self.body.framework.color == "Czerwony":
            self.available_transitions.extend(["T616", "T619"])
        elif self.body.framework.color == "Zielony":
            self.available_transitions.extend(["T617", "T619"])
        elif self.body.framework.color == "Niebieski":
            self.available_transitions.extend(["T618", "T619"])

        if self.body.lower_panel.color == "Czerwony":
            self.available_transitions.extend(["T317", "T320"])
        elif self.body.lower_panel.color == "Zielony":
            self.available_transitions.extend(["T318", "T320"])
        elif self.body.lower_panel.color == "Niebieski":
            self.available_transitions.extend(["T319", "T320"])

        self.available_transitions.extend(["T901"])

        if self.body.armrest.color == "Czerwony":
            self.available_transitions.extend(["T418", "T421"])
        elif self.body.armrest.color == "Zielony":
            self.available_transitions.extend(["T419", "T421"])
        elif self.body.armrest.color == "Niebieski":
            self.available_transitions.extend(["T420", "T421"])

        self.available_transitions.extend(["T902", "T903", "T904", "T905"])
      

class PetriNetSubThread(QThread):

    finished_signal = pyqtSignal(float, str)
    add_sub_thread_text_signal = pyqtSignal(str)

    def __init__(self, thread_id: float, name: str,available_transitions: list, info_terminal: InfoTerminal):
        super().__init__()
        self._running = True
        self.thread_id = thread_id
        self.name = name
        self.petri_net = body_main_petri_net
        self.available_transitions = available_transitions
        self.executed_transitions = []

        self.info_terminal = info_terminal

        self.info_terminal.add_text_info(str(self.available_transitions))

    def run(self):
        i = 0

        while self._running:
            mutex.lock()
            try:
                if self.petri_net.transitions[self.available_transitions[i]].is_enabled():
                    # self.add_sub_thread_text_signal.emit(f"\nSub-Thread thread_id: {self.thread_id}, part: {self.name} - Odpalam Tranzycje {self.available_transitions[i]}")
                    self.petri_net.fire_transition(self.available_transitions[i])
                    self.executed_transitions.append(self.available_transitions[i])
                    i += 1

                if self.executed_transitions == self.available_transitions:
                    break
            finally:
                mutex.unlock()

            time.sleep(0.5)

        self.finished_signal.emit(self.thread_id, self.name)
