import numpy as np

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
)
from PyQt5.QtCore import QTimer

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from petri_nets.PetriNet import PetriNet

class MatplotlibWidget(QWidget):
    def __init__(self, petri_net: PetriNet, parent=None):
        super(MatplotlibWidget, self).__init__(parent)

        self.petri_net = petri_net

        self.tasks = []
        self.start_times = []
        self.durations = []
        self.current_time = 0

        for place in self.petri_net.places.values():
            self.tasks.append(f"{place.name}")
        self.start_times = [0 for place in self.petri_net.places.keys()]
        self.durations = [place.cooldown_ms for place in self.petri_net.places.values()]
        
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.bars = self.ax.barh(self.tasks, self.durations, left=self.start_times, color='#00ffff')

        self.fig.set_facecolor("#2e2e2e")

        self.ax.invert_yaxis()
        self.ax.set_xlim(left=0, right=5)

        self.ax.set_facecolor('#2e2e2e')
        self.ax.tick_params(axis='x', colors='#00ffff')
        self.ax.tick_params(axis='y', colors='#00ffff')
        self.ax.spines['top'].set_color('#00ffff')
        self.ax.spines['bottom'].set_color('#00ffff')
        self.ax.spines['left'].set_color('#00ffff')
        self.ax.spines['right'].set_color('#00ffff')
        self.ax.xaxis.label.set_color('#00ffff')
        self.ax.yaxis.label.set_color('#00ffff')
        self.ax.title.set_color('#00ffff')
        self.ax.grid(True, color='#404040', linestyle='--', linewidth=0.5)

        self.ax.set_xlabel('Ilość ładunków')
        self.ax.set_ylabel('Akcja')
        self.ax.set_title('Stan korpusów')
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        
    def plot(self):
        
        self.start_times = [0 for place in self.petri_net.places.keys()]
        self.durations = [place.tokens for place in self.petri_net.places.values()]

        for bar, new_val in zip(self.bars, self.durations):
            bar.set_width(new_val)
        
        self.canvas.draw()

class PlotWidget(QWidget):
    def __init__(self, petri_net, parent=None):
        super(PlotWidget, self).__init__(parent)
        self.petri_net = petri_net
        self.left = []

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        
        self.categories = [place for place in self.petri_net.places.keys()]
        self.values = [place.cooldown_ms/1000 for place in self.petri_net.places.values()]

        j = 0
        for place1 in self.petri_net.places.keys():
            i = 0
            left = 0
            for place2 in self.petri_net.places.values():
                if i == j: 
                    break
                left += place2.cooldown_ms/1000
                i += 1
            self.left.append(left)
            j += 1
        
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.bars = self.ax.barh(self.categories, self.values, left=self.left, color='#00ffff')

        self.fig.set_facecolor("#2e2e2e")

        self.ax.invert_yaxis()
        self.ax.set_xlim(left=0, right=60)

        self.ax.set_facecolor('#2e2e2e')
        self.ax.tick_params(axis='x', colors='#00ffff')
        self.ax.tick_params(axis='y', colors='#00ffff')
        self.ax.spines['top'].set_color('#00ffff')
        self.ax.spines['bottom'].set_color('#00ffff')
        self.ax.spines['left'].set_color('#00ffff')
        self.ax.spines['right'].set_color('#00ffff')
        self.ax.xaxis.label.set_color('#00ffff')
        self.ax.yaxis.label.set_color('#00ffff')
        self.ax.title.set_color('#00ffff')
        self.ax.grid(True, color='#404040', linestyle='--', linewidth=0.5)

        self.ax.set_xlabel('Ilość ładunków')
        self.ax.set_ylabel('Akcja')
        self.ax.set_title('Stan korpusów')
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)
        
        self.i = 0
    
    def update_plot(self):
        self.i += 1
        new_values = [val + np.sin(self.i / 10.0) for val in self.values]
        
        for bar, new_val in zip(self.bars, new_values):
            bar.set_width(new_val)
        
        self.canvas.draw()