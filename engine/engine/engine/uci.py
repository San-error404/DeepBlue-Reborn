import chess
from .search import Search

class UCI:
    """
    Minimal UCI protocol implementation.
    """

    def __init__(self):
        self.board = chess.Board()
        self.search = Search()

    def parse(self, line: str):
        if line == "uci":
            print("id name DeepBlueReborn")
            print("id author You")
            print("uciok")

        elif line == "isready":
            print("readyok")

        elif line.startswith("position"):
            self.handle_position(line)

        elif line.startswith("go"):
            self.handle_go(line)

    def handle_position(self, line):
        parts = line.split()

        if parts[1] == "startpos":
            self.board = chess.Board()
            move_index = 2

        elif parts[1] == "fen":
            fen = " ".join(parts[2:8])
            self.board = chess.Board(fen)
            move_index = 8

        if len(parts) > move_index and parts[move_index] == "moves":
            for mv in parts[move_index+1:]:
                self.board.push_uci(mv)

    def handle_go(self, line):
        depth = 3
        parts = line.split()

        if "depth" in parts:
            depth = int(parts[parts.index("depth") + 1])

        best_move = self.search.search(self.board, depth)

        if best_move:
            print("bestmove", best_move.uci())
        else:
            print("bestmove 0000")
