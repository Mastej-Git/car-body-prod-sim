class Place:
    def __init__(self, name, tokens=0, max_tokens=1) -> None:
        self.name = name
        self.tokens = tokens
        self.max_tokens = max_tokens

    def __str__(self) -> str:
        return f"Place({self.name}, tokens={self.tokens})"
    

class Transition:
    def __init__(self, name, inputs, outputs) -> None:
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

    def is_enabled(self):
        return all(place.tokens >= weight for place, weight in self.inputs.items())
    
    def can_fire(self):
        for place, count in self.outputs.items():
            if place.max_tokens is not None and place.tokens + count > place.max_tokens:
                return False
        return True
    
    def fire(self):
        if not self.is_enabled():
            raise Exception(f"Transition {self.name} is not enabled")
        if not self.can_fire():
            raise Exception(f"Transition {self.name} cannot fire due to max token constraints")
        
        for place, weight in self.inputs.items():
            place.tokens -= weight

        for place, weight in self.outputs.items():
            place.tokens += weight

    def reverse_fire(self):
        for place, weight in self.inputs.items():
            place.tokens += weight

        for place, weight in self.outputs.items():
            place.tokens -= weight

    def __str__(self) -> str:
        inputs = ", ".join(f"{place.name}: {weight}" for place, weight in self.inputs.items())
        outputs = ", ".join(f"{place.name}: {weight}" for place, weight in self.outputs.items())
        return f"Transition({self.name}, inputs=[{inputs}], outputs=[{outputs}])"
    

class PetriNet:
    def __init__(self) -> None:
        self.places = {}
        self.transitions = {}

    def add_place(self, name, tokens=0, max_tokens=1):
        if name in self.places:
            raise Exception(f"Place {name} already exists")
        self.places[name] = Place(name, tokens, max_tokens)

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