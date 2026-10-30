"""A tiny chess engine: material + piece-square evaluation, negamax with alpha-beta."""
import chess

PIECE_VALUES = {
    chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
    chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0,
}

# Bonus (centipawns) for a white knight on each square, a1..h8. Mirrored for black.
KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
]

MATE = 100_000


# --8<-- [start:evaluate]
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
# --8<-- [end:evaluate]


def ordered_moves(board: chess.Board):
    """Captures first (most valuable victim, least valuable attacker) to help pruning."""
    def key(move):
        if board.is_capture(move):
            victim = board.piece_type_at(move.to_square) or chess.PAWN  # en passant
            attacker = board.piece_type_at(move.from_square)
            return -(10 * PIECE_VALUES[victim] - PIECE_VALUES[attacker])
        return 0
    return sorted(board.legal_moves, key=key)


def negamax(board: chess.Board, depth: int, alpha: int, beta: int, stats: dict) -> int:
    stats["nodes"] += 1
    if depth == 0 or board.is_game_over():
        return evaluate(board)
    best = -MATE - 1
    for move in ordered_moves(board):
        board.push(move)
        score = -negamax(board, depth - 1, -beta, -alpha, stats)
        board.pop()
        best = max(best, score)
        alpha = max(alpha, score)
        if alpha >= beta:  # the opponent would never allow this line
            break
    return best


def best_move(board: chess.Board, depth: int = 3):
    stats = {"nodes": 0}
    best, best_score = None, -MATE - 1
    alpha, beta = -MATE - 1, MATE + 1
    for move in ordered_moves(board):
        board.push(move)
        score = -negamax(board, depth - 1, -beta, -alpha, stats)
        board.pop()
        if score > best_score:
            best, best_score = move, score
        alpha = max(alpha, score)
    return best, best_score, stats["nodes"]


if __name__ == "__main__":
    board = chess.Board()
    while not board.is_game_over() and board.fullmove_number < 20:
        move, score, nodes = best_move(board, depth=3)
        print(f"{board.fullmove_number}. {board.san(move)}  eval={score:+}  nodes={nodes}")
        board.push(move)
    print(board)
