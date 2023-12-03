import enum
import re
from functools import reduce, cache

from solver import Solver


class CubeColor(str, enum.Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Game:
    def __init__(self, number: int, turns: dict[CubeColor: int]):
        self.number = number
        self.turns = turns

    def __str__(self):
        return f"Game {self.number}: {self.turns}"

    def __repr__(self):
        return str(self)

    @classmethod
    def from_str(cls, game_str: str):
        label, _, play = game_str.partition(": ")
        number = int(re.search(r"\d+", label).group())
        turn_strs = play.split(";")

        def turn_from_str(turn: str) -> dict[CubeColor, int]:
            observations = turn.split(", ")
            turn = {}
            for observation in observations:
                count, color = observation.split()
                turn[color] = int(count)
            return turn

        turns = [
            turn_from_str(turn)
            for turn
            in turn_strs
        ]
        return cls(number, turns)

    @cache
    def min_cubes(self) -> dict[str, int]:
        def pick_maxes(turn_1, turn_2) -> dict[str, int]:
            return {
                color: max(
                    turn_1.get(color, 0),
                    turn_2.get(color, 0),
                )
                for color
                in CubeColor
            }
        return reduce(pick_maxes, self.turns)

    def is_possible(self, total_cubes: dict[str, int]) -> bool:
        return all(
            self.min_cubes()[color] <= total_cubes[color] for color in CubeColor
        )


class Puzzle2Solver(Solver):
    def __init__(self, part: int = 1):
        super().__init__(2, part)
        self.total_cubes = {
            CubeColor.RED: 12,
            CubeColor.GREEN: 13,
            CubeColor.BLUE: 14,
        }

    def process_input(self, content: str):
        lines = content.splitlines()
        return [
            Game.from_str(game_str)
            for game_str in
            lines
        ]

    def solve(self):
        games = self.get_input()
        if self.puzzle_part == 1:
            return sum(
                game.number
                for game in games
                if game.is_possible(self.total_cubes)
            )
        else:
            return sum(
                reduce(int.__mul__, game.min_cubes().values())
                for game in games
            )
