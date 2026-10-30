# 4. Pruning the tree: alpha-beta

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
--8<-- "engine/tiny_engine.py"
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

!!! question "Experiment"
    Add a **pawn advancement bonus** (e.g. +5 per rank) to `evaluate`. Does the engine stop shuffling? Next, try depth 4 and see how long a move takes.

## What engines add on top

- **Iterative deepening:** search depth 1, then 2, then 3, and so on. It sounds wasteful, but the earlier results improve move ordering, and you can stop whenever time runs out.
- **Transposition table:** cache positions you've already analysed, since different move orders reach the same position.
- **Quiescence search:** don't stop in the middle of a capture sequence. Keep searching captures until the position is quiet.
- **Null-move pruning and late-move reductions:** search unpromising moves less deeply.
