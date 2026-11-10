connect4-ai
Connect Four in the terminal against an AI opponent that looks ahead using minimax with alpha-beta pruning.

How the AI works
Minimax searches possible future moves, assuming you play your best and the AI plays its best.
Alpha-beta pruning skips branches that cannot change the result, so the search goes deeper in the same time.
Move ordering tries the centre columns first, which improves pruning and play.
Evaluation function scores positions at the search limit: it rewards centre control and open three-in-a-rows, and penalises the opponent's.
Faster wins score higher, so the AI finishes the game instead of delaying a win.
Play
Requires Python 3.8 or newer. No dependencies.

python connect4.py              # you are X, the AI is O
python connect4.py --depth 6    # stronger, slower AI
Type a column number from 1 to 7 to drop a piece.

Tests
python -m unittest test_connect4 -v
The tests cover vertical and diagonal wins, the AI taking a winning move, the AI blocking yours, and full columns.

Ideas for extending it
Add a transposition table to cache positions
Let the player choose who moves first
Build a graphical version
