# 6. LLMs and chess

## Can a language model play chess?

A language model predicts the next token. A game is just text, so you can feed it moves in PGN notation:

```
1. e4 e5 2. Nf3 Nc6 3. Bb5
```

and ask for the next move. This works surprisingly well for the opening, because it has seen thousands of games and the opening theory in text form.

## Where it breaks down

| Issue | Why |
|---|---|
| **Illegal moves** | The model has no board state. It tracks the position implicitly from the move text. |
| **Blunders in tactics** | No search. It can't verify "if I go here, they take my queen". |
| **Long games drift** | Errors accumulate and the model can lose track of where pieces are. |

Some research has shown that models trained on game transcripts build an **internal representation of the board**. The Othello-GPT work found that a network trained only on move sequences developed a board-state representation, even though it was never shown the board.

## Better: use the model as a coach, not a player

The reliable pattern is to let each tool do what it's good at:

```
engine  ->  finds the best move and the evaluation  (search)
LLM     ->  explains *why* in plain language         (language)
```

For example, feed Stockfish's analysis of a game (evaluation swings, best lines) to an LLM and ask it to explain the turning points. This is a good project for your own PGN files.

## Project idea: analyse your own games

1. Read your PGN files with `python-chess`.
2. For each move, compute the evaluation with our tiny engine (or Stockfish via `chess.engine`).
3. Flag moves where the evaluation drops by 150+ centipawns (blunders).
4. Send each flagged position and the better move to an LLM and ask for a short explanation.

```python
import chess.pgn, chess.engine

with open("game.pgn") as f:
    game = chess.pgn.read_game(f)

engine = chess.engine.SimpleEngine.popen_uci("stockfish")
board = game.board()
for move in game.mainline_moves():
    before = engine.analyse(board, chess.engine.Limit(depth=12))["score"].white()
    board.push(move)
    after = engine.analyse(board, chess.engine.Limit(depth=12))["score"].white()
    print(board.fullmove_number, move, before, "->", after)
```

!!! tip
    You need the Stockfish binary installed (`sudo apt install stockfish`) for the snippet above. Check the path with `which stockfish`.
