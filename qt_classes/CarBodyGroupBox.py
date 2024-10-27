from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLabel,
                             QGroupBox,
                             QVBoxLayout,
                             QHBoxLayout)

from Body import Body
from qt_classes.AnimatedButton import AnimatedButton

from other.StyleSheets import style_sheet_label, style_sheet_QGroupBox


class CarBodyGroupBox():

    def __init__(self, body: Body) -> None:
        
        self.group_box = QGroupBox()
        # self.group_box.setStyleSheet(style_sheet_QGroupBox)
        self.body = body

        label_text = self.body.__str__()

        self.label = QLabel(label_text)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setStyleSheet(style_sheet_label)

        self.button_schedule = AnimatedButton("Planuj", 200, 40)
        self.button_ready = AnimatedButton("Gotowe", 200, 40)
        self.button_edit = AnimatedButton("Edytuj", 200, 40)
        self.button_remove = AnimatedButton("Usuń", 200, 40)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.button_schedule)
        buttons_layout.addWidget(self.button_ready)
        buttons_layout.addWidget(self.button_edit)
        buttons_layout.addWidget(self.button_remove)

        main_layout = QHBoxLayout()

        main_layout.addWidget(self.label)
        main_layout.addLayout(buttons_layout)

        self.group_box.setLayout(main_layout)

    def get_car_body_group_box(self):
        return self.group_box
    
    def recreate_label(self):
        self.label.setText(str(self.body))
