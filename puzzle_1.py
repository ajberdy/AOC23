import re

from solver import Solver


class Puzzle1Solver(Solver):
    def __init__(self, part: int = 1):
        super().__init__(1, part)

    def process_input(self, content: str):
        return content.splitlines()

    @staticmethod
    def name_to_digit(digit_name: str) -> str:
        return {
            # "zero": "0",
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9",
        }.get(digit_name, digit_name)

    def get_digits(self, string: str) -> tuple[str, ...]:
        pattern = (
            re.compile(r"\d")
            if self.puzzle_part == 1
            else re.compile(
                r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))"
            )
        )
        found_digits = re.findall(pattern, string)
        return tuple(
            self.name_to_digit(digit)
            for digit in
            (found_digits[0], found_digits[-1])
        )

    @staticmethod
    def combine_digits(digits: tuple[str, ...]) -> int:
        return int(''.join(digits))

    def solve(self):
        stuff = self.get_input()
        digits = [self.get_digits(line) for line in stuff]
        ints = [self.combine_digits(digit_pair) for digit_pair in digits]
        return sum(ints)
