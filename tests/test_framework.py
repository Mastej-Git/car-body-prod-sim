import unittest

from body_parts.Framework import Framework

class TestFramework(unittest.TestCase):
    
    def setUp(self) -> None:
        self.armrest = Framework("Skóra", "Czerwony")

    def test_init(self):

        self.assertEqual(self.armrest.material, "Skóra")
        self.assertEqual(self.armrest.color, "Czerwony")

        self.armrest.material = "Eko-skóra"
        self.armrest.color = "Zielony"

        self.assertEqual(self.armrest.material, "Eko-skóra")
        self.assertEqual(self.armrest.color, "Zielony")

    def test_check_activation(self):
        self.assertFalse(self.armrest.is_activated)
        self.armrest.check_activation()
        self.assertTrue(self.armrest.is_activated)

    def test_remove_parameters(self):
        self.armrest.check_activation()

        self.assertEqual(self.armrest.material, "Skóra")
        self.assertEqual(self.armrest.color, "Czerwony")
        self.assertTrue(self.armrest.is_activated)

        self.armrest.remove_parameters()

        self.assertEqual(self.armrest.material, "")
        self.assertEqual(self.armrest.color, "")
        self.assertFalse(self.armrest.is_activated)

if __name__ == '__main__':
    unittest.main()
