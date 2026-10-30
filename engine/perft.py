"""Perft: count leaf positions at a given depth. A classic move-generator test."""
import chess


def perft(board: chess.Board, depth: int) -> int:
    if depth == 0:
        return 1
    total = 0
    for move in board.legal_moves:
        board.push(move)
        total += perft(board, depth - 1)
        board.pop()
    return total


if __name__ == "__main__":
    for d in range(1, 5):
        print(d, perft(chess.Board(), d))
