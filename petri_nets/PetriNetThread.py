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

        for value in self.available_body_parts_transitions.values():
            self.available_transitions.extend(value)

        self.available_transitions.extend(["T901", "T902", "T903", "T904", "T905"])
        self.info_terminal.add_text_info(str(self.available_transitions))

    def run(self):

        tr_to_exec = []
        while self._running:
            for transition in self.available_transitions:
                if self.petri_net.transitions[transition].is_enabled():
                    tr_to_exec.append(transition)

            print(tr_to_exec)
            for transition in tr_to_exec:
                # self.add_text_signal.emit(f"\nThread thread_id: {self.body.body_id} - Odpalam Tranzycje {transition}")
                print(f"\nThread thread_id: {self.body.body_id} - Odpalam Tranzycje {transition}")
                self.petri_net.fire_transition(transition)
                self.executed_transitions.append(transition)

            if tr_to_exec == []:
                time.sleep(0.5)

            if len(self.executed_transitions) == len(self.available_transitions):
                break

            tr_to_exec.clear()

        end_time = time.time()
        duration = end_time - self.start_time
        self.finished_signal.emit(self.body.body_id, duration)

    # def run(self):
    #     i = 0

    #     while self._running:
    #         mutex.lock()
    #         try:
    #             if self.petri_net.transitions[self.available_transitions[i]].is_enabled():
    #                 # self.add_text_signal.emit(f"\nThread thread_id: {self.body.body_id} - Odpalam Tranzycje {self.available_transitions[i]}")
    #                 self.petri_net.fire_transition(self.available_transitions[i])
    #                 self.executed_transitions.append(self.available_transitions[i])
    #                 i += 1

    #             if self.executed_transitions == self.available_transitions:
    #                 break
    #         finally:
    #             mutex.unlock()

    #         # time.sleep(0.3)

    #     end_time = time.time()
    #     duration = end_time - self.start_time
    #     self.finished_signal.emit(self.body.body_id, duration)

    def stop(self):
        self._running = False

    def add_sub_thread_text_emit(self, text):
        self.add_text_signal.emit(text)
        
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
