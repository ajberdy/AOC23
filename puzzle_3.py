import itertools
import re
from collections import defaultdict
from collections.abc import Generator
from functools import reduce

from solver import Solver


class Puzzle3Solver(Solver):
    def __init__(self, part: int = 1):
        super().__init__(3, part)
        self.schematic = self.get_input()
        self.gears = defaultdict(lambda: [])

    def process_input(self, content: str):
        return content.splitlines()

    def iter_schematic(self) -> Generator[bool, int]:
        for i, row in enumerate(self.schematic):
            for number in re.finditer(r"\d+", row):
                squares_to_check = list(filter(
                    lambda ix: 0 <= ix[0] < len(row) and 0 <= ix[1] < len(self.schematic),
                    itertools.product(
                        range(i - 1, i + 2),
                        range(number.span()[0] - 1, number.span()[1] + 1)
                    ),
                ))
                part = re.search(
                    r"[^\d\.]",
                    "".join(self.schematic[x][y] for x, y in squares_to_check),
                )
                if part and part.group() == "*":
                    gear_loc = squares_to_check[part.span()[0]]
                    self.gears[gear_loc].append(int(number.group()))
                yield part, int(number.group())

    def solve(self):
        sum_part_numbers = sum(
            number
            for is_part, number in self.iter_schematic()
            if is_part
        )
        if self.puzzle_part == 1:
            return sum_part_numbers
        return sum(
            reduce(int.__mul__, numbers)
            for numbers in self.gears.values()
            if len(numbers) == 2
        )
