from .uci import UCI

class Engine:
    """
    Main class connecting UCI protocol to the search engine.
    """

    def __init__(self):
        self.uci = UCI()

    def loop(self):
        """
        Main loop for UCI communication.
        """
        while True:
            try:
                command = input()
            except EOFError:
                break

            if command == "quit":
                break

            self.uci.parse(command)
