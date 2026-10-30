---
title: "Exercises"
---

Roughly in order of difficulty.

## Warm-up

1. Run `perft.py` to depth 5. How long does it take? Estimate depth 6 from the growth rate.
2. Change `PIECE_VALUES` so a bishop is worth 300 instead of 330. Does the opening choice change?
3. Print the evaluation of the starting position. Why is it 0?

## Intermediate

4. Add **piece-square tables** for pawns and the king. For the king, use different tables for the middlegame and the endgame.
5. Implement **iterative deepening** with a time limit, and return the best move found so far.
6. Add a **transposition table** using `chess.polyglot.zobrist_hash(board)` as the key. Measure the node reduction.
7. Add **quiescence search**: at depth 0, keep searching captures until none remain. Test with a position where a queen can be captured by a pawn at the horizon.

## Challenge

8. Play your engine against Stockfish limited to `Skill Level 0` using `chess.engine`. Play 20 games and estimate the win rate.
9. Build the **LLM coach** from part 6 for your own games.
10. Train a tiny evaluation network: generate positions from random games, label them with Stockfish at depth 8, and fit a small PyTorch MLP. Compare it with the hand-written evaluation.

> [!success] Where this leads
> Exercise 10 is the core of how NNUE works. Once you've done it, you understand the main idea behind modern engines.
