import chess

# Valeurs de base des pièces
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}

# Poids des critères supplémentaires
WEIGHTS = {
    "king_safety": 50,
    "pawn_structure": 20,
    "mobility": 10,
    "bishop_pair": 30,
    "center_control": 15,
}

def evaluate(board: chess.Board) -> int:
    """
    Évaluation globale comme Deep Blue (simplifié)
    Retourne un score positif si avantage blanc, négatif si avantage noir.
    """
    score = material(board)
    score += WEIGHTS["king_safety"] * king_safety(board)
    score += WEIGHTS["pawn_structure"] * pawn_structure(board)
    score += WEIGHTS["mobility"] * mobility(board)
    score += WEIGHTS["bishop_pair"] * bishop_pair(board)
    score += WEIGHTS["center_control"] * center_control(board)

    # Toujours du point de vue du joueur à qui c'est le tour
    return score if board.turn == chess.WHITE else -score

# --------------------------
# Fonctions détaillées
# --------------------------

def material(board: chess.Board) -> int:
    """Valeur matérielle classique"""
    score = 0
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if piece:
            value = PIECE_VALUES[piece.piece_type]
            score += value if piece.color == chess.WHITE else -value
    return score

def king_safety(board: chess.Board) -> int:
    """Score simplifié basé sur la sécurité du roi"""
    score = 0
    for color in [chess.WHITE, chess.BLACK]:
        king_sq = board.king(color)
        if king_sq is None:
            continue
        # Compter le nombre de cases autour du roi vides
        safe = 0
        for sq in board.attacks(king_sq):
            if board.piece_at(sq) is None:
                safe += 1
        score += safe if color == chess.WHITE else -safe
    return score

def pawn_structure(board: chess.Board) -> int:
    """Évalue les pions doublés, isolés (simplifié)"""
    score = 0
    for color in [chess.WHITE, chess.BLACK]:
        pawns = board.pieces(chess.PAWN, color)
        for sq in pawns:
            file = chess.square_file(sq)
            # doublés : autre pion sur la même colonne
            if len([p for p in pawns if chess.square_file(p) == file]) > 1:
                score -= 10 if color == chess.WHITE else -10
            # isolés ou passés peuvent être ajoutés plus tard
    return score

def mobility(board: chess.Board) -> int:
    """Nombre de coups légaux"""
    score = len(list(board.legal_moves))
    return score if board.turn == chess.WHITE else -score

def bishop_pair(board: chess.Board) -> int:
    """Bonus si paire de fous"""
    score = 0
    for color in [chess.WHITE, chess.BLACK]:
        bishops = board.pieces(chess.BISHOP, color)
        if len(bishops) >= 2:
            score += 50 if color == chess.WHITE else -50
    return score

def center_control(board: chess.Board) -> int:
    """Contrôle des 4 cases centrales"""
    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    score = 0
    for sq in center_squares:
        piece = board.piece_at(sq)
        if piece:
            score += 5 if piece.color == chess.WHITE else -5
    return score
