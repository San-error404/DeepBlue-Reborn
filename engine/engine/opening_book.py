import random
import chess

# Livre d’ouverture pondéré basé sur les vraies parties de Deep Blue 1997

OPENING_BOOK = {
    # Deep Blue jouait presque toujours 1.e4
    "": [
        ("e2e4", 0.95),
        ("d2d4", 0.05),  # au cas où on veut varier légèrement
    ],

    # Après 1.e4, si l’adversaire joue c6 (Caro-Kann)
    "e2e4 c7c6": [
        ("d2d4", 0.80),
        ("b1c3", 0.20),
    ],

    # Variante Advance
    "e2e4 c7c6 d2d4 d7d5": [
        ("e4e5", 0.90),
        ("b1c3", 0.10),
    ],

    # Anti-Caro-Kann agressif de la partie 6
    "e2e4 c7c6 d2d4 d7d5 b1c3 d5e4 g1e4 c8f5 e4g3 f5g6": [
        ("h2h4", 0.70),
        ("g1h3", 0.30),
    ],

    # Répertoire standard si l’adversaire joue 1…e5
    "e2e4 e7e5": [
        ("g1f3", 0.70),
        ("f1c4", 0.30),
    ],

    # Répertoire Najdorf (quand Deep Blue avait les Noirs dans la partie 1)
    "e2e4 c7c5": [
        ("g1f3", 1.0)
    ],

    "e2e4 c7c5 g1f3 d7d6": [
        ("d2d4", 1.0)
    ],
}

def book_move(board: chess.Board):
    """Renvoie un coup du livre si disponible (pondéré), sinon None."""
    moves_san = []

    # reconstruit l'historique des coups sous forme "e2e4 e7e5 g1f3" etc.
    temp_board = chess.Board()
    for move in board.move_stack:
        moves_san.append(temp_board.san(move))
        temp_board.push(move)

    # mais pour le livre, on utilise les coups UCI concaténés :
    key = " ".join(m.uci() for m in board.move_stack)

    if key not in OPENING_BOOK:
        return None

    choices = OPENING_BOOK[key]

    # Tirage pondéré
    moves = [c[0] for c in choices]
    weights = [c[1] for c in choices]

    move_uci = random.choices(moves, weights)[0]
    return chess.Move.from_uci(move_uci)
