import os

from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QFileDialog,
)

class FileDialog(QWidget):
    def __init__(self, file_name: list, label: QLabel):
        super().__init__()

        self.file_name = file_name
        self.label = label

    def showFileDialog(self):
        home_dir = os.environ.get('HOME')

        options = QFileDialog.Options()
        read_file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", 
                                                   "All Files (*);;Text Files (*.txt)", 
                                                   options=options)
        if read_file_name.endswith(".json"):
            self.file_name[0] = read_file_name
            self.label.setText(f'Selected File: {read_file_name}')
        else:
            self.label.setText(f'Selected File: {read_file_name}\n\nWRONG FILE TYPE: Should be .json file')