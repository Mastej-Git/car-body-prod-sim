![Isaac Sim](docs/readme/hero_shot_compressed.png)

---
# PN Car Body App

PN Car Body App is an application prepared for the engenieering thesis at Wroclaw University of Science and Technology. The program is designed to simulate the production process of car body interior. It focuses on the integrated assembly of driver-passenger interface elements. The project applies Petri net theory to map and analyze the discrete event logic. It was developed in the idea of beeing used in real scenario in car factory to automate and optimize the time it takes to set up the production sequence of large number of very modular elements. The user is able to load a number of car bodies description from JSON file as well as create new ones directly inside the app. The planed production process is represented by the Gantt chart.

## Key Features

- [Input]: Loading the number of car bodies from JSON file description - `bodies.json`.
- [Digital Twin](https://en.wikipedia.org/wiki/Digital_twin): Simulate the real production process and use output values to optimize the real-world process.
- [Representation] Production process is represented using Gantt Chart.
- [Model](https://en.wikipedia.org/wiki/Petri_net): Applies Petri nets  (PT net) mathematical modeling language to represent the production process. 

## Key Applications

- [Isaac Lab](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/isaac_lab_tutorials/index.html): GPU-accelerated framework built for reinforcement learning, imitation learning, and motion planning.
- [ROS Bridge](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/ros2_tutorials/ros2_landing_page.html): Integration with Robot Operating System (ROS).
- [Synthetic Data Generation](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/synthetic_data_generation/index.html): Collection of SDG tools

## Quick Start

This section guides you through building Isaac Sim from source code.

### 1. Clone, Build, Run


```bash
git clone https://github.com/Mastej-Git/PN-Car-Body-App.git
cd PN-Car-Body-App
make setup-env
make run
```
