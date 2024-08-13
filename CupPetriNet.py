from PetrisNet import PetriNet

cup_petris_net_start = PetriNet()
cup_petris_net_aluminium = PetriNet()
cup_petris_net_end = PetriNet()

# start ścieżki
cup_petris_net_start.add_place("P1", tokens=0, max_tokens=5)
cup_petris_net_start.add_place("P2", tokens=3, max_tokens=3)
cup_petris_net_start.add_place("P3", tokens=0, max_tokens=5)

# ścieżka dla aluminium
cup_petris_net_aluminium.add_place("P3", tokens=0, max_tokens=5)
cup_petris_net_aluminium.add_place("P4", tokens=0, max_tokens=5)
cup_petris_net_aluminium.add_place("P5", tokens=10, max_tokens=10)
cup_petris_net_aluminium.add_place("P10", tokens=2, max_tokens=2)
cup_petris_net_aluminium.add_place("P11", tokens=0, max_tokens=5)
cup_petris_net_aluminium.add_place("P16", tokens=3, max_tokens=3)
cup_petris_net_aluminium.add_place("P17", tokens=0, max_tokens=5)
cup_petris_net_aluminium.add_place("P20", tokens=2, max_tokens=2)
cup_petris_net_aluminium.add_place("P21", tokens=0, max_tokens=5)
cup_petris_net_aluminium.add_place("P26", tokens=0, max_tokens=5)
cup_petris_net_aluminium.add_place("P29", tokens=2, max_tokens=2)
cup_petris_net_aluminium.add_place("P30", tokens=0, max_tokens=5)
cup_petris_net_aluminium.add_place("P35", tokens=0, max_tokens=5)
cup_petris_net_aluminium.add_place("P38", tokens=0, max_tokens=5)

# koniec ścieżki
cup_petris_net_end.add_place("P2", tokens=3, max_tokens=3)
cup_petris_net_end.add_place("P16", tokens=3, max_tokens=3)
cup_petris_net_end.add_place("P38", tokens=0, max_tokens=5)
cup_petris_net_end.add_place("P39", tokens=0, max_tokens=5)


# start ścieżki
cup_petris_net_start.add_transition("T1", {}, {"P1": 1})
cup_petris_net_start.add_transition("T2", {"P1": 1, "P2": 1}, {"P3": 1})

# ściżka dla aluminium
cup_petris_net_aluminium.add_transition("T3", {"P3": 1}, {"P4": 1})
cup_petris_net_aluminium.add_transition("T6", {"P4": 1, "P5": 1, "P10": 1}, {"P11": 1})
cup_petris_net_aluminium.add_transition("T9", {"P11": 1}, {"P17": 1})
cup_petris_net_aluminium.add_transition("T12", {"P16": 1, "P17": 1, "P20": 1}, {"P10": 1, "P21": 1})
cup_petris_net_aluminium.add_transition("T15", {"P21": 1}, {"P26": 1})
cup_petris_net_aluminium.add_transition("T18", {"P16": 1, "P26": 1, "P29": 1}, {"P30": 1, "P16": 1})
cup_petris_net_aluminium.add_transition("T21", {"P30": 1}, {"P35": 1})
cup_petris_net_aluminium.add_transition("T24", {"P35": 1}, {"P29": 1, "P38": 1})

# koniec ścieżki
cup_petris_net_end.add_transition("T27", {"P38": 1}, {"P2": 1, "P16": 1, "P39": 1})
cup_petris_net_end.add_transition("T28", {"P39": 1}, {})

def merge_nets(list_of_nets: list[PetriNet]):

    pn = PetriNet()

    for net in list_of_nets:
        for place_name, place in net.places.items():
            if not place_name in pn.places:
                pn.add_place(place_name, tokens=place.tokens, max_tokens=place.max_tokens)

        for transition_name, transition in net.transitions.items():
            if not transition_name in pn.transitions:
                input_places = {place.name: weight for place, weight in transition.inputs.items()}
                output_places = {place.name: weight for place, weight in transition.outputs.items()}
                pn.add_transition(transition_name, input_places, output_places)

    return pn