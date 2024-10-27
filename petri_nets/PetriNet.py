from petri_nets.Place import Place
from petri_nets.Transition import Transition

class PetriNet:
    def __init__(self) -> None:
        self.places = {}
        self.transitions = {}

    def add_place(self, name, description, tokens=0, ready_tokens=0, max_tokens=1, cooldown_ms=500):
        if name in self.places:
            raise Exception(f"Place {name} already exists")
        self.places[name] = Place(name, description, tokens, ready_tokens, max_tokens, cooldown_ms)

    def add_transition(self, name, input_palces, output_places):
        if name in self.transitions:
            raise Exception(f"Transition {name} already exists")
        inputs = {self.places[place_name]: weight for place_name, weight in input_palces.items()}
        outputs = {self.places[place_name]: weight for place_name, weight in output_places.items()}
        self.transitions[name] = Transition(name, inputs, outputs)

    def fire_transition(self, name):
        if name not in self.transitions:
            raise Exception(f"Transition {name} does not exist")
        self.transitions[name].fire()

    def reverse_fire_transition(self, name):
        self.transitions[name].reverse_fire()

    def __str__(self) -> str:
        places_str = "\n".join(str(place) for place in self.places.values())
        transitions_str = "\n".join(str(transition) for transition in self.transitions.values())
        return f"Places:\n{places_str}\nTransitions:\n{transitions_str}"
