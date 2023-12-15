import itertools
from enum import Enum

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation
from matplotlib.animation import FuncAnimation

from solver import Solver


Coordinate = tuple[int | float, int | float]


class Direction(tuple, Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def __neg__(self):
        return tuple(-x for x in self)


class PipeShapes(str, Enum):
    VERTICAL = "|"
    HORIZONTAL = "-"
    F = "F"
    SEVEN = "7"
    L = "L"
    J = "J"
    NO_PIPE = "."


PIPE_SHAPE_MAP = {
    PipeShapes.VERTICAL: (Direction.UP, Direction.DOWN),
    PipeShapes.HORIZONTAL: (Direction.LEFT, Direction.RIGHT),
    PipeShapes.F: (Direction.DOWN, Direction.RIGHT),
    PipeShapes.SEVEN: (Direction.DOWN, Direction.LEFT),
    PipeShapes.L: (Direction.UP, Direction.RIGHT),
    PipeShapes.J: (Direction.UP, Direction.LEFT),
    PipeShapes.NO_PIPE: (),
}


class Puzzle10Solver(Solver):
    def __init__(self, part: int = 1):
        super().__init__(10, part)
        self.map = self.get_input()
        self.initial_position = self.get_initial_position()
        self.loop = self.solve_loop()
        self.height = len(self.map)
        self.width = len(self.map[0])

    def process_input(self, content: str):
        return content.splitlines()

    def get_initial_position(self):
        for r, line in enumerate(self.map):
            if (c := line.find("S")) >= 0:
                return r, c

    def in_bounds(self, r, c):
        return -0.5 <= r < self.height and -0.5 <= c < self.width

    def get_neighbors(self, position: Coordinate):
        r, c = position
        for rn, cn in [(r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)]:
            if self.in_bounds(rn, cn) and self.is_connected(position, (rn, cn)):
                yield rn, cn

    def get_first_move(self) -> Direction:
        r, c = self.initial_position
        # above
        if Direction.DOWN in PIPE_SHAPE_MAP[self.map[r - 1][c]]:
            return Direction.UP
        # right
        if Direction.LEFT in PIPE_SHAPE_MAP[self.map[r][c + 1]]:
            return Direction.RIGHT
        # below
        if Direction.UP in PIPE_SHAPE_MAP[self.map[r + 1][c]]:
            return Direction.DOWN
        # left
        if Direction.RIGHT in PIPE_SHAPE_MAP[self.map[r][c - 1]]:
            return Direction.LEFT

    def get_next_move(self, position: Coordinate, move: Direction) -> Direction:
        r, c = position
        moves = PIPE_SHAPE_MAP[self.map[r][c]]
        return moves[not moves.index(-move)]

    @staticmethod
    def get_next_position(position: Coordinate, move: Direction):
        return position[0] + move[0], position[1] + move[1]

    def solve_loop(self) -> dict[Coordinate, int]:
        position = self.initial_position
        move = self.get_first_move()
        steps = 0
        loop = {}

        while True:
            position = self.get_next_position(position, move)
            loop[position] = steps
            steps += 1
            if position == self.initial_position:
                return loop
            move = self.get_next_move(position, move)

    def is_connected(self, node: Coordinate, neighbor: Coordinate) -> bool:
        (r, c), (rn, cn) = node, neighbor

        rs = (
            [int((r + rn) // 2)] * 2
            if r != rn
            else [int(r - 0.5), int(r + 0.5)]
        )
        cs = (
            [int((c + cn) // 2)] * 2
            if c != cn
            else [int(c - 0.5), int(c + 0.5)]
        )

        loop_node_1, loop_node_2 = zip(rs, cs)
        blocked = (
                loop_node_1 in self.loop
                and loop_node_2 in self.loop
                and self.loop[loop_node_1] - self.loop[loop_node_2] in (-1, 1, -len(self.loop) + 1, len(self.loop) - 1)
        )
        return not blocked

    @staticmethod
    def draw_grid(grid_width, grid_height, highlighted_squares, highlighted_corners):
        fig, ax = plt.subplots()

        # Draw grid squares
        for r in range(grid_height):
            for c in range(grid_width):
                square = patches.Rectangle((c, grid_height - r - 1), 1, 1, edgecolor='gray', facecolor='none')
                ax.add_patch(square)

        # Highlight squares
        for sq in highlighted_squares:
            r, c = sq
            highlight = patches.Rectangle((c + .1, grid_height - r - 1 + .1), .8, .8, edgecolor='red', facecolor='red', lw=2)
            ax.add_patch(highlight)

        # Mark corners
        for corner in highlighted_corners:
            r, c = corner
            ax.plot(c + 0.5, grid_height - r - 1 + 0.5, 'bo', markersize=10)  # 'bo' is blue circle marker

        plt.xlim(0, grid_width)
        plt.ylim(0, grid_height)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    def solve(self):
        if self.puzzle_part == 1:
            return len(self.loop) // 2

        out_of_loop = set()
        fringe = [(-0.5, -0.5)]

        while fringe:
            node = fringe.pop(0)
            out_of_loop.add(node)

            for neighbor in self.get_neighbors(node):
                if neighbor not in out_of_loop and neighbor not in fringe:
                    fringe.append(neighbor)

        # self.draw_grid(self.width, self.height, self.loop, out_of_loop)

        in_loop = {
            (r, c)
            for r, c in itertools.product(range(self.height), range(self.width))
            if any(
                corner not in out_of_loop
                for corner in [
                    (r - 0.5, c - 0.5),
                    (r - 0.5, c + 0.5),
                    (r + 0.5, c - 0.5),
                    (r + 0.5, c + 0.5),
                ]
            ) and (r, c) not in self.loop
        }

        return len(in_loop)
