# PN Car Body App

PN Car Body App is an application prepared for the engenieering thesis at Wroclaw University of Science and Technology. The program is designed to simulate the production process of car body interior. It focuses on the integrated assembly of driver-passenger interface elements. The project applies Petri net theory to map and analyze the discrete event logic. It was developed in the idea of beeing used in real scenario in car factory to automate and optimize the time it takes to set up the production sequence of large number of very modular elements. The user is able to load a number of car bodies description from JSON file as well as create new ones directly inside the app. The planed production process is represented by the Gantt chart.

## Key Features

- [Input]: Loading the number of car bodies from JSON file description - `bodies.json`.
- [Digital Twin](https://en.wikipedia.org/wiki/Digital_twin): Simulate the real production process and use output values to optimize the real-world process.
- [Representation] Production process is represented using Gantt Chart.
- [Model](https://en.wikipedia.org/wiki/Petri_net): Applies Petri nets  (PT net) mathematical modeling language to represent the production process. 

## Quick Start

This section guides you through building PN-Car-Body-App from source code.

### Clone &rarr; Build &rarr; Run:


```bash
git clone https://github.com/Mastej-Git/PN-Car-Body-App.git
cd PN-Car-Body-App
make setup-env
make run
```

## Tools

- [Poetry](https://python-poetry.org/): Python packaging and dependency management.
- [Ruff](https://docs.astral.sh/ruff/): An extremely fast Python linter and code formatter.

## Engineering Thesis

Location of the engineering thesis: `/docs/engineering_thesis.pdf`
