# 1. Boards and moves

## Representing a position

A position needs: piece placement, side to move, castling rights, en passant square, and move counters. The standard text form is **FEN**:

```
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
```

Ranks run from 8 down to 1. Digits are runs of empty squares. Uppercase is White.

## Bitboards

Serious engines store each piece type as a **64-bit integer**, one bit per square. White pawns on their starting rank:

```
00000000 00000000 00000000 00000000 00000000 00000000 11111111 00000000
```

Moving every pawn forward one square is a single shift: `pawns << 8`. Checking which squares a rook attacks uses lookup tables and bit tricks. This is why engines search millions of positions per second.

!!! info "Why 64 bits?"
    A chessboard has 64 squares, so a 64-bit word covers it exactly. CPUs operate on whole words in one instruction, so you process all 64 squares at once.

## Generating moves

We'll use the `python-chess` library, which handles the rules for us:

```python
import chess

board = chess.Board()
print(board.legal_moves.count())   # 20
for move in board.legal_moves:
    print(board.san(move), end=" ")
```

## Perft: testing a move generator

**Perft** counts every leaf position reachable in exactly *n* moves. The right answers are well known, so any bug in move generation shows up as a wrong number.

```python
--8<-- "engine/perft.py"
```

Output:

| Depth | Positions |
|---|---|
| 1 | 20 |
| 2 | 400 |
| 3 | 8,902 |
| 4 | 197,281 |
| 5 | 4,865,609 |

The count grows by about 20-30x per ply. That growth is the central problem of computer chess.

!!! question "Experiment"
    Run perft from the position after `1. e4`. Predict the depth-1 count first. Then try the position `r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1` (famous as "Kiwipete") and look up its known counts online.
