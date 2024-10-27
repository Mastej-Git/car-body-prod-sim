class Transition:
    def __init__(self, name, inputs, outputs) -> None:
        self.name = name
        self.inputs = inputs
        self.outputs = outputs

    def is_enabled(self):
        return all(place.ready_tokens >= weight for place, weight in self.inputs.items())
    
    def can_fire(self):
        for place, count in self.outputs.items():
            if place.max_tokens is not None and place.ready_tokens + count > place.max_tokens:
                return False
        return True
    
    def fire(self):
        if not self.is_enabled():
            raise Exception(f"Transition {self.name} is not enabled")
        if not self.can_fire():
            raise Exception(f"Transition {self.name} cannot fire due to max token constraints")
        
        for place, weight in self.inputs.items():
            place.ready_tokens -= weight

        for place, weight in self.outputs.items():
            place.tokens += weight

    def reverse_fire(self):
        for place, weight in self.inputs.items():
            place.ready_tokens += weight

        for place, weight in self.outputs.items():
            place.tokens -= weight

    def __str__(self) -> str:
        inputs = ", ".join(f"{place.name}: {weight}" for place, weight in self.inputs.items())
        outputs = ", ".join(f"{place.name}: {weight}" for place, weight in self.outputs.items())
        return f"Transition({self.name}, inputs=[{inputs}], outputs=[{outputs}])"
    