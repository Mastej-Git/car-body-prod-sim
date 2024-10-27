import unittest
from unittest.mock import patch

from petri_nets.Place import Place
from petri_nets.Transition import Transition

class TestTransition(unittest.TestCase):
    
    def setUp(self) -> None:
        self.place1 = Place("P1", "Description1", tokens=0, ready_tokens=1, max_tokens=3, cooldown_ms=1)
        self.place2 = Place("P2", "Description2", tokens=0, ready_tokens=2, max_tokens=2, cooldown_ms=1)
        self.place3 = Place("P3", "Description3", tokens=0, ready_tokens=0, max_tokens=2, cooldown_ms=1)
        self.place4 = Place("P4", "Description4", tokens=0, ready_tokens=0, max_tokens=2, cooldown_ms=1)
        self.place5 = Place("P5", "Description5", tokens=0, ready_tokens=1, max_tokens=2, cooldown_ms=1)
        
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

    @patch('PyQt5.QtCore.QTimer.singleShot')
    def test_fire_working(self, mock_single_shot):
        def fake_single_shot(_ms, callback):
            callback()

        mock_single_shot.side_effect = fake_single_shot

        self.transition1.fire()

        self.assertEqual(list(self.transition1.inputs.keys())[0].ready_tokens, 0)
        self.assertEqual(list(self.transition1.inputs.keys())[1].ready_tokens, 0)
        self.assertEqual(list(self.transition1.outputs.keys())[0].ready_tokens, 2)

    def test_fire_exception_not_enabled(self):
        output = "Transition T3 is not enabled"

        with self.assertRaises(Exception) as context:
            self.transition3.fire()
        
        self.assertEqual(str(context.exception), output)

    def test_fire_exception_cannot_fire(self):
        output = "Transition T4 cannot fire due to max token constraints"

        with self.assertRaises(Exception) as context:
            self.transition4.fire()
        
        self.assertEqual(str(context.exception), output)

    @patch('PyQt5.QtCore.QTimer.singleShot')
    def test_reverse_fire(self, mock_single_shot):
        def fake_single_shot(_ms, callback):
            callback()

        mock_single_shot.side_effect = fake_single_shot

        self.transition1.fire()
        self.transition1.reverse_fire()

        self.assertEqual(list(self.transition1.inputs.keys())[0].ready_tokens, 1)
        self.assertEqual(list(self.transition1.inputs.keys())[1].ready_tokens, 2)
        self.assertEqual(list(self.transition1.outputs.keys())[0].tokens, 0)

    def test_transition_str(self):
        output = "Transition(T1, inputs=[P1: 1, P2: 2], outputs=[P3: 2])"

        self.assertEqual(str(self.transition1), output)

if __name__ == '__main__':
    unittest.main()
    