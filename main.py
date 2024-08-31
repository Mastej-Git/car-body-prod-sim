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
from PyQt5.QtCore import Qt, pyqtSlot, QMutex

from Body import Body
from body_parts.UpperPanel import UpperPanel
from body_parts.MiddlePanel import MiddlePanel
from body_parts.LowerPanel import LowerPanel
from body_parts.Armrest import Armrest
from body_parts.CupHolder import CupHolder

from petri_nets.PetriNetThread import PetriNetThread

from other.MatPlotlibWidget import MatplotlibWidget

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

def create_push_button(name, size_x, size_y):
        button = QPushButton(name)
        button.setStyleSheet(style_sheet_QPushButton)
        button.setFixedSize(size_x, size_y)

        return button

class CarBodyGroupBox():

    def __init__(self, body: Body) -> None:
        
        self.group_box = QGroupBox()
        self.body = body

        label_text = self.create_label()

        label = QLabel(label_text)
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        label.setStyleSheet(style_sheet_label)

        self.button_schedule = create_push_button("Schedule", 200, 40)
        self.button_remove = create_push_button("Remove", 200, 40)
        self.button_edit = create_push_button("Edit", 200, 40)

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

        if self.body.upper_panel.is_activated is True:
            label += f"▸  Panel gorny:\n\t ▪ Sterowanie klimatyzacja: {self.body.upper_panel.is_controlable}\n\t ▪ Typ: {self.body.upper_panel.type}\n"
        if self.body.middle_panel.is_activated is True:
            label += f"▸  Panel środkowy:\n\t ▪ Funkcjonalność: {self.body.middle_panel.functionality}\n"
        if self.body.lower_panel.is_activated is True:
            label += (f"▸  Panel dolny:\n\t ▪ Funkcjonalność: {self.body.lower_panel.functionality}\n\t "
                      f"▪ Chwytaki na kubki: {self.body.lower_panel.is_cup}\n\t" 
                      f" ▪ Kolor: {self.body.lower_panel.color}\n")
        if self.body.armrest.is_activated is True:
            label += (f"▸  Podłokietnik:\n\t ▪ Podgrzewanie: {self.body.armrest.heating}\n\t "
                      f"▪ Materiał: {self.body.armrest.material}\n\t" 
                      f" ▪ Kolor: {self.body.armrest.color}\n")
        if self.body.cup_holder.is_activated is True:
            label += f"▸  Miejsce na kubki:\n\t ▪ Wejście USB: {self.body.cup_holder.usb_socket}\n\t ▪ Kolor: {self.body.cup_holder.color}\n"

        return label

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.body_counter = 0
        self.list_of_threads = []

        self.body = Body(UpperPanel("", ""),
                         MiddlePanel(""),
                         LowerPanel("", "", ""),
                         Armrest("", "", ""),
                         CupHolder("", ""))
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

        self.gowno = 1

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
        button_add_to_corpse.clicked.connect(self.pb_add_clicked)

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
        sub_tab_upper_panel.setLayout(sub_layout1)

        return sub_tab_upper_panel
    
    def create_sub_tab_middle_panel_content(self):

        sub_tab_middle_panel = QWidget()

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

        radio1 = QRadioButton("Tak")
        radio2 = QRadioButton("Nie")
        radio1.toggled.connect(self.on_radio_button_armrest_clicked)
        radio2.toggled.connect(self.on_radio_button_armrest_clicked)

        radio_groupbox1 = QGroupBox()
        radio_vboxlayout1 = QVBoxLayout()

        radio_vboxlayout1.addWidget(radio1)
        radio_vboxlayout1.addWidget(radio2)

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

        button_add_to_corpse = QPushButton("Dodaj")
        button_add_to_corpse.setStyleSheet(style_sheet_QPushButton)
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

        radio1 = QRadioButton("Tak")
        radio2 = QRadioButton("Nie")
        radio1.toggled.connect(self.on_radio_button_cup_holder_clicked)
        radio2.toggled.connect(self.on_radio_button_cup_holder_clicked)

        radio_groupbox1 = QGroupBox()
        radio_vboxlayout1 = QVBoxLayout()

        radio_vboxlayout1.addWidget(radio1)
        radio_vboxlayout1.addWidget(radio2)

        radio_groupbox1.setLayout(radio_vboxlayout1)

        combo_box_color = QComboBox()
        combo_box_color.addItems(["Czerwony", "Zielony", "Niebieski"])
        combo_box_color.setStyleSheet(style_sheet_QComboBox)
        combo_box_color.currentIndexChanged.connect(self.on_change_cbox_cup_holder_color)
        combo_box_color.activated.connect(self.on_change_cbox_cup_holder_color)

        button_add_to_corpse = QPushButton("Dodaj")
        button_add_to_corpse.setStyleSheet(style_sheet_QPushButton)
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
        self.car_body_group_box = CarBodyGroupBox(self.body)
        self.car_body_group_box.button_schedule.pressed.connect(self.on_schedule_clicked)

    def on_change_cbox_lower_panel_color(self, index):
        # print(f"Selected size index: {index}")
        if index == 0:
            self.body.lower_panel.color = "Czerwony"
        elif index == 1:
            self.body.lower_panel.color = "Zielony"
        elif index == 2:
            self.body.lower_panel.color = "Niebieski"
        self.body.lower_panel.check_activation()
    
    def on_change_cbox_armrest_material(self, index):
        # print(f"Selected size index: {index}")
        if index == 0:
            self.body.armrest.material = "Skóra"
        elif index == 1:
            self.body.armrest.material = "Eko skóra"
        elif index == 2:
            self.body.armrest.material = "Sztuczna skóra"
        self.body.armrest.check_activation()

    def on_change_cbox_armrest_color(self, index):
        # print(f"Selected size index: {index}")
        if index == 0:
            self.body.armrest.color = "Czerwony"
        elif index == 1:
            self.body.armrest.color = "Zielony"
        elif index == 2:
            self.body.armrest.color = "Niebieski"
        self.body.armrest.check_activation()

    def on_change_cbox_cup_holder_color(self, index):
        # print(f"Selected size index: {index}")
        if index == 0:
            self.body.cup_holder.color = "Czerwony"
        elif index == 1:
            self.body.cup_holder.color = "Zielony"
        elif index == 2:
            self.body.cup_holder.color = "Niebieski"
        self.body.cup_holder.check_activation()

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

    def on_radio_button_armrest_clicked(self):
        sender = self.sender()

        if sender.isChecked():
            self.body.armrest.heating = sender.text()
        print(f'Selected option: {sender.text()}')

        self.body.armrest.check_activation()

    def on_radio_button_cup_holder_clicked(self):
        sender = self.sender()

        if sender.isChecked():
            self.body.cup_holder.usb_socket = sender.text()
        print(f'Selected option: {sender.text()}')

        self.body.cup_holder.check_activation()

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
    
    @pyqtSlot()
    def on_schedule_clicked(self):
        print(f"\nScheduled body nr: {self.body_counter}")

        new_petri_net_thread = PetriNetThread(self.body_counter, self.body, self.mpl_widget)
        new_petri_net_thread.finished_signal.connect(self.on_thread_finished)
        self.list_of_threads.append(new_petri_net_thread)
        # self.petri_net_thread.start()
        self.list_of_threads[self.body_counter - 1].start()

        self.body.remove_parameters()
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
