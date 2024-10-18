import unittest
from unittest.mock import patch

from petri_nets.Place import Place

class TestPlace(unittest.TestCase):

    def setUp(self) -> None:
        self.place = Place(
            "P1", "Description1", tokens=5, ready_tokens=0, max_tokens=10, cooldown_ms=1000
        )

    @patch('PyQt5.QtCore.QTimer.singleShot')
    def test_tokens_changed(self, mock_single_shot):
        self.place.tokens = 7        

        self.assertEqual(mock_single_shot.call_count, 1)
        mock_single_shot.assert_called_with(1000, self.place.print_info)

    @patch('PyQt5.QtCore.QTimer.singleShot')
    def test_print_info_called_immediately(self, mock_single_shot):

        def fake_single_shot(_ms, callback):
            callback()

        mock_single_shot.side_effect = fake_single_shot

        self.place.tokens = 7

        self.assertEqual(self.place.ready_tokens, 7)
        self.assertEqual(self.place.tokens, 0)

    @patch('PyQt5.QtCore.QTimer.singleShot')
    def test_no_signal_when_tokens_same(self, mock_single_shot):
        self.place.tokens = 5

        self.assertEqual(mock_single_shot.call_count, 0)

if __name__ == '__main__':
    unittest.main()
