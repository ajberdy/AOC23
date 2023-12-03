import abc


class Solver:

    def __init__(self, puzzle_number: int, puzzle_part: int):
        self.puzzle_number = puzzle_number
        self.puzzle_part = puzzle_part

    @property
    def puzzle_str(self):
        return f"puzzle_{self.puzzle_number}"

    def get_input(self):
        with open(f"puzzle_inputs/{self.puzzle_str}.txt") as f:
            content = f.read()
            return self.process_input(content)

    def process_input(self, content: str):
        return content

    @abc.abstractmethod
    def solve(self):
        """Solution to the puzzle."""
