import unittest

from body_parts.LowerPanel import LowerPanel

class TestLowerPanel(unittest.TestCase):
    
    def setUp(self) -> None:
        self.lower_panel = LowerPanel("Ładowarka bezprzewodowa", "Tak", "Czerwony")

    def test_init(self):
        self.assertEqual(self.lower_panel.functionality, "Ładowarka bezprzewodowa")
        self.assertEqual(self.lower_panel.is_cup, "Tak")
        self.assertEqual(self.lower_panel.color, "Czerwony")

        self.lower_panel.functionality = "Schowek"
        self.lower_panel.is_cup = "Nie"
        self.lower_panel.color = "Zielony"

        self.assertEqual(self.lower_panel.functionality, "Schowek")
        self.assertEqual(self.lower_panel.is_cup, "Nie")
        self.assertEqual(self.lower_panel.color, "Zielony")

    def test_check_activation(self):
        self.assertFalse(self.lower_panel.is_activated)
        self.lower_panel.check_activation()
        self.assertTrue(self.lower_panel.is_activated)

    def test_remove_parameters(self):
        self.lower_panel.check_activation()

        self.assertEqual(self.lower_panel.functionality, "Ładowarka bezprzewodowa")
        self.assertEqual(self.lower_panel.is_cup, "Tak")
        self.assertEqual(self.lower_panel.color, "Czerwony")
        self.assertTrue(self.lower_panel.is_activated)

        self.lower_panel.remove_parameters()

        self.assertEqual(self.lower_panel.functionality, "")
        self.assertEqual(self.lower_panel.is_cup, "")
        self.assertEqual(self.lower_panel.color, "")
        self.assertFalse(self.lower_panel.is_activated)

if __name__ == '__main__':
    unittest.main()