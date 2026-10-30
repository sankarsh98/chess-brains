---
title: "4. Pruning the tree: alpha-beta"
---

## The insight

Suppose you've found a move that guarantees you +2. Now you examine another move and discover that the opponent has a reply that holds you to +1. You can **stop looking at that move immediately**. It's already worse than what you have, and it doesn't matter by how much.

Alpha-beta tracks two bounds:

- **alpha:** the best score I can already guarantee.
- **beta:** the best score the opponent can already guarantee. If my score reaches beta, the opponent would never allow this line, so I stop.

```python
if alpha >= beta:   # the opponent would never allow this line
    break
```

## Move ordering matters

Pruning works best when you examine the **best moves first**. If the first move is the best, every other branch gets cut quickly. Our engine orders captures first, using MVV-LVA (most valuable victim, least valuable attacker). Real engines add killer moves, history heuristics, and the best move from the previous, shallower search.

## The whole engine

```python
"""A tiny chess engine: material + piece-square evaluation, negamax with alpha-beta."""
import chess

PIECE_VALUES = {
    chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
    chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0,
}

# Bonus (centipawns) for a white knight on each square, a1..h8. Mirrored for black.
KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
]

MATE = 100_000


def evaluate(board: chess.Board) -> int:
    """Score in centipawns from the point of view of the side to move."""
    if board.is_checkmate():
        return -MATE
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    score = 0
    for square, piece in board.piece_map().items():
        value = PIECE_VALUES[piece.piece_type]
        if piece.piece_type == chess.KNIGHT:
            idx = square if piece.color == chess.WHITE else chess.square_mirror(square)
            value += KNIGHT_TABLE[idx]
        score += value if piece.color == chess.WHITE else -value
    return score if board.turn == chess.WHITE else -score


def ordered_moves(board: chess.Board):
    """Captures first (most valuable victim, least valuable attacker) to help pruning."""
    def key(move):
        if board.is_capture(move):
            victim = board.piece_type_at(move.to_square) or chess.PAWN  # en passant
            attacker = board.piece_type_at(move.from_square)
            return -(10 * PIECE_VALUES[victim] - PIECE_VALUES[attacker])
        return 0
    return sorted(board.legal_moves, key=key)


def negamax(board: chess.Board, depth: int, alpha: int, beta: int, stats: dict) -> int:
    stats["nodes"] += 1
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    best = -MATE - 1
    for move in ordered_moves(board):
        board.push(move)
        score = -negamax(board, depth - 1, -beta, -alpha, stats)
        board.pop()
        best = max(best, score)
        alpha = max(alpha, score)
        if alpha >= beta:  # the opponent would never allow this line
            break
    return best


def best_move(board: chess.Board, depth: int = 3):
    stats = {"nodes": 0}
    best, best_score = None, -MATE - 1
    alpha, beta = -MATE - 1, MATE + 1
    for move in ordered_moves(board):
        board.push(move)
        score = -negamax(board, depth - 1, -beta, -alpha, stats)
        board.pop()
        if score > best_score:
            best, best_score = move, score
        alpha = max(alpha, score)
    return best, best_score, stats["nodes"]


if __name__ == "__main__":
    board = chess.Board()
    while not board.is_game_over() and board.fullmove_number < 20:
        move, score, nodes = best_move(board, depth=3)
        print(f"{board.fullmove_number}. {board.san(move)}  eval={score:+}  nodes={nodes}")
        board.push(move)
    print(board)
```

## Same answer, far less work

Running `compare_search.py` from the repo:

| Depth | Plain minimax | Alpha-beta | Same score? |
|---|---|---|---|
| 1 | 28 | 28 | yes |
| 2 | 863 | 188 | yes |
| 3 | 24,942 | 1,258 | yes |
| 4 | 775,804 | 9,500 | yes |

At depth 4, alpha-beta visits about **1.2%** of the nodes and returns exactly the same result. The savings grow with depth. With perfect ordering, alpha-beta searches about $\sqrt{N}$ nodes, so it can look **twice as deep** in the same time.

## Why does it play oddly?

Run `tiny_engine.py` and watch the moves. It grabs material and then **shuffles rooks around**. That's expected: with only material and a knight table, once nothing can be won within three plies, every quiet move scores the same.

> [!question] Experiment
> Add a **pawn advancement bonus** (e.g. +5 per rank) to `evaluate`. Does the engine stop shuffling? Next, try depth 4 and see how long a move takes.

## What engines add on top

- **Iterative deepening:** search depth 1, then 2, then 3, and so on. It sounds wasteful, but the earlier results improve move ordering, and you can stop whenever time runs out.
- **Transposition table:** cache positions you've already analysed, since different move orders reach the same position.
- **Quiescence search:** don't stop in the middle of a capture sequence. Keep searching captures until the position is quiet.
- **Null-move pruning and late-move reductions:** search unpromising moves less deeply.
