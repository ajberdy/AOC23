import itertools

from solver import Solver


class Puzzle11Solver(Solver):
    def __init__(self, part: int = 1):
        super().__init__(11, part)
        self.map = self.get_input()
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.galaxy_coordinates = self.get_galaxy_coordinates()
        self.empty_rows, self.empty_columns = self.find_empty_row_and_columns()

    def process_input(self, content: str):
        return content.splitlines()

    def find_empty_row_and_columns(self):
        empty_row_indices = [
            i
            for i, row in enumerate(self.map)
            if "#" not in row
        ]
        empty_column_indices = [
            i
            for i in range(self.width)
            if all(row[i] == "." for row in self.map)
        ]
        return empty_row_indices, empty_column_indices

    def get_galaxy_coordinates(self):
        return [
            (r, c)
            for r, c in itertools.product(range(self.height), range(self.width))
            if self.map[r][c] == "#"
        ]

    def get_distance(self, galaxy_1, galaxy_2):
        (r1, c1), (r2, c2) = galaxy_1, galaxy_2
        expansion_factor = (
            2 if self.puzzle_part == 1 else 1_000_000
        )
        vertical_distance = abs(r2 - r1) + sum(
            expansion_factor - 1 for empty_row in self.empty_rows if min(r1, r2) < empty_row < max(r1, r2)
        )
        horizontal_distance = abs(c2 - c1) + sum(
            expansion_factor - 1 for empty_column in self.empty_columns if min(c1, c2) < empty_column < max(c1, c2)
        )
        return vertical_distance + horizontal_distance

    def solve(self):
        total = 0
        for i, galaxy_1 in enumerate(self.galaxy_coordinates):
            for j, galaxy_2 in enumerate(self.galaxy_coordinates[:i]):
                total += self.get_distance(galaxy_1, galaxy_2)
        return total
