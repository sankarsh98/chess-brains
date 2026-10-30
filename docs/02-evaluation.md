---
title: "2. Judging a position"
---

When the search stops, the engine needs a number: who's better, and by how much? This is the **evaluation function**. Scores are in **centipawns**, where 100 is roughly one pawn.

## Material

The classic starting point:

| Piece | Value |
|---|---|
| Pawn | 100 |
| Knight | 320 |
| Bishop | 330 |
| Rook | 500 |
| Queen | 900 |

Material alone already plays recognizable chess, but it makes poor choices when nothing can be captured.

## Piece-square tables

Where a piece stands matters. A knight in the centre attacks up to 8 squares, while a knight on the rim attacks 4 or fewer ("a knight on the rim is dim"). A **piece-square table** gives each square a bonus or penalty:

```python
KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   5,   5,   0, -20, -40,
    ...
]
```

For Black we look up the *mirrored* square, so one table serves both colours.

## Negamax convention

Our evaluation returns the score **from the side to move's point of view**. This lets the search use a single function for both players, which part 3 explains.

```python
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
```

> [!note]
> The full file is shown in part 4. The snippet above is the `evaluate` function.

## What real engines add

Beyond material and squares, classical evaluations score pawn structure (doubled, isolated, passed pawns), king safety, mobility, bishop pairs, and rooks on open files. Stockfish today replaces most of this with a neural network (see [part 5](05-modern-engines.md)).

> [!question] Experiment
> Set every knight-table value to 0 and compare the engine's opening moves with the original. Does it still develop knights toward the centre?
