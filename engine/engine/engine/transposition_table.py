class TT:
    def __init__(self):
        self.table = {}

    def store(self, key, depth, value):
        self.table[key] = (depth, value)

    def lookup(self, key, depth, alpha, beta):
        if key not in self.table:
            return None

        stored_depth, stored_value = self.table[key]

        if stored_depth >= depth:
            return stored_value

        return None
