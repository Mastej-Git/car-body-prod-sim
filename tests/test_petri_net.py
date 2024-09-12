import unittest

from petri_nets.PetrisNet import PetriNet

class TestPetriNet(unittest.TestCase):

    def setUp(self):
        self.petri_net = PetriNet()

    def test_init(self):
        self.assertEqual(self.petri_net.places, {})
        self.assertEqual(self.petri_net.transitions, {})

    def test_add_place(self):
        self.petri_net.add_place("P1", "Description1", 2, 5)

        self.assertEqual(list(self.petri_net.places.keys())[0], "P1")
        self.assertEqual(self.petri_net.places["P1"].description, "Description1")
        self.assertEqual(self.petri_net.places["P1"].tokens, 2)
        self.assertEqual(self.petri_net.places["P1"].max_tokens, 5)

        self.petri_net.add_place("P2", "Description2", 0, 3)

        self.assertEqual(list(self.petri_net.places.keys())[1], "P2")
        self.assertEqual(self.petri_net.places["P2"].description, "Description2")
        self.assertEqual(self.petri_net.places["P2"].tokens, 0)
        self.assertEqual(self.petri_net.places["P2"].max_tokens, 3)

    def test_add_places(self):
        self.petri_net.add_place("P1", "Description1", 2, 5)
        output = "Place P1 already exists"

        with self.assertRaises(Exception) as context:
            self.petri_net.add_place("P1", "Description1", 2, 5)

        self.assertEqual(str(context.exception), output)

    def test_add_transition(self):
        self.petri_net.add_place("P1", "Description1", 1, 5)
        self.petri_net.add_place("P2", "Description2", 2, 4)
        self.petri_net.add_place("P3", "Description3", 0, 3)

        self.petri_net.add_transition("T1", {"P1": 1, "P2": 2}, {"P3": 3})

        self.assertEqual(list(self.petri_net.transitions.keys())[0], "T1")
        self.assertEqual(list(self.petri_net.transitions["T1"].inputs.keys())[0].name, "P1")
        self.assertEqual(list(self.petri_net.transitions["T1"].inputs.keys())[0].description, "Description1")
        self.assertEqual(list(self.petri_net.transitions["T1"].inputs.keys())[0].tokens, 1)
        self.assertEqual(list(self.petri_net.transitions["T1"].inputs.keys())[0].max_tokens, 5)
        self.assertEqual(list(self.petri_net.transitions["T1"].inputs.values())[0], 1)
        
        self.assertEqual(list(self.petri_net.transitions["T1"].inputs.keys())[1].name, "P2")
        self.assertEqual(list(self.petri_net.transitions["T1"].inputs.keys())[1].description, "Description2")
        self.assertEqual(list(self.petri_net.transitions["T1"].inputs.keys())[1].tokens, 2)
        self.assertEqual(list(self.petri_net.transitions["T1"].inputs.keys())[1].max_tokens, 4)
        self.assertEqual(list(self.petri_net.transitions["T1"].inputs.values())[1], 2)

        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.keys())[0].name, "P3")
        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.keys())[0].description, "Description3")
        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.keys())[0].tokens, 0)
        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.keys())[0].max_tokens, 3)
        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.values())[0], 3)

        with self.assertRaises(Exception) as context:
            self.petri_net.add_transition("T1", {"P1": 1}, {})

        self.assertEqual(str(context.exception), "Transition T1 already exists")
        
    def test_add_transition_2(self):
        self.petri_net.add_place("P1", "Description1", 1, 3)
        self.petri_net.add_place("P2", "Description2", 3, 6)
        self.petri_net.add_place("P3", "Description3", 0, 3)

        self.petri_net.add_transition("T1", {}, {"P1": 1, "P2": 2})
        self.petri_net.add_transition("T2", {"P3": 3}, {})

        self.assertEqual(list(self.petri_net.transitions.keys())[0], "T1")
        self.assertEqual(self.petri_net.transitions["T1"].inputs, {})

        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.keys())[0].name, "P1")
        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.keys())[0].description, "Description1")
        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.keys())[0].tokens, 1)
        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.keys())[0].max_tokens, 3)
        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.values())[0], 1)

        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.keys())[1].name, "P2")
        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.keys())[1].description, "Description2")
        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.keys())[1].tokens, 3)
        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.keys())[1].max_tokens, 6)
        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.values())[1], 2)

        self.assertEqual(list(self.petri_net.transitions.keys())[1], "T2")
        self.assertEqual(self.petri_net.transitions["T2"].outputs, {})

        self.assertEqual(list(self.petri_net.transitions["T2"].inputs.keys())[0].name, "P3")
        self.assertEqual(list(self.petri_net.transitions["T2"].inputs.keys())[0].description, "Description3")
        self.assertEqual(list(self.petri_net.transitions["T2"].inputs.keys())[0].tokens, 0)
        self.assertEqual(list(self.petri_net.transitions["T2"].inputs.keys())[0].max_tokens, 3)
        self.assertEqual(list(self.petri_net.transitions["T2"].inputs.values())[0], 3)

    def test_fire_transition(self):
        output = "Transition T2 does not exist"

        self.petri_net.add_place("P1", "Description1", 2, 5)
        self.petri_net.add_place("P2", "Description2", 2, 4)
        self.petri_net.add_place("P3", "Description3", 0, 3)

        self.petri_net.add_transition("T1", {"P1": 1, "P2": 2}, {"P3": 3})

        self.petri_net.fire_transition("T1")

        self.assertEqual(list(self.petri_net.transitions["T1"].inputs.keys())[0].tokens, 1)
        self.assertEqual(list(self.petri_net.transitions["T1"].inputs.keys())[1].tokens, 0)
        self.assertEqual(list(self.petri_net.transitions["T1"].outputs.keys())[0].tokens, 3)

        with self.assertRaises(Exception) as context:
            self.petri_net.fire_transition("T2")

        self.assertEqual(str(context.exception), output)

    def test_petri_net_str(self):

        output = """Places:
Place(P1, tokens=2, max_tokens=5)
Place(P2, tokens=2, max_tokens=4)
Place(P3, tokens=0, max_tokens=3)
Transitions:
Transition(T1, inputs=[P1: 1, P2: 2], outputs=[P3: 3])"""

        self.petri_net.add_place("P1", "Description1", 2, 5)
        self.petri_net.add_place("P2", "Description2", 2, 4)
        self.petri_net.add_place("P3", "Description3", 0, 3)

        self.petri_net.add_transition("T1", {"P1": 1, "P2": 2}, {"P3": 3})

        self.assertEqual(str(self.petri_net), output)


        
if __name__ == '__main__':
    unittest.main()
