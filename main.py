import sys
import chess
from engine.search import Search
from engine.opening_book import book_move

board = chess.Board()
search = Search()

def uci_loop():
    print("id name DeepBlueClone")
    print("id author Toi")
    print("uciok")

    while True:
        line = sys.stdin.readline().strip()

        if line == "isready":
            print("readyok")

        elif line.startswith("ucinewgame"):
            board.reset()

        elif line.startswith("position"):
            parts = line.split(" ", 2)
            if "startpos" in parts[1]:
                board.reset()
                if len(parts) > 2 and parts[2].startswith("moves"):
                    moves = parts[2][6:].split()
                    for move in moves:
                        board.push_uci(move)
            elif "fen" in parts[1]:
                # position fen <fen string> moves ...
                fen_and_moves = parts[2].split("moves")
                board.set_fen(fen_and_moves[0].strip())
                if len(fen_and_moves) > 1:
                    moves = fen_and_moves[1].split()
                    for move in moves:
                        board.push_uci(move)

        elif line.startswith("go"):
            # 1) Tenter le livre d’ouverture
            bm = book_move(board)
            if bm is not None:
                print(f"bestmove {bm.uci()}")
                continue

            # 2) Sinon lancer ton moteur
            best = search.search(board, depth=4)
            print(f"bestmove {best.uci()}")

        elif line == "quit":
            break


if __name__ == "__main__":
    uci_loop()
