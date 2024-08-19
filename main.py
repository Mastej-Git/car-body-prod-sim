from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QStackedWidget, 
    QFrame, QSizePolicy, QGroupBox, QComboBox, QScrollArea
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
import time
import copy
import threading

from PetrisNet import PetriNet
from Body import Body
from Cup import Cup
from AirConditioning import AirConditioning
from CarScreen import CarScreen

from StyleSheets import *
from Enums import CupMaterial, ScreenTypes

from CupPetriNet import cup_main_petri_net

lock = threading.Lock()

class PetriNetThread(QThread):

    finished_signal = pyqtSignal(int)

    def __init__(self, thread_id, body: Body):
        super().__init__()
        self._running = True
        # self.finished_signal.connect(self.stop)
        self.petri_net = cup_main_petri_net
        self.body = body
        self.thread_id = thread_id
        self.available_transitions = []
        self.executed_transitions = []

        if self.body.cup.material == CupMaterial.ALUMINUM:
            self.available_transitions = ["T2", "T3", "T6", "T9", "T12", "T15", "T18", "T21", "T24", "T27", "T28"]
        elif self.body.cup.material == CupMaterial.STAINLESS_STEEL:
            self.available_transitions = ["T2", "T4", "T7", "T10", "T13", "T16", "T19", "T22", "T25", "T27", "T28"]  

        self.petri_net.fire_transition("T1")

        print(self.thread_id)

    # def run(self):
    #     while self._running:
    #         for name, transition in self.petri_net.transitions.items():
    #             if transition.is_enabled() and name in self.available_transitions:
    #                 with lock:
    #                     print(f"\nThread id: {self.thread_id} - Firing Transition {name}")
    #                     self.petri_net.fire_transition(name)
    #                     self.executed_transitions.append(name)
    #                     # print(self.petri_net)
    #                     time.sleep(3)

    #             if self.executed_transitions == self.available_transitions:
    #                 break
    #         if self.executed_transitions == self.available_transitions:
    #             break
            
    #     self.finished_signal.emit(self.thread_id)

    def run(self):
        i = 0

        while self._running:
            if self.petri_net.transitions[self.available_transitions[i]].is_enabled():
                print(f"\nThread id: {self.thread_id} - Firing Transition {self.available_transitions[i]}")
                with lock:
                    self.petri_net.fire_transition(self.available_transitions[i])
                self.executed_transitions.append(self.available_transitions[i])
                i += 1
                print(self.petri_net)
                time.sleep(3)

            if self.executed_transitions == self.available_transitions:
                break
            
        self.finished_signal.emit(self.thread_id)

    def stop(self):
        self._running = False

