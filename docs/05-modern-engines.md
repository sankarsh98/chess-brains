---
title: "5. Modern engines"
---

## Stockfish: search plus a small neural net

Stockfish is still an alpha-beta engine at heart. Since 2020 it evaluates positions with **NNUE** (Efficiently Updatable Neural Network).

- The network is small and runs on a **CPU**, no GPU needed.
- It's *efficiently updatable*: when one piece moves, only a few input neurons change, so the first layer is updated incrementally instead of being recomputed.
- It's trained on millions of positions scored by deep searches.

The result is a hand-written search paired with a learned evaluation, running at tens of millions of nodes per second.

## AlphaZero and Leela: learning from self-play

DeepMind's **AlphaZero** (2017) took a different path:

| | Stockfish | AlphaZero / Leela |
|---|---|---|
| Search | Alpha-beta | Monte Carlo tree search (MCTS) |
| Evaluation | Small NNUE net | Large deep network |
| Hardware | CPU | GPU / TPU |
| Nodes per second | Tens of millions | Tens of thousands |
| Learning | Trained on engine-scored positions | Reinforcement learning via self-play from scratch |

AlphaZero received only the rules. After a few hours of playing itself, it beat Stockfish 8. The open-source project **Leela Chess Zero** (Lc0) reproduced the approach with volunteer compute.

## MCTS in one paragraph

Instead of searching every move to a fixed depth, MCTS repeatedly walks down the tree, preferring moves the network thinks are promising (the **policy**) and moves it hasn't tried much. At a leaf, the network gives a position value (the **value**). That value flows back up the tree. Over thousands of simulations, the most-visited move becomes the choice.

## The two networks, in short

- **Policy head:** "which moves look worth considering?" This replaces move ordering.
- **Value head:** "who's winning?" This replaces the hand-written evaluation.

> [!info] Pattern worth noticing
> Both engines pair a search with a learned estimate. The difference is how much weight each side carries. Stockfish leans on brute-force search with a small net, while Leela leans on a big net with a lean search. The same trade-off shows up across modern AI.

## Strength today

Top engines are rated well above 3500 Elo, while the best human is around 2800-2900. A phone running Stockfish beats every human alive.
