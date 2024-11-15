import time
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from queue import Queue

from BodyPetriNet import body_main_petri_net
from Body import Body

class Listener(QObject):
    finished_signal = pyqtSignal(int, float)  # To signal when the task is done
    add_text_signal = pyqtSignal(str)        # To emit log messages

    def __init__(self, task_queue, available_tr):
        super().__init__()
        self.task_queue = task_queue
        self._running = True

        self.body_counter = 0
        self.started_bodys = 0
        self.available_tr = available_tr

    def stop(self):
        """Stop the worker."""
        self._running = False

    def run(self):
        """Main loop to process tasks."""

        while self._running:
            try:
                # Wait for a task to arrive (blocking)
                task = self.task_queue.get(timeout=1)  # Wait for up to 1 second
                if task is None:  # A `None` task can be used to signal shutdown
                    break

                body = task
                print("Dupa")
                self.update_available_tr(body)
                self.task_queue.task_done()

            except Exception as e:
                continue  # Timeout occurred, or queue was empty

    def update_available_tr(self, body: Body):
        self.body_counter += 1

        available_body_parts_transitions = {
            "upper_panel": [],
            "middle_panel": [],
            "lower_panel": [],
            "armrest": [],
            "cup_holder": [],
            "framework": []}
        self.define_available_tr(available_body_parts_transitions, body)

        self.available_tr.extend(["T002", "T003", "T004"])
        for value in available_body_parts_transitions.values():
            self.available_tr.extend(value)
        self.available_tr.extend(["T901", "T902", "T903", "T904", "T905"])

    def define_available_tr(self, available_body_parts_transitions, body: Body):

        available_body_parts_transitions["upper_panel"].extend(["T101", "T102"])
        if body.upper_panel.ac_type == "2-strefowa":
            available_body_parts_transitions["upper_panel"].extend(["T103", "T105", "T107"])
        elif body.upper_panel.ac_type == "4-strefowa":
            available_body_parts_transitions["upper_panel"].extend(["T104", "T106", "T108"])
        if body.upper_panel.is_controlable == "Tak":
            available_body_parts_transitions["upper_panel"].extend(["T109", "T111", "T112"])
        elif body.upper_panel.is_controlable == "Nie":
            available_body_parts_transitions["upper_panel"].extend(["T110", "T113"])

        available_body_parts_transitions["middle_panel"].extend(["T201", "T202"])
        if body.middle_panel.functionality == "Interfejs multimedialny":
            available_body_parts_transitions["middle_panel"].extend(["T203", "T205", "T207"])
        elif body.middle_panel.functionality == "Schowek":
            available_body_parts_transitions["middle_panel"].extend(["T204", "T206", "T208"])

        available_body_parts_transitions["lower_panel"].extend(["T301", "T302"])
        if body.lower_panel.functionality == "Ładowarka bezprzewodowa":
            available_body_parts_transitions["lower_panel"].extend(["T303", "T305", "T307"])
        elif body.lower_panel.functionality == "Półka":
            available_body_parts_transitions["lower_panel"].extend(["T304", "T306", "T308"])
        if body.lower_panel.is_cup == "Tak":
            available_body_parts_transitions["lower_panel"].extend(["T309", "T311", "T312"])
        elif body.lower_panel.is_cup == "Nie":
            available_body_parts_transitions["lower_panel"].extend(["T310", "T313"])
        if body.lower_panel.color == "Czerwony":
            available_body_parts_transitions["lower_panel"].extend(["T314", "T317"])
        elif body.lower_panel.color == "Zielony":
            available_body_parts_transitions["lower_panel"].extend(["T315", "T318"])
        elif body.lower_panel.color == "Niebieski":
            available_body_parts_transitions["lower_panel"].extend(["T316", "T319"])
        available_body_parts_transitions["lower_panel"].extend(["T320"])


        available_body_parts_transitions["armrest"].extend(["T401", "T402"])
        if body.armrest.heating == "Tak":
            available_body_parts_transitions["armrest"].extend(["T403", "T405", "T406"])
        elif body.armrest.heating == "Nie":
            available_body_parts_transitions["armrest"].extend(["T404", "T407"])
        if body.armrest.material == "Skóra":
            available_body_parts_transitions["armrest"].extend(["T408", "T411"])
        elif body.armrest.material == "Eko skóra":
            available_body_parts_transitions["armrest"].extend(["T409", "T412"])
        elif body.armrest.material == "Sztuczna skóra":
            available_body_parts_transitions["armrest"].extend(["T410", "T413"])
        available_body_parts_transitions["armrest"].extend(["T414"])
        if body.armrest.color == "Czerwony":
            available_body_parts_transitions["armrest"].extend(["T415", "T418"])
        elif body.armrest.color == "Zielony":
            available_body_parts_transitions["armrest"].extend(["T416", "T419"])
        elif body.armrest.color == "Niebieski":
            available_body_parts_transitions["armrest"].extend(["T417", "T420"])
        available_body_parts_transitions["armrest"].extend(["T421"])


        available_body_parts_transitions["cup_holder"].extend(["T501", "T502", "T503", "T504", "T505"])
        if body.cup_holder.usb_socket == "Tak":
            available_body_parts_transitions["cup_holder"].extend(["T506", "T508", "T509"])
        elif body.cup_holder.usb_socket == "Nie":
            available_body_parts_transitions["cup_holder"].extend(["T507", "T510"])
        if body.cup_holder.color == "Czerwony":
            available_body_parts_transitions["cup_holder"].extend(["T511", "T514"])
        elif body.cup_holder.color == "Zielony":
            available_body_parts_transitions["cup_holder"].extend(["T512", "T515"])
        elif body.cup_holder.color == "Niebieski":
            available_body_parts_transitions["cup_holder"].extend(["T513", "T516"])
        available_body_parts_transitions["cup_holder"].extend(["T517"])

    
        available_body_parts_transitions["framework"].extend(["T601", "T602", "T603", "T604", "T605"])
        if body.framework.material == "Skóra":
            available_body_parts_transitions["framework"].extend(["T606", "T609"])
        elif body.framework.material == "Eko skóra":
            available_body_parts_transitions["framework"].extend(["T607", "T610"])
        elif body.framework.material == "Sztuczna skóra":
            available_body_parts_transitions["framework"].extend(["T608", "T611"])
        available_body_parts_transitions["framework"].extend(["T612"])
        if body.framework.color == "Czerwony":
            available_body_parts_transitions["framework"].extend(["T613", "T616"])
        elif body.framework.color == "Zielony":
            available_body_parts_transitions["framework"].extend(["T614", "T617"])
        elif body.framework.color == "Niebieski":
            available_body_parts_transitions["framework"].extend(["T615", "T618"])
        available_body_parts_transitions["framework"].extend(["T619"])
