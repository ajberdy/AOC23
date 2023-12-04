import abc
from aocd import get_data


class Solver:

    def __init__(self, puzzle_number: int, puzzle_part: int):
        self.puzzle_number = puzzle_number
        self.puzzle_part = puzzle_part

    @property
    def puzzle_str(self):
        return f"puzzle_{self.puzzle_number}"

    def get_input(self):
        content = get_data(year=2023, day=self.puzzle_number)
        return self.process_input(content)

    def process_input(self, content: str):
        return content

    @abc.abstractmethod
    def solve(self):
        """Solution to the puzzle."""
