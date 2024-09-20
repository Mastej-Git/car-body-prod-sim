import unittest

from body_parts.CupHolder import CupHolder

class TestCupHolder(unittest.TestCase):
    
    def setUp(self) -> None:
        self.cup_holder = CupHolder("Tak", "Czerwony")

    def test_init(self):
        self.assertEqual(self.cup_holder.usb_socket, "Tak")
        self.assertEqual(self.cup_holder.color, "Czerwony")

        self.cup_holder.usb_socket = "Nie"
        self.cup_holder.color = "Zielony"

        self.assertEqual(self.cup_holder.usb_socket, "Nie")
        self.assertEqual(self.cup_holder.color, "Zielony")

    def test_check_activation(self):
        self.assertFalse(self.cup_holder.is_activated)
        self.cup_holder.check_activation()
        self.assertTrue(self.cup_holder.is_activated)

    def test_remove_parameters(self):
        self.cup_holder.check_activation()

        self.assertEqual(self.cup_holder.usb_socket, "Tak")
        self.assertEqual(self.cup_holder.color, "Czerwony")
        self.assertTrue(self.cup_holder.is_activated)

        self.cup_holder.remove_parameters()

        self.assertEqual(self.cup_holder.usb_socket, "")
        self.assertEqual(self.cup_holder.color, "")
        self.assertFalse(self.cup_holder.is_activated)

if __name__ == '__main__':
    unittest.main()
