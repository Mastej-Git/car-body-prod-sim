import os

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
                          pyqtSlot,)

from body_parts.Framework import Framework
from body_parts.UpperPanel import UpperPanel
from body_parts.MiddlePanel import MiddlePanel
from body_parts.LowerPanel import LowerPanel
from body_parts.Armrest import Armrest
from body_parts.CupHolder import CupHolder
from Body import Body

from petri_nets.PetriNetThread import PetriNetThread

from other.MatPlotlibWidget import MatplotlibWidget, PlotWidget
from other.ReadJSON import ReadJSON
from other.FileDialog import FileDialog

from qt_classes.AnimatedButton import AnimatedButton
from qt_classes.CarBodyGroupBox import CarBodyGroupBox

from other.StyleSheets import (
    style_sheet_app,
    style_sheet_central_widget,
    style_sheet_label,
    style_sheet_QComboBox,
    style_sheet_QRadioButton,
    style_sheet_sub_tab,
    style_sheet_tab,
)

from BodyPetriNet import body_main_petri_net

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.body_counter = 0
        self.body_tmp = Body(self.body_counter,
                             framework=Framework("", ""),
                             upper_panel=UpperPanel("", ""),
                             middle_panel=MiddlePanel(""),
                             lower_panel=LowerPanel("", "", ""),
                             armrest=Armrest("", "", ""),
                             cup_holder=CupHolder("", "")
                            )
        
        self.list_of_threads = []
        self.list_of_radio_buttons = []
        self.list_of_car_body_group_box = []
        self.list_of_bodys = []

        self.petri_net = body_main_petri_net
        self.json_file_name = [""]

        self.json_reader = ReadJSON(self.json_file_name)
        self.file_dialog = None
        
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

    def create_tabs_content(self):
        layout1 = QVBoxLayout()
        sub_tab_widget = QTabWidget()
        sub_tab_widget.setTabPosition(QTabWidget.West)
        sub_tab_widget.setStyleSheet(style_sheet_sub_tab)

        sub_tab0 = self.create_sub_tab_framework_content()
        sub_tab1 = self.create_sub_tab_upper_panel_content()
        sub_tab2 = self.create_sub_tab_middle_panel_content()
        sub_tab3 = self.create_sub_tab_lower_panel_content()
        sub_tab4 = self.create_sub_tab_armrest_content()
        sub_tab5 = self.create_sub_tab_cup_holder_content()

        sub_tab_widget.addTab(sub_tab0, "Szkielet")
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

        button_layout = QHBoxLayout()
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

        # self.mpl_widget = MatplotlibWidget(self.petri_net, self)
        self.mpl_widget = PlotWidget(self.petri_net)

        layout3 = QVBoxLayout()
        layout3.addWidget(self.mpl_widget)
        # self.mpl_widget.plot()
        self.tab3.setLayout(layout3)

        layout4 = QVBoxLayout()

        group_box = QGroupBox("Wczytaj konfigurację")
        group_box.setFixedHeight(200)

        label = QLabel("No file selected")

        hbox_layout = QHBoxLayout()
        vbox_layout = QVBoxLayout()

        read_file_button = AnimatedButton("Wczytaj")
        read_file_button.clicked.connect(self.pb_read_json)

        self.file_dialog = FileDialog(self.json_file_name, label)

        chose_file_button = AnimatedButton("Wybierz plik")
        chose_file_button.clicked.connect(self.pb_chose_file)

        vbox_layout.addWidget(chose_file_button)
        vbox_layout.addWidget(read_file_button)

        hbox_layout.addWidget(label)
        hbox_layout.addLayout(vbox_layout)

        group_box.setLayout(hbox_layout)

        layout4.addWidget(group_box)
        self.tab4.setLayout(layout4)

    def create_sub_tab_framework_content(self):

        sub_tab_upper_panel = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Parametry szkieletu")
        label_material = self.create_label("Materiał")
        label_color = self.create_label("Kolor")

        button_add_to_body = AnimatedButton("Dodaj do korpusu")
        button_add_to_body.clicked.connect(self.pb_add_clicked)
        button_add_body = AnimatedButton("Dodaj korpus")
        button_add_body.clicked.connect(self.pb_add_body)

        combo_box_material = self.create_combo_box(["Skóra", "Eko skóra", "Sztuczna skóra"], self.on_change_cbox_framework_material)
        combo_box_color = self.create_combo_box(["Czerwony", "Zielony", "Niebieski"], self.on_change_cbox_framework_color)

        vbox_main = QVBoxLayout()
        vbox_sub1 = QVBoxLayout()
        vbox_sub2 = QVBoxLayout()

        vbox_sub1.addWidget(label_material)
        vbox_sub1.addWidget(combo_box_material)
        vbox_sub1.setSpacing(500)

        vbox_sub2.addWidget(label_color)
        vbox_sub2.addWidget(combo_box_color)
        vbox_sub2.setSpacing(5)

        vbox_main.addLayout(vbox_sub1)
        vbox_main.addLayout(vbox_sub2)
        vbox_main.addWidget(button_add_to_body)
        vbox_main.addWidget(button_add_body)

        group_box1.setLayout(vbox_main)

        sub_layout1.addWidget(group_box1)
        sub_tab_upper_panel.setLayout(sub_layout1)

        return sub_tab_upper_panel
    
    def create_sub_tab_upper_panel_content(self):

        sub_tab_upper_panel = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Parametry panelu górnego")
        label_material = self.create_label("Sterowanie klimatyzacją")
        label_size = self.create_label("Rodzaj klimatyzacji")

        radio1 = self.create_radio_button("Tak", self.on_radio_button_upper_panel_clicked)
        radio2 = self.create_radio_button("Nie", self.on_radio_button_upper_panel_clicked)

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

        button_add_to_body = AnimatedButton("Dodaj do korpusu")
        button_add_to_body.clicked.connect(self.pb_add_clicked)
        button_add_body = AnimatedButton("Dodaj korpus")
        button_add_body.clicked.connect(self.pb_add_body)

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
        vbox_main.addWidget(button_add_to_body)
        vbox_main.addWidget(button_add_body)

        group_box1.setLayout(vbox_main)

        sub_layout1.addWidget(group_box1)
        sub_tab_upper_panel.setLayout(sub_layout1)

        return sub_tab_upper_panel
    
    def create_sub_tab_middle_panel_content(self):

        sub_tab_middle_panel = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Parametry panelu środkowego")
        label_functionality = self.create_label("Funkcjonalność")

        radio3 = self.create_radio_button("Interfejs multimedialny", self.on_radio_button_middle_panel_clicked)
        radio4 = self.create_radio_button("Schowek", self.on_radio_button_middle_panel_clicked)
        self.list_of_radio_buttons.extend([radio3, radio4])

        radio_groupbox1 = QGroupBox()
        radio_vboxlayout1 = QVBoxLayout()

        radio_vboxlayout1.addWidget(radio3)
        radio_vboxlayout1.addWidget(radio4)

        radio_groupbox1.setLayout(radio_vboxlayout1)

        button_add_to_body = AnimatedButton("Dodaj do korpusu")
        button_add_to_body.clicked.connect(self.pb_add_clicked)
        button_add_body = AnimatedButton("Dodaj korpus")
        button_add_body.clicked.connect(self.pb_add_body)

        vbox_main = QVBoxLayout()
        vbox_sub1 = QVBoxLayout()
        vbox_sub2 = QVBoxLayout()

        vbox_sub1.addWidget(label_functionality)
        vbox_sub1.addWidget(radio_groupbox1)
        vbox_sub1.setSpacing(5)

        vbox_main.addLayout(vbox_sub1)
        vbox_main.addLayout(vbox_sub2)
        vbox_main.addWidget(button_add_to_body)
        vbox_main.addWidget(button_add_body)

        group_box1.setLayout(vbox_main)

        sub_layout1.addWidget(group_box1)
        sub_tab_middle_panel.setLayout(sub_layout1)

        return sub_tab_middle_panel    
    
    def create_sub_tab_lower_panel_content(self):

        sub_tab_lower_panel = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Parametry panelu dolnego")
        label_functionality = self.create_label("Funkcjonalność")
        label_cup_place = self.create_label("Miejsce na kubek")
        label_color = self.create_label("Kolor")

        radio5 = self.create_radio_button("Ładowarka bezprzewodowa", self.on_radio_button_lower_panel_clicked)
        radio6 = self.create_radio_button("Półka", self.on_radio_button_lower_panel_clicked)

        radio_groupbox1 = QGroupBox()
        radio_vboxlayout1 = QVBoxLayout()

        radio_vboxlayout1.addWidget(radio5)
        radio_vboxlayout1.addWidget(radio6)

        radio_groupbox1.setLayout(radio_vboxlayout1)

        radio7 = self.create_radio_button("Tak", self.on_radio_button_lower_panel_clicked)
        radio8 = self.create_radio_button("Nie", self.on_radio_button_lower_panel_clicked)

        radio_groupbox2 = QGroupBox()
        radio_vboxlayout2 = QVBoxLayout()

        radio_vboxlayout2.addWidget(radio7)
        radio_vboxlayout2.addWidget(radio8)

        self.list_of_radio_buttons.extend([radio5, radio6, radio7, radio8])

        radio_groupbox2.setLayout(radio_vboxlayout2)

        button_add_to_body = AnimatedButton("Dodaj do korpusu")
        button_add_to_body.clicked.connect(self.pb_add_clicked)
        button_add_body = AnimatedButton("Dodaj korpus")
        button_add_body.clicked.connect(self.pb_add_body)

        combo_box_color = self.create_combo_box(["Czerwony", "Zielony", "Niebieski"], self.on_change_cbox_lower_panel_color)

        vbox_main = QVBoxLayout()
        vbox_sub1 = QVBoxLayout()
        vbox_sub2 = QVBoxLayout()

        vbox_sub1.addWidget(label_functionality)
        vbox_sub1.addWidget(radio_groupbox1)
        vbox_sub1.setSpacing(5)

        vbox_sub2.addWidget(label_cup_place)
        vbox_sub2.addWidget(radio_groupbox2)
        vbox_sub2.setSpacing(5)

        vbox_main.addLayout(vbox_sub1)
        vbox_main.addLayout(vbox_sub2)
        vbox_main.addWidget(label_color)
        vbox_main.addWidget(combo_box_color)
        vbox_main.addWidget(button_add_to_body)
        vbox_main.addWidget(button_add_body)

        group_box1.setLayout(vbox_main)

        sub_layout1.addWidget(group_box1)
        sub_tab_lower_panel.setLayout(sub_layout1)

        return sub_tab_lower_panel
    
    def create_sub_tab_armrest_content(self):

        sub_tab_armrest = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Parametry podłokietnika")
        label_heating = self.create_label("Grzanie")
        label_material = self.create_label("Materiał")
        label_color = self.create_label("Kolor")

        radio9 = self.create_radio_button("Tak", self.on_radio_button_armrest_clicked)
        radio10 = self.create_radio_button("Nie", self.on_radio_button_armrest_clicked)
        self.list_of_radio_buttons.extend([radio9, radio10])

        radio_groupbox1 = QGroupBox()
        radio_vboxlayout1 = QVBoxLayout()

        radio_vboxlayout1.addWidget(radio9)
        radio_vboxlayout1.addWidget(radio10)

        radio_groupbox1.setLayout(radio_vboxlayout1)

        combo_box_material = self.create_combo_box(["Skóra", "Eko skóra", "Sztuczna skóra"], self.on_change_cbox_armrest_material)
        combo_box_color = self.create_combo_box(["Czerwony", "Zielony", "Niebieski"], self.on_change_cbox_armrest_color)

        button_add_to_body = AnimatedButton("Dodaj do korpusu")
        button_add_to_body.clicked.connect(self.pb_add_clicked)
        button_add_body = AnimatedButton("Dodaj korpus")
        button_add_body.clicked.connect(self.pb_add_body)

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
        vbox_main.addWidget(button_add_to_body)
        vbox_main.addWidget(button_add_body)

        group_box1.setLayout(vbox_main)

        sub_layout1.addWidget(group_box1)
        sub_tab_armrest.setLayout(sub_layout1)

        return sub_tab_armrest
    
    def create_sub_tab_cup_holder_content(self):

        sub_tab_cup_holder = QWidget()

        sub_layout1 = QVBoxLayout()

        group_box1 = QGroupBox("Parametry miejsca na kubki")
        label_usb_socket = self.create_label("Wejście USB")
        label_color = self.create_label("Kolor")

        radio11 = self.create_radio_button("Tak", self.on_radio_button_cup_holder_clicked)
        radio12 = self.create_radio_button("Nie", self.on_radio_button_cup_holder_clicked)

        radio_groupbox1 = QGroupBox()
        radio_vboxlayout1 = QVBoxLayout()

        radio_vboxlayout1.addWidget(radio11)
        radio_vboxlayout1.addWidget(radio12)

        self.list_of_radio_buttons.extend([radio11, radio12])

        radio_groupbox1.setLayout(radio_vboxlayout1)

        combo_box_color = self.create_combo_box(["Czerwony", "Zielony", "Niebieski"], self.on_change_cbox_cup_holder_color)

        button_add_to_body = AnimatedButton("Dodaj do korpusu")
        button_add_to_body.clicked.connect(self.pb_add_clicked)
        button_add_body = AnimatedButton("Dodaj korpus")
        button_add_body.clicked.connect(self.pb_add_body)

        vbox_main = QVBoxLayout()
        vbox_sub1 = QVBoxLayout()
        vbox_sub2 = QVBoxLayout()

        vbox_sub1.addWidget(label_usb_socket)
        vbox_sub1.addWidget(radio_groupbox1)
        vbox_sub1.setSpacing(5)

        vbox_main.addLayout(vbox_sub1)
        vbox_main.addLayout(vbox_sub2)
        vbox_main.addWidget(label_color)
        vbox_main.addWidget(combo_box_color)
        vbox_main.addWidget(button_add_to_body)
        vbox_main.addWidget(button_add_body)

        group_box1.setLayout(vbox_main)

        sub_layout1.addWidget(group_box1)
        sub_tab_cup_holder.setLayout(sub_layout1)

        return sub_tab_cup_holder
    
    def create_group_box_body(self):
        self.list_of_car_body_group_box.append(CarBodyGroupBox(self.list_of_bodys[self.body_counter - 1]))

        self.list_of_car_body_group_box[self.body_counter - 1].button_schedule.clicked.connect(
            lambda _, x=self.list_of_car_body_group_box[self.body_counter - 1].body.body_id: self.pb_schedule_clicked(x))
        
        self.list_of_car_body_group_box[self.body_counter - 1].button_ready.clicked.connect(
            lambda _, x=self.list_of_car_body_group_box[self.body_counter - 1].body.body_id: self.pb_ready_clicked(x))
        
        self.list_of_car_body_group_box[self.body_counter - 1].button_remove.clicked.connect(
            lambda _, x=self.list_of_car_body_group_box[self.body_counter - 1].body.body_id: self.pb_delete_clicked(x))
        
    def on_change_cbox_framework_material(self, index):
        if index == 0:
            self.body_tmp.framework.material = "Skóra"
        elif index == 1:
            self.body_tmp.framework.material = "Eko skóra"
        elif index == 2:
            self.body_tmp.framework.material = "Sztuczna skóra"

    def on_change_cbox_framework_color(self, index):

        if index == 0:
            self.body_tmp.framework.color = "Czerwony"
        elif index == 1:
            self.body_tmp.framework.color = "Zielony"
        elif index == 2:
            self.body_tmp.framework.color = "Niebieski"

    def on_change_cbox_lower_panel_color(self, index):

        if index == 0:
            self.body_tmp.lower_panel.color = "Czerwony"
        elif index == 1:
            self.body_tmp.lower_panel.color = "Zielony"
        elif index == 2:
            self.body_tmp.lower_panel.color = "Niebieski"
    
    def on_change_cbox_armrest_material(self, index):

        if index == 0:
            self.body_tmp.armrest.material = "Skóra"
        elif index == 1:
            self.body_tmp.armrest.material = "Eko skóra"
        elif index == 2:
            self.body_tmp.armrest.material = "Sztuczna skóra"

    def on_change_cbox_armrest_color(self, index):

        if index == 0:
            self.body_tmp.armrest.color = "Czerwony"
        elif index == 1:
            self.body_tmp.armrest.color = "Zielony"
        elif index == 2:
            self.body_tmp.armrest.color = "Niebieski"

    def on_change_cbox_cup_holder_color(self, index):

        if index == 0:
            self.body_tmp.cup_holder.color = "Czerwony"
        elif index == 1:
            self.body_tmp.cup_holder.color = "Zielony"
        elif index == 2:
            self.body_tmp.cup_holder.color = "Niebieski"

    def on_radio_button_upper_panel_clicked(self):

        sender = self.sender()

        if sender.isChecked():
            if (sender.text() == "Tak" or sender.text() == "Nie"):
                self.body_tmp.upper_panel.is_controlable = sender.text()
            else:
                self.body_tmp.upper_panel.ac_type = sender.text()
            print(f'Selected option: {sender.text()}')

    def on_radio_button_middle_panel_clicked(self):

        sender = self.sender()

        if sender.isChecked():
            self.body_tmp.middle_panel.functionality = sender.text()
            print(f'Selected option: {sender.text()}')

    def on_radio_button_lower_panel_clicked(self):

        sender = self.sender()

        if sender.isChecked():
            if (sender.text() == "Tak" or sender.text() == "Nie"):
                self.body_tmp.lower_panel.is_cup = sender.text()
            else:
                self.body_tmp.lower_panel.functionality = sender.text()
            print(f'Selected option: {sender.text()}')

    def on_radio_button_armrest_clicked(self):

        sender = self.sender()

        if sender.isChecked():
            self.body_tmp.armrest.heating = sender.text()
        print(f'Selected option: {sender.text()}')

    def on_radio_button_cup_holder_clicked(self):

        sender = self.sender()

        if sender.isChecked():
            self.body_tmp.cup_holder.usb_socket = sender.text()
        print(f'Selected option: {sender.text()}')

    def pb_add_clicked(self):

        self.body_tmp.id = self.body_counter - 1
        self.list_of_bodys[self.body_counter - 1] = self.body_tmp
        self.list_of_car_body_group_box[self.body_counter - 1].recreate_label()
        self.outer_layout.removeWidget(self.outer_layout.itemAt(self.body_counter - 1).widget())
            
        self.outer_layout.addWidget(self.list_of_car_body_group_box[self.body_counter - 1].group_box)

    def pb_read_json(self):
        self.json_reader.parse_json(self)

    def pb_chose_file(self):
        self.file_dialog.show_file_dialog()

    def pb_add_body(self):
        if self.body_counter == 0:
            self.outer_layout.removeWidget(self.starting_label)
            self.starting_label.deleteLater()

        self.body_counter += 1
        self.body_tmp.id = self.body_counter - 1

        self.body_tmp.remove_parameters()
        self.reset_radio_buttons()

        self.list_of_bodys.append(self.body_tmp)
        self.create_group_box_body()
        self.list_of_car_body_group_box[self.body_counter - 1].group_box.setMinimumWidth(738)

        self.outer_layout.addWidget(self.list_of_car_body_group_box[self.body_counter - 1].group_box)
    
    @pyqtSlot()
    def pb_schedule_clicked(self, body_id):
        print(f"\nID: {body_id} - Rozpoczęto produkcję korpusu.")

        new_petri_net_thread = PetriNetThread(self.list_of_bodys[body_id])
        new_petri_net_thread.finished_signal.connect(self.on_thread_finished)
        self.list_of_threads.append(new_petri_net_thread)
        # self.petri_net_thread.start()
        self.list_of_threads[len(self.list_of_threads) - 1].start()

        self.list_of_car_body_group_box[body_id].button_schedule.setEnabled(False)

    @pyqtSlot()
    def pb_ready_clicked(self, body_id):
        print(f"\nKorpus ID: {body_id} gotowy do produkcji")
        
        self.body_counter += 1
        self.reset_radio_buttons()
        self.body_tmp.remove_parameters()
        self.list_of_car_body_group_box[body_id].button_ready.setEnabled(False)

    @pyqtSlot()
    def pb_delete_clicked(self, body_id):
        print(f"Korpus ID: {body_id} został usunięty")

        index_remove = -1
        i = 0

        for body in self.list_of_bodys:
            if body.body_id == body_id:
                index_remove = i
            i += 1
        
        self.list_of_bodys.pop(index_remove)
        self.outer_layout.removeWidget(self.list_of_car_body_group_box[index_remove].group_box)
        self.list_of_car_body_group_box.pop(index_remove)        
        self.body_counter -= 1

        self.reset_radio_buttons()
        self.body_tmp.remove_parameters()
        self.check_body_group_box_number()

    @pyqtSlot(int)
    def on_thread_finished(self, thread_id):
        print(f"Thread {thread_id} has finished.")

    def reset_radio_buttons(self):
        for radio in self.list_of_radio_buttons:
            radio.setAutoExclusive(False)
            radio.setChecked(False)
            radio.setAutoExclusive(True)

    def check_body_group_box_number(self):
        if self.body_counter == 0 and len(self.list_of_car_body_group_box) == 0:
            self.starting_label = QLabel("Brak korpusów w produkcji")
            self.starting_label.setStyleSheet(style_sheet_label)
            self.starting_label.setAlignment(Qt.AlignCenter)
            self.outer_layout.addWidget(self.starting_label)

    def create_label(self, label_str: str, maximuxm_height=70):
        label = QLabel(label_str)
        label.setStyleSheet(style_sheet_label)
        label.setMaximumHeight(maximuxm_height)

        return label
    
    def create_radio_button(self, label_str: str, signal_function):
        radio_button = QRadioButton(label_str)
        radio_button.setStyleSheet(style_sheet_QRadioButton)
        radio_button.toggled.connect(signal_function)

        return radio_button
    
    def create_combo_box(self, list_of_elements: list, signal_function):
        combo_box = QComboBox()
        combo_box.addItems(list_of_elements)
        combo_box.setStyleSheet(style_sheet_QComboBox)
        combo_box.currentIndexChanged.connect(signal_function)
        combo_box.activated.connect(signal_function)

        return combo_box

def main():
    app = QApplication([])
    app.setStyleSheet(style_sheet_app)
    window = GUI()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