class CarBodyGroupBox():

    def __init__(self, body: Body) -> None:
        
        self.group_box = QGroupBox()
        self.body = body

        label_text = self.create_label()

        label = QLabel(label_text)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        label.setStyleSheet(style_sheet_label)

        self.button_schedule = self.create_push_button("Schedule", 200, 40)
        self.button_remove = self.create_push_button("Remove", 200, 40)
        self.button_edit = self.create_push_button("Edit", 200, 40)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.button_schedule)
        buttons_layout.addWidget(self.button_remove)
        buttons_layout.addWidget(self.button_edit)

        main_layout = QHBoxLayout()

        main_layout.addWidget(label)
        main_layout.addLayout(buttons_layout)

        self.group_box.setLayout(main_layout)

    def get_car_body_group_box(self):
        return self.group_box
    
    def create_label(self):

        label = "Body consists of following elements:\n"

        if self.body.cup.is_activated == True:
            label += f"▸  Cup:\n\t ▪ Material: {self.body.cup.material}\n\t ▪ Size: {self.body.cup.size}\n"
        if self.body.car_screen.is_activated == True:
            label += f"▸  Screen:\n\t ▪ Type: {self.body.car_screen.type}\n\t ▪ Size: {self.body.car_screen.size}\n"

        return label

    def create_push_button(self, name, size_x, size_y):
        button = QPushButton(name)
        button.setStyleSheet(style_sheet_QPushButton)
        button.setFixedSize(size_x, size_y)

        return button

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.body_counter = 0
        self.list_of_threads = []

        self.body = Body(Cup("", ""), AirConditioning("", "", ""), CarScreen("", ""))

        self.setWindowTitle("Tab Example")
        self.setGeometry(100, 100, 800, 1000)

        central_widget = QFrame()
        central_widget.setStyleSheet(style_sheet_central_widget)
        layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        self.tabs.tabBar().setExpanding(True)
        self.tabs.setStyleSheet(style_sheet_tab)

        
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab1, "Add Body")
        self.tabs.addTab(self.tab2, "Current Body state")
        self.tabs.addTab(self.tab3, "Gantt chart")

        self.create_tabs_content()
        layout.addWidget(self.tabs)
        self.setCentralWidget(central_widget)

        self.petri_net = PetriNet()

    def create_tabs_content(self):
        layout1 = QVBoxLayout()
        sub_tab_widget = QTabWidget()
        sub_tab_widget.setTabPosition(QTabWidget.West)
        sub_tab_widget.setStyleSheet(style_sheet_sub_tab)

        sub_tab1 = QWidget()
        sub_tab2 = QWidget()
        sub_tab3 = QWidget()

        self.gowno = 1

        sub_tab1 = self.create_sub_tab_cup_content()

        sub_tab2 = self.create_sub_tab_screen_content()

        sub_layout3 = QVBoxLayout()
        sub_layout3.addWidget(QLabel("This is the content of Sub-Tab 3"))
        sub_tab3.setLayout(sub_layout3)

        sub_tab_widget.addTab(sub_tab1, "Cup")
        sub_tab_widget.addTab(sub_tab2, "Screen")
        sub_tab_widget.addTab(sub_tab3, "Air ventilation")

        stacked_widget = QStackedWidget()
        stacked_widget.addWidget(sub_tab_widget)

        overlay_widget = QWidget()
        overlay_layout = QVBoxLayout(overlay_widget)
        overlay_layout.addWidget(stacked_widget)

        plus_button = QPushButton("+")
        plus_button.setFixedSize(40, 40)
        plus_button.setStyleSheet(style_sheet_QPushButton)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(plus_button)
        overlay_layout.addLayout(button_layout)

        layout1.addWidget(overlay_widget)
        self.tab1.setLayout(layout1)

        self.layout = QVBoxLayout()

        self.starting_label = QLabel("There are no bodys in the making")
        self.starting_label.setStyleSheet(style_sheet_label)
        self.starting_label.setAlignment(Qt.AlignCenter)

        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.outer_layout = QVBoxLayout(self.scroll_widget)

        self.scroll_widget.setLayout(self.outer_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        self.outer_layout.addWidget(self.starting_label)
        self.layout.addWidget(self.scroll_area)
        self.tab2.setLayout(self.layout)

        layout3 = QVBoxLayout()
        layout3.addWidget(QLabel("This is the content of Tab 3"))
        self.tab3.setLayout(layout3)

    def create_sub_tab_cup_content(self):

        sub_tab_cup = QWidget()

        sub_layout1 = QVBoxLayout()

        groupBox = QGroupBox("Cup parameters")
        label_material = QLabel("Material")
        label_material.setStyleSheet(style_sheet_label)
        label_size = QLabel("Size")
        label_size.setStyleSheet(style_sheet_label)

        combo_box_material = QComboBox()
        # combo_box_material.addItems([CupMaterial.ALUMINUM, CupMaterial.STAINLESS_STEEL, CupMaterial.POLICARBONATE])
        combo_box_material.addItems(["Aluminum", "Stainless steel", "Policarbonate"])
        combo_box_material.setStyleSheet(style_sheet_QComboBox)
        combo_box_material.currentIndexChanged.connect(self.on_change_cbox_cup_material)
        combo_box_material.activated.connect(self.on_activate_cbox_cup_material)

        combo_box_size = QComboBox()
        combo_box_size.addItems(["500 ml", "750 ml", "1 L"])
        combo_box_size.setStyleSheet(style_sheet_QComboBox)
        combo_box_size.currentIndexChanged.connect(self.on_change_cbox_cup_size)
        combo_box_size.activated.connect(self.on_activate_cbox_cup_size)

        button_add_to_corpse = QPushButton("Add")
        button_add_to_corpse.setStyleSheet(style_sheet_QPushButton)
        button_add_to_corpse.clicked.connect(self.on_change_pb_cup)

        vbox_main = QVBoxLayout()
        hbox_cboxs = QHBoxLayout()
        vbox_sub1 = QVBoxLayout()
        vbox_sub2 = QVBoxLayout()

        vbox_sub1.addWidget(label_material)
        vbox_sub1.addWidget(combo_box_material)
        vbox_sub1.setSpacing(5)

        vbox_sub2.addWidget(label_size)
        vbox_sub2.addWidget(combo_box_size)
        vbox_sub2.setSpacing(5)

        hbox_cboxs.addLayout(vbox_sub1)
        hbox_cboxs.addLayout(vbox_sub2)
        hbox_cboxs.setSpacing(20)

        vbox_main.addLayout(hbox_cboxs)
        vbox_main.addWidget(button_add_to_corpse)

        groupBox.setLayout(vbox_main)

        sub_layout1.addWidget(groupBox)
        sub_tab_cup.setLayout(sub_layout1)

        return sub_tab_cup
    
    def create_sub_tab_screen_content(self):

        sub_tab_cup = QWidget()

        sub_layout1 = QVBoxLayout()

        groupBox = QGroupBox("Screen parameters")
        label_material = QLabel("Type")
        label_material.setStyleSheet(style_sheet_label)
        label_size = QLabel("Size")
        label_size.setStyleSheet(style_sheet_label)

        combo_box_material = QComboBox()
        # combo_box_material.addItems([ScreenTypes.RESISTIVE, ScreenTypes.CAPACITIVE, ScreenTypes.PROJECTED_CAPACITIVE])
        combo_box_material.addItems(["Resistive", "Capacitive", "Projected Capacitive"])
        combo_box_material.setStyleSheet(style_sheet_QComboBox)
        combo_box_material.currentIndexChanged.connect(self.on_change_cbox_screen_type)
        combo_box_material.activated.connect(self.on_activate_cbox_screen_type)

        combo_box_size = QComboBox()
        combo_box_size.addItems(["7 inches", "8 inches", "10 inches"])
        combo_box_size.setStyleSheet(style_sheet_QComboBox)
        combo_box_size.currentIndexChanged.connect(self.on_change_cbox_screen_size)
        combo_box_size.activated.connect(self.on_activate_cbox_screen_size)

        button_add_to_corpse = QPushButton("Add")
        button_add_to_corpse.setStyleSheet(style_sheet_QPushButton)
        button_add_to_corpse.clicked.connect(self.on_change_pb_screen)

        vbox_main = QVBoxLayout()
        hbox_cboxs = QHBoxLayout()
        vbox_sub1 = QVBoxLayout()
        vbox_sub2 = QVBoxLayout()

        vbox_sub1.addWidget(label_material)
        vbox_sub1.addWidget(combo_box_material)
        vbox_sub1.setSpacing(5)

        vbox_sub2.addWidget(label_size)
        vbox_sub2.addWidget(combo_box_size)
        vbox_sub2.setSpacing(5)

        hbox_cboxs.addLayout(vbox_sub1)
        hbox_cboxs.addLayout(vbox_sub2)
        hbox_cboxs.setSpacing(20)

        vbox_main.addLayout(hbox_cboxs)
        vbox_main.addWidget(button_add_to_corpse)

        groupBox.setLayout(vbox_main)

        sub_layout1.addWidget(groupBox)
        sub_tab_cup.setLayout(sub_layout1)

        return sub_tab_cup
    
    def create_group_box_body(self):
        self.car_body_group_box = CarBodyGroupBox(self.body)
        self.car_body_group_box.button_schedule.pressed.connect(self.on_schedule_clicked)

    def on_change_cbox_cup_material(self, index):
        print(f"Selected material index: {index}")
        if index == 0:
            self.body.cup.material = CupMaterial.ALUMINUM
        elif index == 1:
            self.body.cup.material = CupMaterial.STAINLESS_STEEL
        elif index == 2:
            self.body.cup.material = CupMaterial.POLICARBONATE
        self.body.cup.check_activation()

    def on_change_cbox_cup_size(self, index):
        print(f"Selected size index: {index}")
        if index == 0:
            self.body.cup.size = "500 ml"
        elif index == 1:
            self.body.cup.size = "750 ml"
        elif index == 2:
            self.body.cup.size = "1 L"
        self.body.cup.check_activation()

    def on_activate_cbox_cup_material(self, index):
        print(f"Selected material index: {index}")
        if index == 0:
            self.body.cup.material = CupMaterial.ALUMINUM
        elif index == 1:
            self.body.cup.material = CupMaterial.STAINLESS_STEEL
        elif index == 2:
            self.body.cup.material = CupMaterial.POLICARBONATE
        self.body.cup.check_activation()

    def on_activate_cbox_cup_size(self, index):
        print(f"Selected size index: {index}")
        if index == 0:
            self.body.cup.size = "500 ml"
        elif index == 1:
            self.body.cup.size = "750 ml"
        elif index == 2:
            self.body.cup.size = "1 L"
        self.body.cup.check_activation()

    def on_change_pb_cup(self):
        print(f"Cup added with parameters: {self.body.cup.material}, {self.body.cup.size}")

        self.create_group_box_body()
        self.car_body_group_box.group_box.setFixedSize(738, 200)
        if (self.body_counter == 0):
            self.body_counter += 1
            self.outer_layout.removeWidget(self.starting_label)
            self.starting_label.deleteLater()

        if self.outer_layout.count() == self.body_counter:
            self.outer_layout.removeWidget(self.outer_layout.itemAt(self.body_counter - 1).widget())
        self.outer_layout.addWidget(self.car_body_group_box.group_box)

    def on_change_cbox_screen_type(self, index):
        print(f"Selected material index: {index}")
        if index == 0:
            self.body.car_screen.type = ScreenTypes.RESISTIVE
        elif index == 1:
            self.body.car_screen.type = ScreenTypes.CAPACITIVE
        elif index == 2:
            self.body.car_screen.type = ScreenTypes.PROJECTED_CAPACITIVE
        self.body.car_screen.check_activation()

    def on_change_cbox_screen_size(self, index):
        print(f"Selected size index: {index}")
        if index == 0:
            self.body.car_screen.size = "7 inches"
        elif index == 1:
            self.body.car_screen.size = "8 inches"
        elif index == 2:
            self.body.car_screen.size = "10 inches"
        self.body.car_screen.check_activation()

    def on_activate_cbox_screen_type(self, index):
        print(f"Selected material index: {index}")
        if index == 0:
            self.body.car_screen.type = ScreenTypes.RESISTIVE
        elif index == 1:
            self.body.car_screen.type = ScreenTypes.CAPACITIVE
        elif index == 2:
            self.body.car_screen.type = ScreenTypes.PROJECTED_CAPACITIVE
        self.body.car_screen.check_activation()

    def on_activate_cbox_screen_size(self, index):
        print(f"Selected size index: {index}")
        if index == 0:
            self.body.car_screen.size = "7 inches"
        elif index == 1:
            self.body.car_screen.size = "8 inches"
        elif index == 2:
            self.body.car_screen.size = "10 inches"
        self.body.car_screen.check_activation()

    def on_change_pb_screen(self):
        print(f"Screen added with parameters: {self.body.car_screen.type}, {self.body.car_screen.size}")

        self.create_group_box_body()
        self.car_body_group_box.group_box.setFixedSize(738, 200)
        if (self.body_counter == 0):
            self.body_counter += 1
            self.outer_layout.removeWidget(self.starting_label)
            self.starting_label.deleteLater()

        if self.outer_layout.count() == self.body_counter:
            self.outer_layout.removeWidget(self.outer_layout.itemAt(self.body_counter - 1).widget())
        self.outer_layout.addWidget(self.car_body_group_box.group_box)

    def create_push_button(self, name, size_x, size_y):
        button = QPushButton(name)
        button.setStyleSheet(style_sheet_QPushButton)
        button.setFixedSize(size_x, size_y)

        return button
    
    @pyqtSlot()
    def on_schedule_clicked(self):
        print(f"\nScheduled body nr: {self.body_counter}")

        new_petri_net_thread = PetriNetThread(self.body_counter, self.body)
        new_petri_net_thread.finished_signal.connect(self.on_thread_finished)
        self.list_of_threads.append(new_petri_net_thread)
        # self.petri_net_thread.start()
        self.list_of_threads[self.body_counter - 1].start()

        self.body.cup.remove_parameters()
        self.body.car_screen.remove_parameters()
        self.car_body_group_box.button_schedule.setEnabled(False)

        self.body_counter += 1

    @pyqtSlot(int)
    def on_thread_finished(self, thread_id):
        print(f"Thread {thread_id} has finished.")

def main():
    app = QApplication([])
    app.setStyleSheet(style_sheet_app)
    window = GUI()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
