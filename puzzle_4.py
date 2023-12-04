import re

from solver import Solver


class Puzzle4Solver(Solver):
    def __init__(self, part: int = 1):
        super().__init__(4, part)
        self.winning, self.mine = self.get_input()

    def process_input(self, content: str):
        lines = content.splitlines()
        card_numbers, winning, mine = zip(*[
            re.search(r"Card +(\d+): ([\d ]+) \| ([\d ]+)", line).groups() for line in lines
        ])
        return [
            [
                {int(number) for number in number_string.split()}
                for number_string in numbers_list
            ] for numbers_list in (winning, mine)
        ]

    @staticmethod
    def compute_points(winning: set[int], mine: set[int]) -> int:
        return 2 ** (len(intersection) - 1) if (intersection := winning & mine) else 0

    def solve(self):
        if self.puzzle_part == 1:
            return sum(
                self.compute_points(winning, mine)
                for winning, mine
                in zip(self.winning, self.mine)
            )
        num_scratchcards = {i: 1 for i, _ in enumerate(self.mine)}
        for i, (winning, mine) in enumerate(zip(self.winning, self.mine)):
            for j, _ in enumerate(winning & mine, start=1):
                num_scratchcards[i + j] += num_scratchcards[i]
        return sum(num_scratchcards.values())
