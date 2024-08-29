from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

from PetrisNet import PetriNet

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MatplotlibWidget(QWidget):
    def __init__(self, petri_net: PetriNet, parent=None):
        super().__init__(parent)

        self.petri_net = petri_net
        
        self.figure = Figure(facecolor='#404040')
        
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        
        self.tasks = []
        self.start_times = []
        self.durations = []
        self.current_time = 0
        
    def plot(self):

        self.tasks = self.petri_net.places.keys()
        self.start_times = [0 for place in self.petri_net.places.keys()]
        self.durations = [place.tokens for place in self.petri_net.places.values()]

        self.figure.clear()
        
        ax = self.figure.add_subplot(111)
        
        ax.set_facecolor('#404040')
        ax.tick_params(axis='x', colors='#00ffff')
        ax.tick_params(axis='y', colors='#00ffff')
        ax.spines['top'].set_color('#00ffff')
        ax.spines['bottom'].set_color('#00ffff')
        ax.spines['left'].set_color('#00ffff')
        ax.spines['right'].set_color('#00ffff')
        ax.xaxis.label.set_color('#00ffff')
        ax.yaxis.label.set_color('#00ffff')
        ax.title.set_color('#00ffff')
        
        ax.barh(self.tasks, self.durations, left=self.start_times, color='#00ffff')

        ax.grid(True, color='#2e2e2e', linestyle='--', linewidth=0.5)
        
        ax.invert_yaxis()
        
        ax.set_xlabel('Time')
        ax.set_ylabel('Tokens')
        ax.set_title('Tokens distribution')
        
        self.canvas.draw()