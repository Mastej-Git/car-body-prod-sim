import unittest

from petri_nets.Place import Place

class TestPlace(unittest.TestCase):

    def setUp(self) -> None:
        self.place = Place("P1", "Description1", tokens=3, ready_tokens=1, max_tokens=5, cooldown_ms=1)

    def test_init(self):
        self.assertEqual(self.place.name, "P1")
        self.assertEqual(self.place.description, "Description1")
        self.assertEqual(self.place.tokens, 3)
        self.assertEqual(self.place.ready_tokens, 1)
        self.assertEqual(self.place.max_tokens, 5)

        self.place.name = "P2"
        self.place.description = "Description2"
        self.place.tokens += 2
        self.place.max_tokens = 7

        self.assertEqual(self.place.name, "P2")
        self.assertEqual(self.place.description, "Description2")
        self.assertEqual(self.place.tokens, 2)
        self.assertEqual(self.place.ready_tokens, 1)
        self.assertEqual(self.place.max_tokens, 7)

    def test_place_str(self):
        output = "Place(P1, tokens=3, ready_tokens=1, max_tokens=5, cooldown_ms=1)"

        self.assertEqual(str(self.place), output)

if __name__ == '__main__':
    unittest.main()
