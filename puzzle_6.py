import math
import re
from functools import reduce

from solver import Solver


class Race:

    def __init__(self, time: int, record: int):
        self.time = time
        self.record = record

    def __str__(self):
        return f"Race({self.record}mm in {self.time}ms)"

    def __repr__(self):
        return f"Race({self.time}, {self.record})"


class Puzzle6Solver(Solver):
    def __init__(self, part: int = 1):
        super().__init__(6, part)
        self.races = self.get_input()

    def process_input(self, content: str):
        if self.puzzle_part == 1:
            times, distances = (
                list(map(int, re.findall(r"\d+", line)))
                for line in content.splitlines()
            )
            return [Race(time, distance) for time, distance in zip(times, distances)]
        elif self.puzzle_part == 2:
            time, distance = (
                int(''.join(re.findall(r"\d+", line)))
                for line in content.splitlines()
            )
            return [Race(time, distance)]

    @staticmethod
    def solve_range(total_time, record):
        # time_held ** 2 - total_time * time_held + record
        a, b, c = 1, -total_time, record

        soln_0 = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        soln_1 = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)

        lower_bound = int(soln_0 + 1)
        upper_bound = math.ceil(soln_1)
        return range(lower_bound, upper_bound)

    def solve(self):
        return reduce(
            int.__mul__,
            (
                len(self.solve_range(race.time, race.record))
                for race in self.races
            ),
        )
