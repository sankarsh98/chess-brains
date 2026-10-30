# How Computers Play Chess

A short, hands-on course. You will build a tiny chess engine in about 70 lines of Python, then see how it connects to Stockfish, AlphaZero and large language models.

## The big idea

A chess engine does two things:

1. **Search:** look ahead through possible moves and replies.
2. **Evaluate:** decide how good a position is when you stop looking.

Everything else, from bitboards to neural networks, makes one of these two faster or smarter.

## Course map

| Part | Question it answers |
|---|---|
| [1. Boards and moves](01-boards-and-moves.md) | How does a program know what's legal? |
| [2. Judging a position](02-evaluation.md) | How do you turn a position into a number? |
| [3. Looking ahead](03-minimax.md) | How do you choose a move assuming the opponent plays well? |
| [4. Pruning the tree](04-alpha-beta.md) | How do you skip 99% of the work? |
| [5. Modern engines](05-modern-engines.md) | What do Stockfish and Leela do differently? |
| [6. LLMs and chess](06-llms-and-chess.md) | Can a language model play chess? |

## Setup

```bash
uv venv && uv pip install chess
```

All the code lives in the `engine/` folder of the [repo](https://github.com/sankarsh98/chess-brains). Run each script as you read.

!!! tip "How to use this course"
    Don't just read. Each part ends with a small experiment. Change a number, predict what happens, then run it.

## More from this series

- [Thoughts: the notes garden](https://sankarsh98.github.io/garden/)
- [AI Systems](https://sankarsh98.github.io/ai-systems/): agents, MCP and inference efficiency
- [All sites](https://sankarsh98.github.io/)
