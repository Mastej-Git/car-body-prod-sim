import unittest

from body_parts.UpperPanel import UpperPanel

class TestUpperPanel(unittest.TestCase):
    
    def setUp(self) -> None:
        self.upper_panel = UpperPanel("Tak", "4-strefowa")

    def test_init(self):
        self.assertEqual(self.upper_panel.is_controlable, "Tak")
        self.assertEqual(self.upper_panel.ac_type, "4-strefowa")

        self.upper_panel.is_controlable = "Nie"
        self.upper_panel.ac_type = "2-strefowa"

        self.assertEqual(self.upper_panel.is_controlable, "Nie")
        self.assertEqual(self.upper_panel.ac_type, "2-strefowa")

    def test_check_activation(self):
        self.assertFalse(self.upper_panel.is_activated)
        self.upper_panel.check_activation()
        self.assertTrue(self.upper_panel.is_activated)

    def test_remove_parameters(self):
        self.upper_panel.check_activation()

        self.assertEqual(self.upper_panel.is_controlable, "Tak")
        self.assertEqual(self.upper_panel.ac_type, "4-strefowa")
        self.assertTrue(self.upper_panel.is_activated)

        self.upper_panel.remove_parameters()

        self.assertEqual(self.upper_panel.is_controlable, "")
        self.assertEqual(self.upper_panel.ac_type, "")
        self.assertFalse(self.upper_panel.is_activated)

if __name__ == '__main__':
    unittest.main()
