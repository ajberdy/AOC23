import re
from enum import Enum
from functools import reduce
from itertools import cycle

from solver import Solver


class Direction(int, Enum):
    LEFT = 0
    RIGHT = 1


class Puzzle8Solver(Solver):
    def __init__(self, part: int = 1):
        super().__init__(8, part)
        self.directions, self.map = self.get_input()

    def process_input(self, content: str):
        direction_line, _, map_lines = content.partition("\n\n")
        direction_map = {"L": Direction.LEFT, "R": Direction.RIGHT}
        directions = [direction_map[direction] for direction in direction_line]
        node_map = {
            root: (lhs, rhs)
            for root, lhs, rhs
            in re.findall(r"(.+) = \((.+), (.+)\)", map_lines)
        }
        return directions, node_map

    def get_zees(self):
        nodes = [node for node in self.map if node.endswith("A")]
        zees = [[] for _ in nodes]

        steps = 0

        for direction in cycle(self.directions):
            for i, node in enumerate(nodes):
                if node.endswith("Z"):
                    if len(zees[i]) < 2:
                        zees[i].append(steps)

            nodes = [self.map[node][direction] for node in nodes]
            steps += 1

            if all([len(z) == 2 for z in zees]):
                return zees

    @staticmethod
    def iter_zees(first_z, second_z):
        i = 0
        while True:
            yield first_z + (second_z - first_z) * i
            i += 1

    @staticmethod
    def is_z(first_z, second_z, i):
        return not (i - first_z) % (second_z - first_z)

    def combine_zees(self, first_set, second_set):
        zees = []
        for i in self.iter_zees(*first_set):
            if self.is_z(*second_set, i):
                zees.append(i)
            if len(zees) == 2:
                return zees

    def solve(self):
        if self.puzzle_part == 1:
            node = "AAA"
            end_node = "ZZZ"

            steps = 0

            for direction in cycle(self.directions):
                if node == end_node:
                    return steps

                node = self.map[node][direction]
                steps += 1
        else:
            zees = self.get_zees()
            return reduce(
                self.combine_zees,
                zees,
            )[0]

