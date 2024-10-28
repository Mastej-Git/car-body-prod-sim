import numpy as np

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
)
from PyQt5.QtCore import QTimer

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from petri_nets.PetriNet import PetriNet
from Body import Body

class PlotWidget(QWidget):

    def __init__(self, petri_net: PetriNet, parent=None):
        super(PlotWidget, self).__init__(parent)

        self.plot_colors = ["skyblue", "red", "lightgreen"]
        self.color_iter = 0
        self.numb_of_plots = 0
        self.petri_net = petri_net
        self.list_of_machines_p = []

        self.list_of_durations = []
        self.list_of_starting_times = []

        self.tasks = []
        for place in self.petri_net.places.values():
            if "Maszyna M" in place.description:
                self.list_of_machines_p.append(place)

        for machine in self.list_of_machines_p:
            self.tasks.append(machine.name)
        
        # self.start_times1 = [1, 4, 7, 10, 14, 15, 17, 21, 24, 27, 31, 34, 38, 41, 45, 49, 53, 57, 61]
        # self.durations1 = [3, 2, 5, 1, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3]
        # self.durations1 = self.calculate_duration()
        # self.start_times1 = self.calculate_starting_times()

        # self.start_times2 = [self.start_times1[i] + self.durations1[i] + 0.5 for i in range(len(self.tasks))]
        # self.durations2 = [2, 3, 4, 2, 1, 4, 2, 3, 2, 3, 4, 3, 2, 4, 3, 2, 4, 3, 2]     
        
        self.y_pos = np.arange(len(self.tasks))  
        
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        
        # self.bars1 = self.ax.barh(self.y_pos, self.durations1, left=self.start_times1, 
        #                           color='skyblue', height=0.4, label='Dataset 1')
        
        # self.bars2 = self.ax.barh(self.y_pos, self.durations2, left=self.start_times2, 
        #                           color='lightgreen', height=0.4, label='Dataset 2')
        
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
        
        self.ax.set_yticks(self.y_pos)
        self.ax.set_yticklabels(self.tasks)

        self.ax.invert_yaxis()
        self.ax.set_xlim(left=0, right=90)
        self.ax.set_xlabel('Czas')
        self.ax.set_ylabel('Maszyny')
        self.ax.set_title('Planowane dystrybucja zadań do maszyn')
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update_plot)
        # self.timer.start(100)  

        self.i = 0

    def update_plot1(self, body):

        self.calculate_duration(body)
        self.calculate_starting_times()

        self.bars1 = self.ax.barh(self.y_pos, self.list_of_durations[self.numb_of_plots], left=self.list_of_starting_times[self.numb_of_plots], 
                                  color=self.plot_colors[self.color_iter % 3], height=0.4, label='Dataset 1')
        
        self.color_iter += 1
        self.numb_of_plots += 1
        self.canvas.draw()

    def calculate_duration(self, body: Body):

        duration = []

        if body.upper_panel.ac_type == "2-strefowa":
            duration.append((self.petri_net.places["P103"].cooldown_ms + self.petri_net.places["P105"].cooldown_ms)/1000)
        else:
            duration.append(0)
        
        if body.upper_panel.ac_type == "4-strefowa":
            duration.append((self.petri_net.places["P104"].cooldown_ms + self.petri_net.places["P106"].cooldown_ms)/1000)
        else:
            duration.append(0)

        if body.middle_panel.functionality == "Interfejs multimedialny":
            duration.append((self.petri_net.places["P203"].cooldown_ms + self.petri_net.places["P205"].cooldown_ms)/1000)
        else:
            duration.append(0)

        if body.middle_panel.functionality == "Schowek":
            duration.append((self.petri_net.places["P204"].cooldown_ms + self.petri_net.places["P206"].cooldown_ms)/1000)
        else:
            duration.append(0)

        if body.lower_panel.functionality == "Ładowarka bezprzewodowa":
            duration.append((self.petri_net.places["P303"].cooldown_ms + self.petri_net.places["P305"].cooldown_ms)/1000)
        else:
            duration.append(0)
        
        if body.lower_panel.functionality == "Półka":
            duration.append((self.petri_net.places["P304"].cooldown_ms + self.petri_net.places["P306"].cooldown_ms)/1000)
        else:
            duration.append(0)

        if body.lower_panel.is_cup == "Tak":
            duration.append((self.petri_net.places["P308"].cooldown_ms + self.petri_net.places["P309"].cooldown_ms)/1000)
        else:
            duration.append(0)
        
        duration.append((self.petri_net.places["P312"].cooldown_ms + self.petri_net.places["P315"].cooldown_ms)/1000)

        if body.armrest.heating == "Tak":
            duration.append((self.petri_net.places["P403"].cooldown_ms + self.petri_net.places["P405"].cooldown_ms)/1000)
        else:
            duration.append(0)
        
        duration.append((self.petri_net.places["P407"].cooldown_ms + self.petri_net.places["P410"].cooldown_ms)/1000)

        duration.append((self.petri_net.places["P412"].cooldown_ms + self.petri_net.places["P415"].cooldown_ms)/1000)

        duration.append((self.petri_net.places["P502"].cooldown_ms + self.petri_net.places["P503"].cooldown_ms)/1000)

        duration.append((self.petri_net.places["P504"].cooldown_ms + self.petri_net.places["P505"].cooldown_ms)/1000)

        if body.cup_holder.usb_socket == "Tak":
            duration.append((self.petri_net.places["P506"].cooldown_ms + self.petri_net.places["P508"].cooldown_ms)/1000)
        else:
            duration.append(0)
        
        duration.append((self.petri_net.places["P510"].cooldown_ms + self.petri_net.places["P513"].cooldown_ms)/1000)

        duration.append((self.petri_net.places["P602"].cooldown_ms + self.petri_net.places["P603"].cooldown_ms)/1000)

        duration.append((self.petri_net.places["P604"].cooldown_ms + self.petri_net.places["P605"].cooldown_ms)/1000)

        duration.append((self.petri_net.places["P606"].cooldown_ms + self.petri_net.places["P609"].cooldown_ms)/1000)

        duration.append((self.petri_net.places["P611"].cooldown_ms + self.petri_net.places["P614"].cooldown_ms)/1000)

        self.list_of_durations.append(duration)
    
    def calculate_starting_times(self):

        if len(self.list_of_durations) > 1:
            previous_starting_times = self.list_of_starting_times[self.numb_of_plots - 1]
        else:
            previous_starting_times = [0 for i in range(len(self.list_of_durations[0]))]

        starting_times = []

        print(previous_starting_times)
        print(self.list_of_durations[self.numb_of_plots])
        j = 0
        for machine in self.list_of_machines_p:
            i = 0
            sum = 0
            for duration in self.list_of_durations[self.numb_of_plots]:
                if i == j: break
                sum += duration
                i += 1
                if duration != 0: sum += 1
            if sum <= previous_starting_times[i] and self.check_previous_times(i):
                sum = previous_starting_times[i] + self.list_of_durations[self.numb_of_plots - 1][i] 
                if self.list_of_durations[self.numb_of_plots - 1][i] != 0:
                    sum += 1
            starting_times.append(sum)
            j += 1

        self.list_of_starting_times.append(starting_times)

    def check_previous_times(self, index):
        for k in range(self.numb_of_plots):
            if self.list_of_durations[k][index] != 0:
                return True
        return False

    def sum_durations(self, index):
        sum = 0

        for j in range(self.numb_of_plots):
            sum += self.list_of_durations[j][index]

        return sum