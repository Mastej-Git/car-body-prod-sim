import time
import threading

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QStackedWidget,
    QFrame,
    QGroupBox,
    QComboBox,
    QScrollArea,
    QRadioButton
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QMutex

from PetrisNet import PetriNet

from Body import Body
from body_parts.Cup import Cup
from body_parts.AirConditioning import AirConditioning
from body_parts.CarScreen import CarScreen

from body_parts.UpperPanel import UpperPanel
from body_parts.MiddlePanel import MiddlePanel
from body_parts.LowerPanel import LowerPanel

from utils.MatPlotlibWidget import MatplotlibWidget

from other.StyleSheets import (
    style_sheet_central_widget,
    style_sheet_app,
    style_sheet_label,
    style_sheet_QComboBox,
    style_sheet_QPushButton,
    style_sheet_sub_tab,
    style_sheet_tab
)
from other.Enums import CupMaterial, ScreenTypes

from CupPetriNet import cup_main_petri_net

lock = threading.Lock()
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

        label = "Korpus zawiera następujące elementy:\n"

        if self.body.cup.is_activated is True:
            label += f"▸  Cup:\n\t ▪ Material: {self.body.cup.material}\n\t ▪ Size: {self.body.cup.size}\n"
        if self.body.car_screen.is_activated is True:
            label += f"▸  Screen:\n\t ▪ Type: {self.body.car_screen.type}\n\t ▪ Size: {self.body.car_screen.size}\n"
        if self.body.upper_panel.is_activated is True:
            label += f"▸  Panel gorny:\n\t ▪ Sterowanie klimatyzacja: {self.body.upper_panel.is_controlable}\n\t ▪ Typ: {self.body.upper_panel.type}\n"
        if self.body.middle_panel.is_activated is True:
            label += f"▸  Panel środkowy:\n\t ▪ Funkcjonalność: {self.body.middle_panel.functionality}\n"
        if self.body.lower_panel.is_activated is True:
            label += (f"▸  Panel dolny:\n\t ▪ Funkcjonalność: {self.body.lower_panel.functionality}\n\t "
                      f"▪ Chwytaki na kubki: {self.body.lower_panel.is_cup}\n\t" 
                      f" ▪ Kolor: {self.body.lower_panel.color}\n")

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

        self.body = Body(Cup("", ""), AirConditioning("", "", ""), CarScreen("", ""), UpperPanel("", ""), MiddlePanel(""), LowerPanel("", "", ""))
        self.petri_net = cup_main_petri_net

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
        self.tabs.addTab(self.tab1, "Dodaj korpus")
        self.tabs.addTab(self.tab2, "Stan korpusów")
        self.tabs.addTab(self.tab3, "Wykres Gantta")

        self.create_tabs_content()
        layout.addWidget(self.tabs)
        self.setCentralWidget(central_widget)

    def create_tabs_content(self):
        layout1 = QVBoxLayout()
        sub_tab_widget = QTabWidget()
        sub_tab_widget.setTabPosition(QTabWidget.West)
        sub_tab_widget.setStyleSheet(style_sheet_sub_tab)

        sub_tab1 = QWidget()
        sub_tab2 = QWidget()
        sub_tab3 = QWidget()
        sub_tab4 = QWidget()
        sub_tab5 = QWidget()

        self.gowno = 1

        sub_tab1 = self.create_sub_tab_cup_content()
        sub_tab2 = self.create_sub_tab_screen_content()
        sub_tab3 = self.create_sub_tab_upper_panel_content()
        sub_tab4 = self.create_sub_tab_middle_panel_content()
        sub_tab5 = self.create_sub_tab_lower_panel_content()

        sub_tab_widget.addTab(sub_tab1, "Cup")
        sub_tab_widget.addTab(sub_tab2, "Screen")
        sub_tab_widget.addTab(sub_tab3, "Panel górny")
        sub_tab_widget.addTab(sub_tab4, "Panel środkowy")
        sub_tab_widget.addTab(sub_tab5, "Panel dolny")

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

        self.starting_label = QLabel("Brak korpusów w produkcji")
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

        self.mpl_widget = MatplotlibWidget(self.petri_net, self)

        layout3 = QVBoxLayout()
        layout3.addWidget(self.mpl_widget)
        self.mpl_widget.plot()
        self.tab3.setLayout(layout3)

    def create_sub_tab_cup_content(self):

        sub_tab_cup = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Cup parameters")
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

        button_add_to_corpse = QPushButton("Dodaj")
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

        group_box1.setLayout(vbox_main)

        sub_layout1.addWidget(group_box1)
        sub_tab_cup.setLayout(sub_layout1)

        return sub_tab_cup
    
    def create_sub_tab_screen_content(self):

        sub_tab_cup = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Screen parameters")
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

        button_add_to_corpse = QPushButton("Dodaj")
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

        group_box1.setLayout(vbox_main)

        sub_layout1.addWidget(group_box1)
        sub_tab_cup.setLayout(sub_layout1)

        return sub_tab_cup
    
    def create_sub_tab_upper_panel_content(self):

        sub_tab_cup = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Parametry panelu górnego")
        label_material = QLabel("Sterowanie klimatyzacją")
        label_material.setStyleSheet(style_sheet_label)
        label_size = QLabel("Klimatyzacja")
        label_size.setStyleSheet(style_sheet_label)

        radio1 = QRadioButton("Tak")
        radio2 = QRadioButton("Nie")
        radio1.toggled.connect(self.on_radio_button_upper_panel_clicked)
        radio2.toggled.connect(self.on_radio_button_upper_panel_clicked)

        radio_groupbox1 = QGroupBox()
        radio_vboxlayout1 = QVBoxLayout()

        radio_vboxlayout1.addWidget(radio1)
        radio_vboxlayout1.addWidget(radio2)

        radio_groupbox1.setLayout(radio_vboxlayout1)

        radio3 = QRadioButton("4-strefowa")
        radio4 = QRadioButton("2-strefowa")
        radio3.toggled.connect(self.on_radio_button_upper_panel_clicked)
        radio4.toggled.connect(self.on_radio_button_upper_panel_clicked)

        radio_groupbox2 = QGroupBox()
        radio_vboxlayout2 = QVBoxLayout()

        radio_vboxlayout2.addWidget(radio3)
        radio_vboxlayout2.addWidget(radio4)

        radio_groupbox2.setLayout(radio_vboxlayout2)

        button_add_to_corpse = QPushButton("Dodaj")
        button_add_to_corpse.setStyleSheet(style_sheet_QPushButton)
        button_add_to_corpse.clicked.connect(self.pb_upper_panel_clicked)

        vbox_main = QVBoxLayout()
        hbox_cboxs = QHBoxLayout()
        vbox_sub1 = QVBoxLayout()
        vbox_sub2 = QVBoxLayout()

        vbox_sub1.addWidget(label_material)
        vbox_sub1.addWidget(radio_groupbox1)
        vbox_sub1.setSpacing(5)

        vbox_sub2.addWidget(label_size)
        vbox_sub2.addWidget(radio_groupbox2)
        vbox_sub2.setSpacing(5)

        hbox_cboxs.addLayout(vbox_sub1)
        hbox_cboxs.addLayout(vbox_sub2)
        hbox_cboxs.setSpacing(20)

        vbox_main.addLayout(hbox_cboxs)
        vbox_main.addWidget(button_add_to_corpse)

        group_box1.setLayout(vbox_main)

        sub_layout1.addWidget(group_box1)
        sub_tab_cup.setLayout(sub_layout1)

        return sub_tab_cup
    
    def create_sub_tab_middle_panel_content(self):

        sub_tab_cup = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Parametry panelu środkowego")
        label_material = QLabel("Funkcjonalność")
        label_material.setStyleSheet(style_sheet_label)

        radio1 = QRadioButton("Interfejs multimedialny")
        radio2 = QRadioButton("Schowek")
        radio1.toggled.connect(self.on_radio_button_middle_panel_clicked)
        radio2.toggled.connect(self.on_radio_button_middle_panel_clicked)

        radio_groupbox1 = QGroupBox()
        radio_vboxlayout1 = QVBoxLayout()

        radio_vboxlayout1.addWidget(radio1)
        radio_vboxlayout1.addWidget(radio2)

        radio_groupbox1.setLayout(radio_vboxlayout1)

        button_add_to_corpse = QPushButton("Dodaj")
        button_add_to_corpse.setStyleSheet(style_sheet_QPushButton)
        button_add_to_corpse.clicked.connect(self.pb_middle_panel_clicked)

        vbox_main = QVBoxLayout()
        vbox_sub1 = QVBoxLayout()
        vbox_sub2 = QVBoxLayout()

        vbox_sub1.addWidget(label_material)
        vbox_sub1.addWidget(radio_groupbox1)
        vbox_sub1.setSpacing(5)

        vbox_main.addLayout(vbox_sub1)
        vbox_main.addLayout(vbox_sub2)
        vbox_main.addWidget(button_add_to_corpse)

        group_box1.setLayout(vbox_main)

        sub_layout1.addWidget(group_box1)
        sub_tab_cup.setLayout(sub_layout1)

        return sub_tab_cup    
    
    def create_sub_tab_lower_panel_content(self):

        sub_tab_cup = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Parametry panelu dolnego")
        label_material = QLabel("Funkcjonalność")
        label_material.setStyleSheet(style_sheet_label)
        label_size = QLabel("Miejsce na kubek")
        label_size.setStyleSheet(style_sheet_label)

        radio1 = QRadioButton("Ładowarka bezprzewodowa")
        radio2 = QRadioButton("Półka")
        radio1.toggled.connect(self.on_radio_button_lower_panel_clicked)
        radio2.toggled.connect(self.on_radio_button_lower_panel_clicked)

        radio_groupbox1 = QGroupBox()
        radio_vboxlayout1 = QVBoxLayout()

        radio_vboxlayout1.addWidget(radio1)
        radio_vboxlayout1.addWidget(radio2)

        radio_groupbox1.setLayout(radio_vboxlayout1)

        radio3 = QRadioButton("Tak")
        radio4 = QRadioButton("Nie")
        radio3.toggled.connect(self.on_radio_button_lower_panel_clicked)
        radio4.toggled.connect(self.on_radio_button_lower_panel_clicked)

        radio_groupbox2 = QGroupBox()
        radio_vboxlayout2 = QVBoxLayout()

        radio_vboxlayout2.addWidget(radio3)
        radio_vboxlayout2.addWidget(radio4)

        radio_groupbox2.setLayout(radio_vboxlayout2)

        button_add_to_corpse = QPushButton("Dodaj")
        button_add_to_corpse.setStyleSheet(style_sheet_QPushButton)
        button_add_to_corpse.clicked.connect(self.pb_lower_panel_clicked)

        combo_box_color = QComboBox()
        combo_box_color.addItems(["Czerwony", "Zielony", "Niebieski"])
        combo_box_color.setStyleSheet(style_sheet_QComboBox)
        combo_box_color.currentIndexChanged.connect(self.on_change_cbox_lower_panel_color)
        combo_box_color.activated.connect(self.on_activate_cbox_lower_panel_color)

        vbox_main = QVBoxLayout()
        vbox_sub1 = QVBoxLayout()
        vbox_sub2 = QVBoxLayout()

        vbox_sub1.addWidget(label_material)
        vbox_sub1.addWidget(radio_groupbox1)
        vbox_sub1.setSpacing(5)

        vbox_sub2.addWidget(label_size)
        vbox_sub2.addWidget(radio_groupbox2)
        vbox_sub2.setSpacing(5)

        vbox_main.addLayout(vbox_sub1)
        vbox_main.addLayout(vbox_sub2)
        vbox_main.addWidget(combo_box_color)
        vbox_main.addWidget(button_add_to_corpse)

        group_box1.setLayout(vbox_main)

        sub_layout1.addWidget(group_box1)
        sub_tab_cup.setLayout(sub_layout1)

        return sub_tab_cup
    
    def create_group_box_body(self):
        self.car_body_group_box = CarBodyGroupBox(self.body)
        self.car_body_group_box.button_schedule.pressed.connect(self.on_schedule_clicked)

    def on_change_cbox_cup_material(self, index):
        # print(f"Selected material index: {index}")
        if index == 0:
            self.body.cup.material = CupMaterial.ALUMINUM
        elif index == 1:
            self.body.cup.material = CupMaterial.STAINLESS_STEEL
        elif index == 2:
            self.body.cup.material = CupMaterial.POLICARBONATE
        self.body.cup.check_activation()

    def on_change_cbox_cup_size(self, index):
        # print(f"Selected size index: {index}")
        if index == 0:
            self.body.cup.size = "500 ml"
        elif index == 1:
            self.body.cup.size = "750 ml"
        elif index == 2:
            self.body.cup.size = "1 L"
        self.body.cup.check_activation()

    def on_activate_cbox_cup_material(self, index):
        # print(f"Selected material index: {index}")
        if index == 0:
            self.body.cup.material = CupMaterial.ALUMINUM
        elif index == 1:
            self.body.cup.material = CupMaterial.STAINLESS_STEEL
        elif index == 2:
            self.body.cup.material = CupMaterial.POLICARBONATE
        self.body.cup.check_activation()

    def on_activate_cbox_cup_size(self, index):
        # print(f"Selected size index: {index}")
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
        # self.car_body_group_box.group_box.setFixedSize(738, 200)
        self.car_body_group_box.group_box.setMinimumWidth(738)
        if self.body_counter == 0:
            self.body_counter += 1
            self.outer_layout.removeWidget(self.starting_label)
            self.starting_label.deleteLater()

        if self.outer_layout.count() == self.body_counter:
            self.outer_layout.removeWidget(self.outer_layout.itemAt(self.body_counter - 1).widget())
        self.outer_layout.addWidget(self.car_body_group_box.group_box)

    def on_change_cbox_screen_type(self, index):
        # print(f"Selected material index: {index}")
        if index == 0:
            self.body.car_screen.type = ScreenTypes.RESISTIVE
        elif index == 1:
            self.body.car_screen.type = ScreenTypes.CAPACITIVE
        elif index == 2:
            self.body.car_screen.type = ScreenTypes.PROJECTED_CAPACITIVE
        self.body.car_screen.check_activation()

    def on_change_cbox_screen_size(self, index):
        # print(f"Selected size index: {index}")
        if index == 0:
            self.body.car_screen.size = "7 inches"
        elif index == 1:
            self.body.car_screen.size = "8 inches"
        elif index == 2:
            self.body.car_screen.size = "10 inches"
        self.body.car_screen.check_activation()

    def on_activate_cbox_screen_type(self, index):
        # print(f"Selected material index: {index}")
        if index == 0:
            self.body.car_screen.type = ScreenTypes.RESISTIVE
        elif index == 1:
            self.body.car_screen.type = ScreenTypes.CAPACITIVE
        elif index == 2:
            self.body.car_screen.type = ScreenTypes.PROJECTED_CAPACITIVE
        self.body.car_screen.check_activation()

    def on_activate_cbox_screen_size(self, index):
        # print(f"Selected size index: {index}")
        if index == 0:
            self.body.car_screen.size = "7 inches"
        elif index == 1:
            self.body.car_screen.size = "8 inches"
        elif index == 2:
            self.body.car_screen.size = "10 inches"
        self.body.car_screen.check_activation()

    def on_change_cbox_lower_panel_color(self, index):
        # print(f"Selected size index: {index}")
        if index == 0:
            self.body.lower_panel.color = "Czerwony"
        elif index == 1:
            self.body.lower_panel.color = "Zielony"
        elif index == 2:
            self.body.lower_panel.color = "Niebieski"
        self.body.lower_panel.check_activation()

    def on_activate_cbox_lower_panel_color(self, index):
        # print(f"Selected material index: {index}")
        if index == 0:
            self.body.lower_panel.color = "Czerwony"
        elif index == 1:
            self.body.lower_panel.color = "Zielony"
        elif index == 2:
            self.body.lower_panel.color = "Niebieski"
        self.body.lower_panel.check_activation()

    def on_change_pb_screen(self):
        print(f"Screen added with parameters: {self.body.car_screen.type}, {self.body.car_screen.size}")

        self.create_group_box_body()
        # self.car_body_group_box.group_box.setFixedSize(738, 200)
        self.car_body_group_box.group_box.setMinimumWidth(738)
        if self.body_counter == 0:
            self.body_counter += 1
            self.outer_layout.removeWidget(self.starting_label)
            self.starting_label.deleteLater()

        if self.outer_layout.count() == self.body_counter:
            self.outer_layout.removeWidget(self.outer_layout.itemAt(self.body_counter - 1).widget())
        self.outer_layout.addWidget(self.car_body_group_box.group_box)

    def on_radio_button_upper_panel_clicked(self):
        sender = self.sender()

        if sender.isChecked():
            if (sender.text() == "Tak" or sender.text() == "Nie"):
                self.body.upper_panel.is_controlable = sender.text()
                pass
            else:
                self.body.upper_panel.type = sender.text()
            print(f'Selected option: {sender.text()}')

        self.body.upper_panel.check_activation()

    def on_radio_button_middle_panel_clicked(self):
        sender = self.sender()

        if sender.isChecked():
            self.body.middle_panel.functionality = sender.text()
            print(f'Selected option: {sender.text()}')

        self.body.middle_panel.check_activation()

    def on_radio_button_lower_panel_clicked(self):
        sender = self.sender()

        if sender.isChecked():
            if (sender.text() == "Tak" or sender.text() == "Nie"):
                self.body.lower_panel.is_cup = sender.text()
                pass
            else:
                self.body.lower_panel.functionality = sender.text()
            print(f'Selected option: {sender.text()}')

        self.body.lower_panel.check_activation()

    def pb_upper_panel_clicked(self):
        print(f"Gorny panel dodany z parametrami: {self.body.upper_panel.is_controlable}, {self.body.upper_panel.type}")

        self.create_group_box_body()
        # self.car_body_group_box.group_box.setFixedSize(738, 200)
        self.car_body_group_box.group_box.setMinimumWidth(738)
        if self.body_counter == 0:
            self.body_counter += 1
            self.outer_layout.removeWidget(self.starting_label)
            self.starting_label.deleteLater()

        if self.outer_layout.count() == self.body_counter:
            self.outer_layout.removeWidget(self.outer_layout.itemAt(self.body_counter - 1).widget())
        self.outer_layout.addWidget(self.car_body_group_box.group_box)

    def pb_middle_panel_clicked(self):
        print(f"Środkowy panel dodany z parametrami: {self.body.middle_panel.functionality}")

        self.create_group_box_body()
        # self.car_body_group_box.group_box.setFixedSize(738, 200)
        self.car_body_group_box.group_box.setMinimumWidth(738)
        if self.body_counter == 0:
            self.body_counter += 1
            self.outer_layout.removeWidget(self.starting_label)
            self.starting_label.deleteLater()

        if self.outer_layout.count() == self.body_counter:
            self.outer_layout.removeWidget(self.outer_layout.itemAt(self.body_counter - 1).widget())
        self.outer_layout.addWidget(self.car_body_group_box.group_box)

    def pb_lower_panel_clicked(self):
        print(f"Dolny panel dodany z parametrami: {self.body.lower_panel.functionality}, {self.body.lower_panel.is_cup}, {self.body.lower_panel.color}")

        self.create_group_box_body()
        # self.car_body_group_box.group_box.setFixedSize(738, 200)
        self.car_body_group_box.group_box.setMinimumWidth(738)
        if self.body_counter == 0:
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

        new_petri_net_thread = PetriNetThread(self.body_counter, self.body, self.mpl_widget)
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
