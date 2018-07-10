import unittest
import decipher


class TestDecipher(unittest.TestCase):

    def setUp(self):
        self.p1 = decipher.Player(1)

    def test_SetRemainingBoard(self):
        self.p1.word = 'GAMES'
        self.p1.SetRemainingBoard()
        self.assertEqual(self.p1.remaining, {1: 'B', 2: 'C', 3: 'D', 4: 'F', 5: 'H',
                                             6: 'I', 7: 'J', 8: 'K', 9: 'L', 10: 'N',
                                             11: 'O', 12: 'P', 13: 'Q', 14: 'R', 15: 'T',
                                             16: 'U', 17: 'V', 18: 'W', 19: 'XY', 20: 'Z'},
                         'Remaining letters are set incorrectly.')

        self.p1.word = 'FIXED'
        self.p1.SetRemainingBoard()
        self.assertEqual(self.p1.remaining, {1: 'A', 2: 'B', 3: 'C', 4: 'G', 5: 'H',
                                             6: 'J', 7: 'K', 8: 'L', 9: 'M', 10: 'N',
                                             11: 'O', 12: 'P', 13: 'Q', 14: 'R', 15: 'S',
                                             16: 'T', 17: 'U', 18: 'V', 19: 'W', 20: 'Z'},
                         'Check that XY is handled correctly.')

        self.p1.word = 'CHEWY'
        self.p1.SetRemainingBoard()
        self.assertEqual(self.p1.remaining, {1: 'A', 2: 'B', 3: 'D', 4: 'F', 5: 'G',
                                             6: 'I', 7: 'J', 8: 'K', 9: 'L', 10: 'M',
                                             11: 'N', 12: 'O', 13: 'P', 14: 'Q', 15: 'R',
                                             16: 'S', 17: 'T', 18: 'U', 19: 'V', 20: 'Z'},
                         'Check that XY is handled correctly.')

    def test_SetReceivedBoard(self):
        self.p1.SetReceivedBoard()
        self.assertEqual(self.p1.received, {1: '_', 2: '_', 3: '_', 4: '_', 5: '_',
                                            6: '_', 7: '_', 8: '_', 9: '_', 10: '_',
                                            11: '_', 12: '_', 13: '_', 14: '_', 15: '_',
                                            16: '_', 17: '_', 18: '_', 19: '_', 20: '_'})

    def test_ValidWord(self):
        self.assertFalse(self.p1.ValidWord(''), 'Empty string is not valid.')
        self.assertFalse(self.p1.ValidWord('ASDFGH'),
                         'Word must be exactly 5 letters.')
        self.assertFalse(self.p1.ValidWord('ASDF1'), 'Must use letters only.')
        self.assertFalse(self.p1.ValidWord('AASDD'), 'Cannot repeat letters.')
        self.assertFalse(self.p1.ValidWord(
            'EPOXY'), 'X and Y is considered one letter and cannot be used at the same time.')
        self.assertTrue(self.p1.ValidWord('ASDFG'),
                        '5 letter word. Letters cannot be repeated')


if __name__ == '__main__':
    unittest.main()
