"""Connect Four in the terminal against a minimax AI with alpha-beta pruning.

    python connect4.py              # you are X, the AI is O
    python connect4.py --depth 6    # stronger (slower) AI
"""
import argparse
import math

ROWS, COLS = 6, 7
EMPTY, HUMAN, AI = ".", "X", "O"
ORDER = [3, 2, 4, 1, 5, 0, 6]  # centre first: better pruning and better play


def new_board():
    return [[EMPTY] * COLS for _ in range(ROWS)]


def valid_moves(b):
    return [c for c in ORDER if b[0][c] == EMPTY]


def drop(b, col, piece):
    """Return a new board with piece dropped in col."""
    nb = [row[:] for row in b]
    for r in range(ROWS - 1, -1, -1):
        if nb[r][col] == EMPTY:
            nb[r][col] = piece
            return nb
    raise ValueError("column full")


def windows(b):
    for r in range(ROWS):
        for c in range(COLS):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                er, ec = r + 3 * dr, c + 3 * dc
                if 0 <= er < ROWS and 0 <= ec < COLS:
                    yield [b[r + i * dr][c + i * dc] for i in range(4)]


def winner(b):
    for w in windows(b):
        if w[0] != EMPTY and w.count(w[0]) == 4:
            return w[0]
    return None


def score_window(w, piece):
    opp = HUMAN if piece == AI else AI
    if w.count(piece) == 3 and w.count(EMPTY) == 1:
        return 5
    if w.count(piece) == 2 and w.count(EMPTY) == 2:
        return 2
    if w.count(opp) == 3 and w.count(EMPTY) == 1:
        return -4
    return 0


def evaluate(b):
    centre = [b[r][COLS // 2] for r in range(ROWS)]
    return 3 * centre.count(AI) + sum(score_window(w, AI) for w in windows(b))


def minimax(b, depth, alpha, beta, maximising):
    win, moves = winner(b), valid_moves(b)
    if win == AI:
        return None, 1_000_000 + depth  # prefer faster wins
    if win == HUMAN:
        return None, -1_000_000 - depth
    if not moves:
        return None, 0
    if depth == 0:
        return None, evaluate(b)
    best_col = moves[0]
    if maximising:
        best = -math.inf
        for c in moves:
            _, s = minimax(drop(b, c, AI), depth - 1, alpha, beta, False)
            if s > best:
                best, best_col = s, c
            alpha = max(alpha, best)
            if alpha >= beta:
                break
    else:
        best = math.inf
        for c in moves:
            _, s = minimax(drop(b, c, HUMAN), depth - 1, alpha, beta, True)
            if s < best:
                best, best_col = s, c
            beta = min(beta, best)
            if alpha >= beta:
                break
    return best_col, best


def ai_move(b, depth=5):
    return minimax(b, depth, -math.inf, math.inf, True)[0]


def show(b):
    print("\n" + "\n".join(" ".join(r) for r in b) + "\n" + " ".join(map(str, range(1, COLS + 1))))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--depth", type=int, default=5)
    depth = p.parse_args().depth
    b = new_board()
    while True:
        show(b)
        try:
            col = int(input("Your column (1-7): ")) - 1
            if col not in range(COLS) or b[0][col] != EMPTY:
                raise ValueError
        except ValueError:
            print("Invalid move.")
            continue
        b = drop(b, col, HUMAN)
        if winner(b) or not valid_moves(b):
            break
        b = drop(b, ai_move(b, depth), AI)
        if winner(b) or not valid_moves(b):
            break
    show(b)
    print({HUMAN: "You win!", AI: "The AI wins!"}.get(winner(b), "Draw."))


if __name__ == "__main__":
    main()
