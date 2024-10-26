from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
)

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import QTimer
import numpy as np

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
        self.durations = [place.cooldown for place in self.petri_net.places.values()]
        
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
    def __init__(self, parent=None):
        super(PlotWidget, self).__init__(parent)

        # Gantt chart data
        self.tasks = ['Task A', 'Task B', 'Task C', 'Task D']
        
        # Dataset 1
        self.start_times1 = [1, 4, 7, 10]  # Start times for tasks in dataset 1
        self.durations1 = [3, 2, 5, 1]     # Durations for tasks in dataset 1

        # Dataset 2 (Same tasks, but we'll offset their start times to avoid overlap)
        self.start_times2 = [self.start_times1[i] + self.durations1[i] + 0.5 for i in range(len(self.tasks))]
        self.durations2 = [2, 3, 4, 2]     # Durations for tasks in dataset 2

        # Position of tasks on y-axis
        self.y_pos = np.arange(len(self.tasks))  # Same y positions for both datasets

        # Initialize the plot
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)

        # Create Gantt bars for dataset 1
        self.bars1 = self.ax.barh(self.y_pos, self.durations1, left=self.start_times1, 
                                  color='skyblue', height=0.4, label='Dataset 1')
        # Create Gantt bars for dataset 2
        self.bars2 = self.ax.barh(self.y_pos, self.durations2, left=self.start_times2, 
                                  color='lightgreen', height=0.4, label='Dataset 2')

        # Styling the plot (similar to your original code)
        self.fig.set_facecolor("#2e2e2e")
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

        # Combine all tasks into one list for y-axis labels
        self.ax.set_yticks(self.y_pos)
        self.ax.set_yticklabels(self.tasks)

        self.ax.invert_yaxis()
        self.ax.set_xlim(left=0, right=20)
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Task')
        self.ax.set_title('Gantt Chart with Two Data Sets')

        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Timer to update the plot
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)  # Update every 100ms

        self.i = 0

    def update_plot(self):
        # Update the task durations dynamically using a sine wave
        self.i += 1
        new_durations1 = [d + np.sin(self.i / 10.0) for d in self.durations1]
        new_durations2 = [d + np.sin(self.i / 10.0) for d in self.durations2]

        # Update the widths (durations) of the bars for both datasets
        for bar, new_dur in zip(self.bars1, new_durations1):
            bar.set_width(new_dur)
        for bar, new_dur in zip(self.bars2, new_durations2):
            bar.set_width(new_dur)

        # Redraw the canvas to show updates
        self.canvas.draw()
