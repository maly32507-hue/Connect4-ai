import unittest
from connect4 import *


def board(rows):
    return [list(r) for r in rows]


class Tests(unittest.TestCase):
    def test_vertical_win(self):
        b = new_board()
        for _ in range(4):
            b = drop(b, 0, HUMAN)
        self.assertEqual(winner(b), HUMAN)

    def test_diagonal_win(self):
        b = board(["......." , "......." , "...X...", "..XO...", ".XOO...", "XOOX..."])
        self.assertEqual(winner(b), HUMAN)

    def test_ai_takes_winning_move(self):
        b = board(["......." , "......." , "......." , "O......", "O.X....", "O.XX..."])
        self.assertEqual(ai_move(b, 4), 0)

    def test_ai_blocks_opponent_win(self):
        b = board(["......." , "......." , "......." , "......." , "..O....", "XXX.O.."])
        self.assertEqual(ai_move(b, 4), 3)

    def test_full_column_rejected(self):
        b = new_board()
        for i in range(ROWS):
            b = drop(b, 0, HUMAN if i % 2 else AI)
        self.assertNotIn(0, valid_moves(b))


if __name__ == "__main__":
    unittest.main()
