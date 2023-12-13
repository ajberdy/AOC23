import numpy as np

from solver import Solver


class Sequence:

    def __init__(self, values):
        self.values = np.array([int(x) for x in values], dtype=int)

    def __repr__(self):
        return f"Sequence([{', '.join(str(x) for x in self.values)}])"

    def get_dx(self) -> "Sequence":
        return Sequence(self.values[1:] - self.values[:-1])

    def apply_dx(self) -> int:
        return self.values[-1] + self.get_dx().get_next()

    def get_next(self) -> int:
        if not any(self.values):
            return 0
        return self.apply_dx()

    def apply_dx_backwards(self) -> int:
        return self.values[0] - self.get_dx().get_previous()

    def get_previous(self) -> int:
        if not any(self.values):
            return 0
        return self.apply_dx_backwards()


class Puzzle9Solver(Solver):
    def __init__(self, part: int = 1):
        super().__init__(9, part)
        self.sequences = self.get_input()

    def process_input(self, content: str):
        return [Sequence(line.split()) for line in content.splitlines()]

    def solve(self):
        if self.puzzle_part == 1:
            return sum(seq.get_next() for seq in self.sequences)
        else:
            return sum(seq.get_previous() for seq in self.sequences)
