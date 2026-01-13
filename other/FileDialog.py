import os

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QFileDialog,
)

class FileDialog(QWidget):
    def __init__(self, label: QLabel):
        super().__init__()

        self.label = label

    def show_file_dialog(self):
        home_dir = os.environ.get('HOME')

        options = QFileDialog.Options()
        read_file_name, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", 
            "All Files (*);;Text Files (*.txt)", 
            options=options
        )
        
        if read_file_name.endswith(".json"):
            self.label.setText(f'Wybrany plik: {read_file_name}')
            return read_file_name
        
        self.label.setText(f'ZŁY FORMAT PLIKU! Oczekiwany format: .json\n\nWybrany plik: {read_file_name}')
        return ""
