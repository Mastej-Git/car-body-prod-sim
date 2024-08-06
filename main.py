from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QStackedWidget, 
    QFrame, QSizePolicy, QGroupBox, QComboBox
)
from PyQt5.QtCore import Qt


style_sheet_QPushButton = """
            QPushButton {
                background-color: #404040;
                color: #00ffff;
                border: 1px solid #404040;
                height: 50px;
            }
            QPushButton:hover {
                background-color: #2e2e2e;
                border: 1px solid #00ffff;
            }
        """

style_sheet_QComboBox = """
QComboBox {
    background-color: #404040;
    color: #00ffff;
    height: 40px;
    border: 1px solid #404040;
    padding: 5px;
    border-radius: 3px;
    combobox-popup: 0;
}

QComboBox:hover {
    background-color: #2e2e2e;
    border: 1px solid #00ffff;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;
    border-left-width: 1px;
    border-left-color: #00ffff;
    border-left-style: solid;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
    background-color: #404040;
}

QComboBox::down-arrow {
    image: url(down-arrow.png);
    width: 10px;
    height: 10px;
}

QComboBox QAbstractItemView {
    background-color: #404040;
    color: #00ffff;
    selection-background-color: #2e2e2e;
    selection-color: #00ffff;
    border: 1px solid #00ffff;
}
"""

style_sheet_label = """
QLabel {
    color: #00ffff;
    padding: 5px;
    border-radius: 3px;
    height: 30px;
}
"""


class Cup():

    def __init__(self, material, size) -> None:
        self.material = material
        self.size = size

class AirConditioning():

    def __init__(self, refrigerant_type, compressor_type, heat_exchanger_efficiency):
        self.refrigerant_type = refrigerant_type
        self.compressor_type = compressor_type
        self.heat_exchanger_efficiency = heat_exchanger_efficiency

class Corps():

    def __init__(self, cup: Cup, air_conditioning: AirConditioning) -> None:
        self.cup = cup
        self.air_conditioning = AirConditioning            

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.cup = Cup("", "")

        self.setWindowTitle("Tab Example")
        self.setGeometry(100, 100, 800, 1000)

        central_widget = QFrame()
        central_widget.setStyleSheet("""
            QFrame {
                border: 1px solid #2e2e2e;
                border-radius: 10px;
                background-color: #2e2e2e;
            }
        """)
        layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        self.tabs.tabBar().setExpanding(True)
        self.tabs.setStyleSheet("""
            QTabWidget::pane { 
                border: none; 
            }
            QTabBar::tab {
                background: #2e2e2e; 
                color: #b1b1b1; 
                width: 260px; 
                height: 40px;
            }
            QTabBar::tab:selected { 
                background: #404040; 
                color: #00ffff; 
                font-weight: bold;
            }
        """)

        
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.addTab(self.tab1, "Add Corps")
        self.tabs.addTab(self.tab2, "Current corps state")
        self.tabs.addTab(self.tab3, "Gantt chart")

        self.create_tab_content()
        layout.addWidget(self.tabs)
        self.setCentralWidget(central_widget)

    def create_tab_content(self):
        layout1 = QVBoxLayout()
        sub_tab_widget = QTabWidget()
        sub_tab_widget.setTabPosition(QTabWidget.West)
        sub_tab_widget.setStyleSheet("""
            QTabBar::tab {
                background: #2e2e2e;
                color: #b1b1b1;
                width: 50px;
                height: 120px;
            }
            QTabBar::tab:selected {
                background: #404040;
                color: #00ffff;
                font-weight: bold;
            }
        """)

        sub_tab1 = QWidget()
        sub_tab2 = QWidget()
        sub_tab3 = QWidget()

        sub_tab1 = self.create_sub_tab_cup_content()

        sub_layout2 = QVBoxLayout()
        sub_layout2.addWidget(QLabel("This is the content of Sub-Tab 2"))
        sub_tab2.setLayout(sub_layout2)

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

        layout2 = QVBoxLayout()
        layout2.addWidget(QLabel("This is the content of Tab 2"))

        group_box1 = QGroupBox()
        group_box1 = self.create_group_box_corpse()
        group_box1.setFixedSize(800, 200)
        group_box2 = QGroupBox()
        group_box2 = self.create_group_box_corpse()
        group_box2.setFixedSize(800, 200)

        outer_layout = QVBoxLayout()
        outer_layout.addWidget(group_box1)
        outer_layout.addWidget(group_box2)
        self.tab2.setLayout(outer_layout)

        # Set the initial size and resize policy
        # layout2.setMinimumHeight(200)
        # layout2.setMinimumWidth(400)
        # layout2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.tab2.setLayout(layout2)

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
        combo_box_material.addItems(["Alminum", "Stainless steel", "policarbonate"])
        combo_box_material.setStyleSheet(style_sheet_QComboBox)
        combo_box_material.currentIndexChanged.connect(self.on_change_cbox_material)

        combo_box_size = QComboBox()
        combo_box_size.addItems(["500 ml", "750 ml", "1 L"])
        combo_box_size.setStyleSheet(style_sheet_QComboBox)
        combo_box_size.currentIndexChanged.connect(self.on_change_cbox_size)

        button_add_to_corpse = QPushButton("Add")
        button_add_to_corpse.setStyleSheet(style_sheet_QPushButton)
        button_add_to_corpse.clicked.connect(self.on_change_pb)

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
    
    def create_group_box_corpse(self):
        group_box = QGroupBox()

        label = QLabel("This is a label. The label text will determine the height of the label.")
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        label.setStyleSheet(style_sheet_label)

        button1 = QPushButton("Add")
        button1.setStyleSheet(style_sheet_QPushButton)
        button1.setFixedSize(200, 40)
        button2 = QPushButton("Remove")
        button2.setStyleSheet(style_sheet_QPushButton)
        button2.setFixedSize(200, 40)
        button3 = QPushButton("Edit")
        button3.setStyleSheet(style_sheet_QPushButton)
        button3.setFixedSize(200, 40)

        buttons_layout = QVBoxLayout()
        # buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.addWidget(button1)
        buttons_layout.addWidget(button2)
        buttons_layout.addWidget(button3)

        main_layout = QHBoxLayout()

        main_layout.addWidget(label)
        main_layout.addLayout(buttons_layout)

        group_box.setLayout(main_layout)

        return group_box

    def on_change_cbox_material(self, index):
        print(f"Selected material index: {index}")
        if index == 0:
            self.cup.material = "aluminum"
        elif index == 1:
            self.cup.material = "stainless steel"
        elif index == 2:
            self.cup.material = "policarbonate"

    def on_change_cbox_size(self, index):
        print(f"Selected size index: {index}")
        if index == 0:
            self.cup.size = "500"
        elif index == 1:
            self.cup.size = "750"
        elif index == 2:
            self.cup.size = "1000"

    def on_change_pb(self):
        print(f"Cup added with parameters: {self.cup.material}, {self.cup.size}")

def main():
    app = QApplication([])
    app.setStyleSheet("""
        QWidget {
            background-color: #2e2e2e;
            color: #b1b1b1;
        }
        QLabel {
            color: #b1b1b1;
        }
    """)
    window = GUI()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
