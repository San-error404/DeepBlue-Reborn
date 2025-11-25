import chess

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}

def evaluate(board: chess.Board):
    if board.is_checkmate():
        return -999999 if board.turn else 999999
    if board.is_stalemate():
        return 0

    score = 0

    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if not piece:
            continue

        value = piece_values[piece.piece_type]
        score += value if piece.color == chess.WHITE else -value

    return score if board.turn else -score
