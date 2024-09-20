import unittest

from body_parts.MiddlePanel import MiddlePanel

class TestMiddlePanel(unittest.TestCase):
    
    def setUp(self) -> None:
        self.middle_panel = MiddlePanel("Interfejs multimedialny")

    def test_init(self):
        self.assertEqual(self.middle_panel.functionality, "Interfejs multimedialny")

        self.middle_panel.functionality = "Schowek"

        self.assertEqual(self.middle_panel.functionality, "Schowek")

    def test_check_activation(self):
        self.assertFalse(self.middle_panel.is_activated)
        self.middle_panel.check_activation()
        self.assertTrue(self.middle_panel.is_activated)

    def test_remove_parameters(self):
        self.middle_panel.check_activation()

        self.assertEqual(self.middle_panel.functionality, "Interfejs multimedialny")
        self.assertTrue(self.middle_panel.is_activated)

        self.middle_panel.remove_parameters()

        self.assertEqual(self.middle_panel.functionality, "")
        self.assertFalse(self.middle_panel.is_activated)

if __name__ == '__main__':
    unittest.main()