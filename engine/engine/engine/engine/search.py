import chess
from .evaluation import evaluate
from .transposition_table import TT

class Search:

    def __init__(self):
        self.tt = TT()

    def search(self, board, depth):
        best_score = -999999
        best_move = None

        for move in board.legal_moves:
            board.push(move)
            score = -self.negamax(board, depth - 1, -1000000, 1000000)
            board.pop()

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def negamax(self, board, depth, alpha, beta):
        key = board.transposition_key()

        tt_value = self.tt.lookup(key, depth, alpha, beta)
        if tt_value is not None:
            return tt_value

        if depth == 0:
            return self.quiescence(board, alpha, beta)

        if board.is_game_over():
            return evaluate(board)

        best = -1_000_000

        for move in board.legal_moves:
            board.push(move)
            score = -self.negamax(board, depth - 1, -beta, -alpha)
            board.pop()

            if score > best:
                best = score

            if best > alpha:
                alpha = best

            if alpha >= beta:
                break

        self.tt.store(key, depth, best)

        return best

    def quiescence(self, board, alpha, beta):
        stand_pat = evaluate(board)

        if stand_pat >= beta:
            return beta

        if alpha < stand_pat:
            alpha = stand_pat

        for move in board.legal_moves:
            if board.is_capture(move):
                board.push(move)
                score = -self.quiescence(board, -beta, -alpha)
                board.pop()

                if score >= beta:
                    return beta

                if score > alpha:
                    alpha = score

        return alpha
