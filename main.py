import json, copy

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QStackedWidget,
    QFrame,
    QGroupBox,
    QComboBox,
    QScrollArea,
    QRadioButton,
)

from PyQt5.QtCore import (Qt,
                          pyqtSlot,
                          QMutex)

from Body import Body
from body_parts.UpperPanel import UpperPanel
from body_parts.MiddlePanel import MiddlePanel
from body_parts.LowerPanel import LowerPanel
from body_parts.Armrest import Armrest
from body_parts.CupHolder import CupHolder

from petri_nets.PetriNetThread import PetriNetThread

from other.MatPlotlibWidget import MatplotlibWidget
from qt_classes.AnimatedButton import AnimatedButton
from qt_classes.CarBodyGroupBox import CarBodyGroupBox

from other.StyleSheets import (
    style_sheet_central_widget,
    style_sheet_app,
    style_sheet_label,
    style_sheet_QComboBox,
    style_sheet_sub_tab,
    style_sheet_tab,
    style_sheet_QRadioButton
)

from CupPetriNet import cup_main_petri_net

class ReadJSON():

    def __init__(self, file_name: str):

        self.file_name = file_name

    def parse_json(self, gui):

        with open(self.file_name, "r") as file:
            body_configs = json.load(file)

        for index, body_config in enumerate(body_configs):

            body_tmp = Body(gui.body_counter, upper_panel=UpperPanel("", ""), 
                middle_panel=MiddlePanel(""), 
                lower_panel=LowerPanel("", "", ""),
                armrest=Armrest("", "", ""),
                cup_holder=CupHolder("", ""))

            body_tmp.upper_panel.is_controlable = body_config['body']['upper_panel']['is_controllable']
            body_tmp.upper_panel.type = body_config['body']['upper_panel']['type']

            body_tmp.middle_panel.functionality = body_config['body']['middle_panel']['functionality']

            body_tmp.lower_panel.functionality = body_config['body']['lower_panel']['functionality']
            body_tmp.lower_panel.is_cup = body_config['body']['lower_panel']['is_cup']
            body_tmp.lower_panel.color = body_config['body']['lower_panel']['color']

            body_tmp.armrest.heating = body_config['body']['armrest']['heating']
            body_tmp.armrest.material = body_config['body']['armrest']['material']
            body_tmp.armrest.color = body_config['body']['armrest']['color']

            body_tmp.cup_holder.usb_socket = body_config['body']['cup_holder']['usb_socket']
            body_tmp.cup_holder.color = body_config['body']['cup_holder']['color']

            gui.list_of_bodys.append(body_tmp)

            car_body_group_box = CarBodyGroupBox(gui.body_counter, body_tmp)
            # car_body_group_box.button_schedule.pressed.connect(gui.pb_schedule_clicked)
            car_body_group_box.button_ready.pressed.connect(gui.pb_ready_clicked)
            if gui.body_counter == 0:
                gui.outer_layout.removeWidget(gui.starting_label)
                gui.starting_label.deleteLater()
            gui.outer_layout.addWidget(car_body_group_box.group_box)
            gui.body_counter += 1

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.body_counter = 0
        self.list_of_threads = []
        self.list_of_radio_buttons = []

        self.list_of_bodys = []
        self.petri_net = cup_main_petri_net

        self.setWindowTitle("Tab Example")
        self.setGeometry(100, 100, 1300, 1000)

        central_widget = QFrame()
        central_widget.setStyleSheet(style_sheet_central_widget)
        layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        self.tabs.tabBar().setExpanding(True)
        self.tabs.setStyleSheet(style_sheet_tab)
        
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()
        self.tabs.addTab(self.tab1, "Dodaj korpus")
        self.tabs.addTab(self.tab2, "Stan korpusów")
        self.tabs.addTab(self.tab3, "Wykres Gantta")
        self.tabs.addTab(self.tab4, "Dodaj korpusy z pliku")

        self.create_tabs_content()
        layout.addWidget(self.tabs)
        self.setCentralWidget(central_widget)

        self.json_file_name = "bodys.json"

    def create_tabs_content(self):
        layout1 = QVBoxLayout()
        sub_tab_widget = QTabWidget()
        sub_tab_widget.setTabPosition(QTabWidget.West)
        sub_tab_widget.setStyleSheet(style_sheet_sub_tab)

        sub_tab1 = self.create_sub_tab_upper_panel_content()
        sub_tab2 = self.create_sub_tab_middle_panel_content()
        sub_tab3 = self.create_sub_tab_lower_panel_content()
        sub_tab4 = self.create_sub_tab_armrest_content()
        sub_tab5 = self.create_sub_tab_cup_holder_content()

        sub_tab_widget.addTab(sub_tab1, "Panel górny")
        sub_tab_widget.addTab(sub_tab2, "Panel środkowy")
        sub_tab_widget.addTab(sub_tab3, "Panel dolny")
        sub_tab_widget.addTab(sub_tab4, "Podłokietnik")
        sub_tab_widget.addTab(sub_tab5, "Miejsce na kubki")

        stacked_widget = QStackedWidget()
        stacked_widget.addWidget(sub_tab_widget)

        overlay_widget = QWidget()
        overlay_layout = QVBoxLayout(overlay_widget)
        overlay_layout.addWidget(stacked_widget)

        plus_button = AnimatedButton("+", 40, 40)
        plus_button.clicked.connect(self.pb_debug)

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

        layout4 = QVBoxLayout()
        read_from_file_button = AnimatedButton("Wczytaj")
        read_from_file_button.clicked.connect(self.pb_read_json)
        layout4.addWidget(read_from_file_button)
        self.tab4.setLayout(layout4)
    
    def create_sub_tab_upper_panel_content(self):

        sub_tab_upper_panel = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Parametry panelu górnego")
        label_material = QLabel("Sterowanie klimatyzacją")
        label_material.setStyleSheet(style_sheet_label)
        label_size = QLabel("Klimatyzacja")
        label_size.setStyleSheet(style_sheet_label)

        radio1 = QRadioButton("Tak")
        radio2 = QRadioButton("Nie")
        radio1.setStyleSheet(style_sheet_QRadioButton)
        radio2.setStyleSheet(style_sheet_QRadioButton)
        radio1.toggled.connect(self.on_radio_button_upper_panel_clicked)
        radio2.toggled.connect(self.on_radio_button_upper_panel_clicked)

        radio_groupbox1 = QGroupBox()
        radio_vboxlayout1 = QVBoxLayout()

        radio_vboxlayout1.addWidget(radio1)
        radio_vboxlayout1.addWidget(radio2)

        radio_groupbox1.setLayout(radio_vboxlayout1)

        radio_upac_4 = QRadioButton("4-strefowa")
        radio_upac_2 = QRadioButton("2-strefowa")
        radio_upac_4.setStyleSheet(style_sheet_QRadioButton)
        radio_upac_2.setStyleSheet(style_sheet_QRadioButton)
        radio_upac_4.toggled.connect(self.on_radio_button_upper_panel_clicked)
        radio_upac_2.toggled.connect(self.on_radio_button_upper_panel_clicked)

        self.list_of_radio_buttons.extend([radio1, radio2, radio_upac_4, radio_upac_2])

        radio_groupbox2 = QGroupBox()
        radio_vboxlayout2 = QVBoxLayout()

        radio_vboxlayout2.addWidget(radio_upac_4)
        radio_vboxlayout2.addWidget(radio_upac_2)

        radio_groupbox2.setLayout(radio_vboxlayout2)

        button_add_to_corpse = AnimatedButton("Dodaj")
        button_add_to_corpse.clicked.connect(self.pb_add_clicked)

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
        vbox_main.addWidget(button_add_to_corpse)

        group_box1.setLayout(vbox_main)

        sub_layout1.addWidget(group_box1)
        sub_tab_upper_panel.setLayout(sub_layout1)

        return sub_tab_upper_panel
    
    def create_sub_tab_middle_panel_content(self):

        sub_tab_middle_panel = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Parametry panelu środkowego")
        label_material = QLabel("Funkcjonalność")
        label_material.setStyleSheet(style_sheet_label)

        radio3 = QRadioButton("Interfejs multimedialny")
        radio4 = QRadioButton("Schowek")
        radio3.setStyleSheet(style_sheet_QRadioButton)
        radio4.setStyleSheet(style_sheet_QRadioButton)
        radio3.toggled.connect(self.on_radio_button_middle_panel_clicked)
        radio4.toggled.connect(self.on_radio_button_middle_panel_clicked)
        self.list_of_radio_buttons.extend([radio3, radio4])

        radio_groupbox1 = QGroupBox()
        radio_vboxlayout1 = QVBoxLayout()

        radio_vboxlayout1.addWidget(radio3)
        radio_vboxlayout1.addWidget(radio4)

        radio_groupbox1.setLayout(radio_vboxlayout1)

        button_add_to_corpse = AnimatedButton("Dodaj")
        button_add_to_corpse.clicked.connect(self.pb_add_clicked)

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
        sub_tab_middle_panel.setLayout(sub_layout1)

        return sub_tab_middle_panel    
    
    def create_sub_tab_lower_panel_content(self):

        sub_tab_lower_panel = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Parametry panelu dolnego")
        label_material = QLabel("Funkcjonalność")
        label_material.setStyleSheet(style_sheet_label)
        label_size = QLabel("Miejsce na kubek")
        label_size.setStyleSheet(style_sheet_label)

        radio5 = QRadioButton("Ładowarka bezprzewodowa")
        radio6 = QRadioButton("Półka")
        radio5.setStyleSheet(style_sheet_QRadioButton)
        radio6.setStyleSheet(style_sheet_QRadioButton)
        radio5.toggled.connect(self.on_radio_button_lower_panel_clicked)
        radio6.toggled.connect(self.on_radio_button_lower_panel_clicked)

        radio_groupbox1 = QGroupBox()
        radio_vboxlayout1 = QVBoxLayout()

        radio_vboxlayout1.addWidget(radio5)
        radio_vboxlayout1.addWidget(radio6)

        radio_groupbox1.setLayout(radio_vboxlayout1)

        radio7 = QRadioButton("Tak")
        radio8 = QRadioButton("Nie")
        radio7.setStyleSheet(style_sheet_QRadioButton)
        radio8.setStyleSheet(style_sheet_QRadioButton)
        radio7.toggled.connect(self.on_radio_button_lower_panel_clicked)
        radio8.toggled.connect(self.on_radio_button_lower_panel_clicked)

        radio_groupbox2 = QGroupBox()
        radio_vboxlayout2 = QVBoxLayout()

        radio_vboxlayout2.addWidget(radio7)
        radio_vboxlayout2.addWidget(radio8)

        self.list_of_radio_buttons.extend([radio5, radio6, radio7, radio8])

        radio_groupbox2.setLayout(radio_vboxlayout2)

        button_add_to_corpse = AnimatedButton("Dodaj")
        button_add_to_corpse.clicked.connect(self.pb_add_clicked)

        combo_box_color = QComboBox()
        combo_box_color.addItems(["Czerwony", "Zielony", "Niebieski"])
        combo_box_color.setStyleSheet(style_sheet_QComboBox)
        combo_box_color.currentIndexChanged.connect(self.on_change_cbox_lower_panel_color)
        combo_box_color.activated.connect(self.on_change_cbox_lower_panel_color)

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
        sub_tab_lower_panel.setLayout(sub_layout1)

        return sub_tab_lower_panel
    
    def create_sub_tab_armrest_content(self):

        sub_tab_armrest = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Parametry podłokietnika")
        label_heating = QLabel("Grzanie")
        label_heating.setStyleSheet(style_sheet_label)
        label_material = QLabel("Materiał")
        label_material.setStyleSheet(style_sheet_label)
        label_color = QLabel("Kolor")
        label_color.setStyleSheet(style_sheet_label)

        radio9 = QRadioButton("Tak")
        radio10 = QRadioButton("Nie")
        radio9.setStyleSheet(style_sheet_QRadioButton)
        radio10.setStyleSheet(style_sheet_QRadioButton)
        radio9.toggled.connect(self.on_radio_button_armrest_clicked)
        radio10.toggled.connect(self.on_radio_button_armrest_clicked)

        self.list_of_radio_buttons.extend([radio9, radio10])

        radio_groupbox1 = QGroupBox()
        radio_vboxlayout1 = QVBoxLayout()

        radio_vboxlayout1.addWidget(radio9)
        radio_vboxlayout1.addWidget(radio10)

        radio_groupbox1.setLayout(radio_vboxlayout1)

        combo_box_material = QComboBox()
        combo_box_material.addItems(["Skóra", "Eko skóra", "Sztuczna skóra"])
        combo_box_material.setStyleSheet(style_sheet_QComboBox)
        combo_box_material.currentIndexChanged.connect(self.on_change_cbox_armrest_material)
        combo_box_material.activated.connect(self.on_change_cbox_armrest_material)

        combo_box_color = QComboBox()
        combo_box_color.addItems(["Czerwony", "Zielony", "Niebieski"])
        combo_box_color.setStyleSheet(style_sheet_QComboBox)
        combo_box_color.currentIndexChanged.connect(self.on_change_cbox_armrest_color)
        combo_box_color.activated.connect(self.on_change_cbox_armrest_color)

        button_add_to_corpse = AnimatedButton("Dodaj")
        button_add_to_corpse.clicked.connect(self.pb_add_clicked)

        vbox_main = QVBoxLayout()
        vbox_sub1 = QVBoxLayout()
        vbox_sub2 = QVBoxLayout()

        vbox_sub1.addWidget(label_heating)
        vbox_sub1.addWidget(radio_groupbox1)
        vbox_sub1.setSpacing(5)

        vbox_sub2.addWidget(label_material)
        vbox_sub2.addWidget(combo_box_material)
        vbox_sub2.setSpacing(5)

        vbox_main.addLayout(vbox_sub1)
        vbox_main.addLayout(vbox_sub2)
        vbox_main.addWidget(label_color)
        vbox_main.addWidget(combo_box_color)
        vbox_main.addWidget(button_add_to_corpse)

        group_box1.setLayout(vbox_main)

        sub_layout1.addWidget(group_box1)
        sub_tab_armrest.setLayout(sub_layout1)

        return sub_tab_armrest
    
    def create_sub_tab_cup_holder_content(self):

        sub_tab_cup_holder = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Parametry miejsca na kubki")
        label_heating = QLabel("Wejście USB")
        label_heating.setStyleSheet(style_sheet_label)
        label_color = QLabel("Kolor")
        label_color.setStyleSheet(style_sheet_label)

        radio11 = QRadioButton("Tak")
        radio12 = QRadioButton("Nie")
        radio11.setStyleSheet(style_sheet_QRadioButton)
        radio12.setStyleSheet(style_sheet_QRadioButton)
        radio11.toggled.connect(self.on_radio_button_cup_holder_clicked)
        radio12.toggled.connect(self.on_radio_button_cup_holder_clicked)

        radio_groupbox1 = QGroupBox()
        radio_vboxlayout1 = QVBoxLayout()

        radio_vboxlayout1.addWidget(radio11)
        radio_vboxlayout1.addWidget(radio12)

        self.list_of_radio_buttons.extend([radio11, radio12])

        radio_groupbox1.setLayout(radio_vboxlayout1)

        combo_box_color = QComboBox()
        combo_box_color.addItems(["Czerwony", "Zielony", "Niebieski"])
        combo_box_color.setStyleSheet(style_sheet_QComboBox)
        combo_box_color.currentIndexChanged.connect(self.on_change_cbox_cup_holder_color)
        combo_box_color.activated.connect(self.on_change_cbox_cup_holder_color)

        button_add_to_corpse = AnimatedButton("Dodaj")
        button_add_to_corpse.clicked.connect(self.pb_add_clicked)

        vbox_main = QVBoxLayout()
        vbox_sub1 = QVBoxLayout()
        vbox_sub2 = QVBoxLayout()

        vbox_sub1.addWidget(label_heating)
        vbox_sub1.addWidget(radio_groupbox1)
        vbox_sub1.setSpacing(5)

        vbox_main.addLayout(vbox_sub1)
        vbox_main.addLayout(vbox_sub2)
        vbox_main.addWidget(label_color)
        vbox_main.addWidget(combo_box_color)
        vbox_main.addWidget(button_add_to_corpse)

        group_box1.setLayout(vbox_main)

        sub_layout1.addWidget(group_box1)
        sub_tab_cup_holder.setLayout(sub_layout1)

        return sub_tab_cup_holder
    
    def create_group_box_body(self):
        self.car_body_group_box = CarBodyGroupBox(self.body_counter, self.list_of_bodys[self.body_counter - 1])
        # self.car_body_group_box.button_schedule.pressed.connect(self.pb_schedule_clicked)
        self.car_body_group_box.button_ready.pressed.connect(self.pb_ready_clicked)

    def update_bodys_list_size(self):
        if len(self.list_of_bodys) == 0:
            body_tmp = Body(self.body_counter, upper_panel=UpperPanel("", ""), 
                middle_panel=MiddlePanel(""), 
                lower_panel=LowerPanel("", "", ""),
                armrest=Armrest("", "", ""),
                cup_holder=CupHolder("", ""))
            self.list_of_bodys.append(body_tmp)
            self.body_counter += 1
        # if len(self.list_of_bodys) < self.body_counter:
        #     body_tmp = Body(self.body_counter - 1, upper_panel=UpperPanel("", ""), 
        #         middle_panel=MiddlePanel(""), 
        #         lower_panel=LowerPanel("", "", ""),
        #         armrest=Armrest("", "", ""),
        #         cup_holder=CupHolder("", ""))
        #     self.list_of_bodys.append(body_tmp)

    def on_change_cbox_lower_panel_color(self, index):
        # print(f"Selected size index: {index}")
        self.update_bodys_list_size()

        if index == 0:
            self.list_of_bodys[self.body_counter - 1].lower_panel.color = "Czerwony"
        elif index == 1:
            self.list_of_bodys[self.body_counter - 1].lower_panel.color = "Zielony"
        elif index == 2:
            self.list_of_bodys[self.body_counter - 1].lower_panel.color = "Niebieski"
    
    def on_change_cbox_armrest_material(self, index):
        # print(f"Selected size index: {index}")
        self.update_bodys_list_size()

        if index == 0:
            self.list_of_bodys[self.body_counter - 1].armrest.material = "Skóra"
        elif index == 1:
            self.list_of_bodys[self.body_counter - 1].armrest.material = "Eko skóra"
        elif index == 2:
            self.list_of_bodys[self.body_counter - 1].armrest.material = "Sztuczna skóra"

    def on_change_cbox_armrest_color(self, index):
        # print(f"Selected size index: {index}")
        self.update_bodys_list_size()

        if index == 0:
            self.list_of_bodys[self.body_counter - 1].armrest.color = "Czerwony"
        elif index == 1:
            self.list_of_bodys[self.body_counter - 1].armrest.color = "Zielony"
        elif index == 2:
            self.list_of_bodys[self.body_counter - 1].armrest.color = "Niebieski"

    def on_change_cbox_cup_holder_color(self, index):
        # print(f"Selected size index: {index}")
        self.update_bodys_list_size()

        if index == 0:
            self.list_of_bodys[self.body_counter - 1].cup_holder.color = "Czerwony"
        elif index == 1:
            self.list_of_bodys[self.body_counter - 1].cup_holder.color = "Zielony"
        elif index == 2:
            self.list_of_bodys[self.body_counter - 1].cup_holder.color = "Niebieski"

    def on_radio_button_upper_panel_clicked(self):
        self.update_bodys_list_size()

        sender = self.sender()

        if sender.isChecked():
            if (sender.text() == "Tak" or sender.text() == "Nie"):
                self.list_of_bodys[self.body_counter - 1].upper_panel.is_controlable = sender.text()
                pass
            else:
                self.list_of_bodys[self.body_counter - 1].upper_panel.type = sender.text()
            print(f'Selected option: {sender.text()}')

    def on_radio_button_middle_panel_clicked(self):
        self.update_bodys_list_size()

        sender = self.sender()

        if sender.isChecked():
            self.list_of_bodys[self.body_counter - 1].middle_panel.functionality = sender.text()
            print(f'Selected option: {sender.text()}')

    def on_radio_button_lower_panel_clicked(self):
        self.update_bodys_list_size()

        sender = self.sender()

        if sender.isChecked():
            if (sender.text() == "Tak" or sender.text() == "Nie"):
                self.list_of_bodys[self.body_counter - 1].lower_panel.is_cup = sender.text()
                pass
            else:
                self.list_of_bodys[self.body_counter - 1].lower_panel.functionality = sender.text()
            print(f'Selected option: {sender.text()}')

    def on_radio_button_armrest_clicked(self):
        self.update_bodys_list_size()

        sender = self.sender()

        if sender.isChecked():
            self.list_of_bodys[self.body_counter - 1].armrest.heating = sender.text()
        print(f'Selected option: {sender.text()}')

    def on_radio_button_cup_holder_clicked(self):
        self.update_bodys_list_size()

        sender = self.sender()

        if sender.isChecked():
            self.list_of_bodys[self.body_counter - 1].cup_holder.usb_socket = sender.text()
        print(f'Selected option: {sender.text()}')

    def pb_add_clicked(self):

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

    def pb_read_json(self):
        self.json_reader = ReadJSON(self.json_file_name)
        self.json_reader.parse_json(self)
        # for body in self.list_of_bodys:
        #     print(body)

    # def pb_debug(self):
    #     for body in self.list_of_bodys:
    #         print(body)

    def pb_debug(self):
        # self.update_bodys_list_size()
        for body in self.list_of_bodys:
            print(body)

    
    @pyqtSlot()
    def pb_schedule_clicked(self):
        print(f"\nScheduled body nr: {self.body_counter}")

        new_petri_net_thread = PetriNetThread(self.body_counter, self.body, self.mpl_widget)
        new_petri_net_thread.finished_signal.connect(self.on_thread_finished)
        self.list_of_threads.append(new_petri_net_thread)
        # self.petri_net_thread.start()
        self.list_of_threads[self.body_counter - 1].start()

        self.body.remove_parameters()
        self.car_body_group_box.button_schedule.setEnabled(False)

        self.body_counter += 1

    @pyqtSlot()
    def pb_ready_clicked(self):
        print("Przycisk gotowe wcisniety")
        print(len(self.list_of_bodys))
        self.list_of_bodys.append(Body(self.body_counter,
                upper_panel=UpperPanel("", ""), 
                middle_panel=MiddlePanel(""), 
                lower_panel=LowerPanel("", "", ""),
                armrest=Armrest("", "", ""),
                cup_holder=CupHolder("", "")))
        self.body_counter += 1
        self.reset_radio_buttons()
        # self.car_body_group_box.button_ready.setEnabled(False)

    @pyqtSlot(int)
    def on_thread_finished(self, thread_id):
        print(f"Thread {thread_id} has finished.")

    def reset_radio_buttons(self):
        for radio in self.list_of_radio_buttons:
            radio.setAutoExclusive(False)
            radio.setChecked(False)
            radio.setAutoExclusive(True)

def main():
    app = QApplication([])
    app.setStyleSheet(style_sheet_app)
    window = GUI()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
