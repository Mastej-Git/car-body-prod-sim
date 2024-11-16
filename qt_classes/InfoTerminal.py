from PyQt5.QtWidgets import QVBoxLayout, QLabel, QScrollArea, QWidget, QGroupBox
from PyQt5.QtCore import Qt

from enums.StyleSheet import StyleSheet

class InfoTerminal:

    def __init__(self, list_of_info_group_box) -> None:

        self.buffor_size = 300
        
        self.list_of_info_group_box = list_of_info_group_box

        self.layout_info = QVBoxLayout()

        self.starting_label_info = QLabel("Brak informacji")
        self.starting_label_info.setStyleSheet(StyleSheet.InfoLabel.value)
        self.starting_label_info.setAlignment(Qt.AlignCenter)

        self.scroll_area1 = QScrollArea()
        self.scroll_widget_info = QWidget()
        self.outer_layout_info = QVBoxLayout(self.scroll_widget_info)

        self.scroll_widget_info.setLayout(self.outer_layout_info)
        self.scroll_area1.setWidget(self.scroll_widget_info)
        self.scroll_area1.setWidgetResizable(True)

        self.outer_layout_info.addWidget(self.starting_label_info)
        self.layout_info.addWidget(self.scroll_area1)

    def add_text_info(self, text):

        if len(self.list_of_info_group_box) == 0:
            self.outer_layout_info.removeWidget(self.starting_label_info)
            self.starting_label_info.deleteLater()

        if self.outer_layout_info.count() >= self.buffor_size:
            label = self.outer_layout_info.itemAt(0).widget()
            self.outer_layout_info.removeWidget(self.outer_layout_info.itemAt(0).widget())
            label.deleteLater()

        label1 = QLabel(text)
        label1.setWordWrap(True)
        label1.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        label1.setStyleSheet(StyleSheet.InfoLabel.value)

        main_layout = QVBoxLayout()
        main_layout.addWidget(label1)

        self.list_of_info_group_box.append(label1)
        self.outer_layout_info.addWidget(label1, alignment=Qt.AlignTop)
