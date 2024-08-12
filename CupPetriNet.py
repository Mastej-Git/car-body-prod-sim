from PetrisNet import PetriNet

cup_petris_net = PetriNet()

cup_petris_net.add_place("P1", tokens=0, max_tokens=5)
cup_petris_net.add_place("P2", tokens=3, max_tokens=3)
cup_petris_net.add_place("P3", tokens=0, max_tokens=5)

cup_petris_net.add_place("P4", tokens=0, max_tokens=5)
cup_petris_net.add_place("P5", tokens=10, max_tokens=10)
cup_petris_net.add_place("P10", tokens=2, max_tokens=2)
cup_petris_net.add_place("P11", tokens=0, max_tokens=5)
cup_petris_net.add_place("P16", tokens=3, max_tokens=3)
cup_petris_net.add_place("P17", tokens=0, max_tokens=5)
cup_petris_net.add_place("P20", tokens=2, max_tokens=2)
cup_petris_net.add_place("P21", tokens=0, max_tokens=5)
cup_petris_net.add_place("P26", tokens=0, max_tokens=5)
cup_petris_net.add_place("P29", tokens=2, max_tokens=2)
cup_petris_net.add_place("P30", tokens=0, max_tokens=5)
cup_petris_net.add_place("P35", tokens=0, max_tokens=5)
cup_petris_net.add_place("P38", tokens=0, max_tokens=5)
cup_petris_net.add_place("P39", tokens=0, max_tokens=5)



cup_petris_net.add_transition("T1", {}, {"P1": 1})
cup_petris_net.add_transition("T2", {"P1": 1, "P2": 1}, {"P3": 1})

cup_petris_net.add_transition("T3", {"P3": 1}, {"P4": 1})
cup_petris_net.add_transition("T6", {"P4": 1, "P5": 1, "P10": 1}, {"P11": 1})
cup_petris_net.add_transition("T9", {"P11": 1}, {"P17": 1})
cup_petris_net.add_transition("T12", {"P16": 1, "P17": 1, "P20": 1}, {"P10": 1, "P21": 1})
cup_petris_net.add_transition("T15", {"P21": 1}, {"P26": 1})
cup_petris_net.add_transition("T18", {"P16": 1, "P26": 1, "P29": 1}, {"P30": 1, "P16": 1})
cup_petris_net.add_transition("T21", {"P30": 1}, {"P35": 1})
cup_petris_net.add_transition("T24", {"P35": 1}, {"P29": 1, "P38": 1})
cup_petris_net.add_transition("T27", {"P38": 1}, {"P2": 1, "P16": 1, "P39": 1})
cup_petris_net.add_transition("T28", {"P39": 1}, {})

def merge_nets(pn1: PetriNet, pn2: PetriNet):

    merged_pn = PetriNet()

    merged_pn.places = {**pn1.places, **pn2.places}
    merged_pn.transitions = {**pn1.transitions, **pn2.transitions}

    return merged_pn
