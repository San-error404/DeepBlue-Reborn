import chess
from .evaluation import evaluate
from .transposition_table import TT
from .move_ordering import order_moves, PIECE_VALUES

class Search:
    def __init__(self):
        self.tt = TT()
        self.killer_moves = {}  # clé = profondeur, valeur = move

    def search(self, board: chess.Board, depth: int):
        """
        Renvoie le meilleur coup pour la position donnée et la profondeur.
        """
        best_score = -999999
        best_move = None

        moves = order_moves(board, list(board.legal_moves))
        for move in moves:
            board.push(move)
            score = -self.negamax(board, depth - 1, -1000000, 1000000)
            board.pop()

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def negamax(self, board: chess.Board, depth: int, alpha: int, beta: int):
        """
        Negamax avec alpha-beta et table de transpositions
        """
        if board.is_game_over():
            return self.game_over_score(board)

        key = board.transposition_key()
        tt_entry = self.tt.lookup(key, depth, alpha, beta)
        if tt_entry is not None:
            return tt_entry

        # Extension tactique simple : si roi en échec, augmente la profondeur
        extend = 1 if board.is_check() else 0

        if depth == 0:
            return self.quiescence(board, alpha, beta)

        best = -1000000
        moves = order_moves(board, list(board.legal_moves))
        for move in moves:
            board.push(move)
            score = -self.negamax(board, depth - 1 + extend, -beta, -alpha)
            board.pop()

            if score > best:
                best = score
                # Killer move : si coup coupe l’alpha-beta, on le note
                if best >= beta:
                    self.killer_moves[depth] = move

            if best > alpha:
                alpha = best
            if alpha >= beta:
                break

        # Stockage dans la table de transposition avec flag
        self.tt.store(key, depth, best, alpha, beta)

        return best

    def quiescence(self, board: chess.Board, alpha: int, beta: int):
        """
        Recherche quiescence : seulement captures et promotions
        """
        stand_pat = evaluate(board)

        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        moves = [m for m in board.legal_moves if board.is_capture(m) or board.piece_at(m.from_square).piece_type == chess.PAWN]
        moves = order_moves(board, moves)

        for move in moves:
            board.push(move)
            score = -self.quiescence(board, -beta, -alpha)
            board.pop()

            if score >= beta:
                return beta
            if score > alpha:
                alpha = score

        return alpha

    def game_over_score(self, board: chess.Board):
        """
        Retourne un score extrême selon le résultat de la partie
        """
        if board.is_checkmate():
            return -999999 if board.turn else 999999
        return 0
