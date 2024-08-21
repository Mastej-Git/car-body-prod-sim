import unittest

from PetrisNet import Place, Transition

class TestPlace(unittest.TestCase):

    def setUp(self) -> None:
        self.place = Place("P1", tokens=3, max_tokens=5)

    def test_init(self):
        self.assertEqual(self.place.name, "P1")
        self.assertEqual(self.place.tokens, 3)
        self.assertEqual(self.place.max_tokens, 5)

        self.place.name = "P2"
        self.place.tokens = 2
        self.place.max_tokens = 7

        self.assertEqual(self.place.name, "P2")
        self.assertEqual(self.place.tokens, 2)
        self.assertEqual(self.place.max_tokens, 7)

    def test_str(self):
        output = "Place(P1, tokens=3, max_tokens=5)"

        self.assertEqual(str(self.place), output)
        

class TestTransition(unittest.TestCase):
    
    def setUp(self) -> None:
        self.place1 = Place("P1", 3, 3)
        self.place2 = Place("P2", 2, 2)
        self.place3 = Place("P3", 0, 2)
        self.place4 = Place("P4", 0, 2)
        self.place5 = Place("P5", 1, 2)
        
        self.transition1 = Transition("T1", {self.place1: 1, self.place2: 2}, {self.place3: 2})
        self.transition2 = Transition("T2", {}, {})
        self.transition3 = Transition("T3", {self.place1: 1, self.place4: 2}, {self.place3: 2})

    def test_init_normal(self):

        self.assertEqual(self.transition1.name, "T1")
        self.assertEqual(self.transition1.inputs[self.place1], 1)
        self.assertEqual(self.transition1.inputs[self.place2], 2)
        self.assertEqual(self.transition1.outputs[self.place3], 2)

    def test_init_no_inputs_no_outputs(self):

        self.assertEqual(self.transition2.name, "T2")
        self.assertEqual(self.transition2.inputs, {})
        self.assertEqual(self.transition2.outputs, {})

    def test_is_enabled_yes(self):
        self.assertTrue(self.transition1.is_enabled())

    def test_is_enabled_no(self):
        self.assertFalse(self.transition3.is_enabled())

if __name__ == '__main__':
    unittest.main()