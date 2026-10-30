---
title: "3. Looking ahead: minimax"
---

## The idea

You choose the move that leads to the best outcome **assuming your opponent also chooses their best reply**. White tries to maximise the score, Black tries to minimise it.

```
        White to move
       /      |       \
     Ma       Mb       Mc          <- White picks the max
    /  \     /  \     /  \
  +3   +1   +2   +5  -2   +4       <- Black replies; Black picks the min
```

Black would answer Ma with +1 (the min of 3, 1), Mb with +2, and Mc with -2. White picks the best of those: **Mb, worth +2**.

## Negamax: one function for both sides

Because chess is zero-sum, one player's score is the negative of the other's. So we can write a single function:

$$\text{score}(p) = \max_{m}\; -\text{score}(p \cdot m)$$

Each recursion flips the sign. No separate max and min branches.

## Plain minimax in code

```python
def minimax_nodes(board, depth):
    if depth == 0 or board.is_game_over():
        return evaluate(board), 1
    best, nodes = -MATE - 1, 1
    for move in board.legal_moves:
        board.push(move)
        score, n = minimax_nodes(board, depth - 1)
        board.pop()
        best, nodes = max(best, -score), nodes + n
    return best, nodes
```

## The problem: explosion

With about 30 legal moves per position, looking *d* plies ahead visits roughly $30^d$ positions:

| Depth | Nodes (approx.) |
|---|---|
| 2 | 900 |
| 4 | 810,000 |
| 6 | 729,000,000 |
| 8 | 656,000,000,000 |

Our plain minimax measured **775,804 nodes at depth 4**. That's about what the formula predicts, and far too slow to go deeper.

> [!question] Experiment
> Run `compare_search.py` at depth 5. How long does plain minimax take compared with depth 4? That ratio is your *effective branching factor*.
