"""Plain minimax vs alpha-beta: same answer, very different node counts."""
import chess
from tiny_engine import evaluate, negamax, MATE


# --8<-- [start:minimax]
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
# --8<-- [end:minimax]


if __name__ == "__main__":
    board = chess.Board("r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3")
    for depth in (1, 2, 3, 4):
        plain, n_plain = minimax_nodes(board, depth)
        stats = {"nodes": 0}
        ab = negamax(board, depth, -MATE - 1, MATE + 1, stats)
        print(f"depth {depth}: minimax={plain:+} ({n_plain:>7} nodes)  alpha-beta={ab:+} ({stats['nodes']:>6} nodes)")
