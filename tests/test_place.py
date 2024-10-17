import unittest
from unittest.mock import patch, call
from PyQt5.QtCore import QCoreApplication, QObject
from petri_nets.Place import Place

class TestPlace(unittest.TestCase):

    def setUp(self) -> None:
        self.place = Place(
            "P1", "Description1", tokens=5, ready_tokens=0, max_tokens=10, cooldown_ms=1000
        )

    @patch('PyQt5.QtCore.QTimer.singleShot')
    def test_tokens_changed(self, mock_singleShot):
        self.place.tokens = 7        

        self.assertEqual(mock_singleShot.call_count, 1)
        mock_singleShot.assert_called_with(1000, self.place.print_info)

    @patch('PyQt5.QtCore.QTimer.singleShot')
    def test_print_info_called_immediately(self, mock_singleShot):

        def fake_singleShot(_ms, callback):
            callback()

        mock_singleShot.side_effect = fake_singleShot

        self.place.tokens = 7

        self.assertEqual(self.place.ready_tokens, 7)
        self.assertEqual(self.place.tokens, 0)

    @patch('PyQt5.QtCore.QTimer.singleShot')
    def test_no_signal_when_tokens_same(self, mock_singleShot):
        self.place.tokens = 5

        self.assertEqual(mock_singleShot.call_count, 0)

if __name__ == '__main__':
    import sys
    app = QCoreApplication(sys.argv)
    unittest.main()

if __name__ == '__main__':
    unittest.main()
