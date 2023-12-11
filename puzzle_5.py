import re
from functools import reduce

from solver import Solver


class Transform:

    def __init__(self, dest_start: int, source_start: int, range_len: int):
        self.source_range = range(source_start, source_start + range_len)
        self.offset = dest_start - source_start

    def __str__(self):
        return f"[{self.source_range.start}, {self.source_range.stop}){self.offset:+}"

    def __call__(self, source_num: int | range):
        if isinstance(source_num, range):
            # -1 + 1 to ensure that the end gets transformed if it == transform range end
            return range(self(source_num.start), self(source_num.stop - 1) + 1)
        return source_num + (
            self.offset
            if source_num in self.source_range
            else 0
        )


class Puzzle5Solver(Solver):
    def __init__(self, part: int = 1):
        super().__init__(5, part)
        self.seeds, self.maps = self.get_input()

    def process_seeds(self, seed_str):
        if self.puzzle_part == 1:
            return [
                range(int(start), int(start) + 1)
                for start in re.findall(r"\d+", seed_str)
            ]
        else:
            return [
                range(int(start), int(start) + int(range_len))
                for start, range_len in re.findall(r"(\d+) (\d+)", seed_str)
            ]

    @staticmethod
    def process_maps(maps_str):
        return [
            sorted(
                [Transform(*row) for row in transformation],
                key=lambda t: t.source_range.start,
            )
            for transformation in [
                [
                    [int(x) for x in row.split()]
                    for row in mapping.splitlines()
                ] for mapping in re.findall(r"map:\n([\d \n]+)\n\n", maps_str)
            ]
        ]

    def process_input(self, content: str):
        seed_str, _, maps_str = content.partition("\n\n")
        seeds = self.process_seeds(seed_str)
        maps = self.process_maps(maps_str)
        return seeds, maps

    @staticmethod
    def update(seeds: list[range], transforms: list[Transform]):
        # transforms are sorted
        new_seeds = []
        while seeds:
            seed = seeds.pop(0)
            new_seed_start = seed.start
            for transform in transforms:
                if new_seed_start in transform.source_range:
                    # create new range for overlap of seed range and transform range
                    if seed.stop in transform.source_range:
                        new_seed_end = seed.stop
                    else:
                        new_seed_end = transform.source_range.stop
                        # capture remaining seed range to be handled by other transforms
                        if remaining_seed := range(transform.source_range.stop, seed.stop):
                            seeds.insert(0, remaining_seed)
                    new_seeds.append(transform(range(new_seed_start, new_seed_end)))
                    break
            else:
                # gets mapped as is
                new_seeds.append(seed)
        return new_seeds

    def solve(self):
        return min(
            loc_range.start for loc_range in reduce(
                self.update,
                self.maps,
                self.seeds,
            )
        )
