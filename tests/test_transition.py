import unittest

from PetrisNet import Place, Transition

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
        self.transition4 = Transition("T4", {self.place1: 1, self.place2: 2}, {self.place5: 2})

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
        self.assertTrue(self.transition2.is_enabled())

    def test_is_enabled_no(self):
        self.assertFalse(self.transition3.is_enabled())

    def test_can_fire_yes(self):
        self.assertTrue(self.transition1.can_fire())

    def test_can_fire_no(self):
        self.assertFalse(self.transition4.can_fire())

    def test_fire_working(self):
        self.transition1.fire()

        self.assertEqual(list(self.transition1.inputs.keys())[0].tokens, 2)
        self.assertEqual(list(self.transition1.inputs.keys())[1].tokens, 0)
        self.assertEqual(list(self.transition1.outputs.keys())[0].tokens, 2)

    def test_fire_exception_not_enabled(self):
        with self.assertRaises(Exception) as context:
            self.transition3.fire()
        
        self.assertEqual(str(context.exception), "Transition T3 is not enabled")

    def test_fire_exception_cannot_fire(self):
        with self.assertRaises(Exception) as context:
            self.transition4.fire()
        
        self.assertEqual(str(context.exception), "Transition T4 cannot fire due to max token constraints")

    def test_reverse_fire(self):
        self.transition1.fire()
        self.transition1.reverse_fire()

        self.assertEqual(list(self.transition1.inputs.keys())[0].tokens, 3)
        self.assertEqual(list(self.transition1.inputs.keys())[1].tokens, 2)
        self.assertEqual(list(self.transition1.outputs.keys())[0].tokens, 0)

    def test_transition_str(self):
        output = "Transition(T1, inputs=[P1: 1, P2: 2], outputs=[P3: 2])"

        self.assertEqual(str(self.transition1), output)

if __name__ == '__main__':
    unittest.main()