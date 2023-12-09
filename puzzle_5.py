import re
from functools import reduce

from solver import Solver


class Range:

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __bool__(self):
        return self.end > self.start

    def __add__(self, other):
        return Range(self.start + other, self.end + other)

    def __sub__(self, other):
        return self + (-other)

    def __repr__(self):
        return f"Range({self.start}, {self.end})"

    def __contains__(self, item):
        return self.start <= item < self.end


class Transform:

    def __init__(self, dest_start: int, source_start: int, range_len: int):
        self.dest_start = dest_start
        self.dest_end = dest_start + range_len
        self.dest_range = Range(self.dest_start, self.dest_end)
        self.source_start = source_start
        self.source_end = source_start + range_len
        self.source_range = Range(self.source_start, self.source_end)
        self.range_len = range_len
        self.offset = self.dest_start - self.source_start

    @classmethod
    def from_range_and_offset(cls, start, end, offset):
        return cls(start + offset, start, end - start)

    def __lt__(self, other):
        return self.source_start < other.source_start

    def __str__(self):
        return f"[{self.source_start}, {self.source_start + self.range_len}){self.offset:+}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __call__(self, source_num: int | Range):
        if isinstance(source_num, Range):
            # -1 + 1 to ensure that the end gets transformed if it == transform range end
            return Range(self(source_num.start), self(source_num.end - 1) + 1)
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
            return {int(seed) for seed in re.findall(r"\d+", seed_str)}
        else:
            return sorted(
                [
                    Range(int(start), int(start) + int(range_len))
                    for start, range_len in re.findall(r"(\d+) (\d+)", seed_str)
                ],
                key=lambda r: r.start,
            )

    def process_maps(self, maps_str):
        if self.puzzle_part == 2:
            maps = re.findall(r"map:\n([\d \n]+)\n\n", maps_str)
            return [
                sorted(
                    [Transform(*row) for row in transformation],
                    key=lambda t: t.source_start,
                )
                for transformation in [
                    [
                        [int(x) for x in row.split()]
                        for row in mapping.splitlines()
                    ] for mapping in maps
                ]
            ]

        def create_transform(mapping):
            def transform(from_num):
                for dest_range_start, source_range_start, range_len in (
                        (int(num) for num in line.split())
                        for line in mapping.split("\n")
                ):
                    if source_range_start <= from_num < source_range_start + range_len:
                        return from_num - source_range_start + dest_range_start
                return from_num

            return transform

        return [
            create_transform(mapping)
            for mapping in re.findall(r"map:\n([\d \n]+)\n\n", maps_str)
        ]

    def process_input(self, content: str):
        seed_str, _, maps_str = content.partition("\n\n")
        seeds = self.process_seeds(seed_str)
        maps = self.process_maps(maps_str)
        return seeds, maps

    def update(self, seeds: list[Range], transforms: list[Transform]):
        # seeds and transforms are both sorted
        new_seeds = []
        while seeds:
            seed = seeds.pop(0)
            new_seed_start = seed.start
            for transform in transforms:
                if new_seed_start in transform.source_range:
                    # create new range for overlap of seed range and transform range
                    if seed.end in transform.source_range:
                        new_seed_end = seed.end
                    else:
                        new_seed_end = transform.source_end
                        # capture remaining seed range to be handled by other transforms
                        if remaining_seed := Range(transform.source_end, seed.end):
                            seeds.insert(0, remaining_seed)
                    new_seeds.append(transform(Range(new_seed_start, new_seed_end)))
                    break
            else:
                # gets mapped as is
                new_seeds.append(seed)
        return new_seeds


    def solve(self):
        if self.puzzle_part == 1:
            return min(
                reduce(lambda acc, transform: transform(acc), self.maps, seed)
                for seed in self.seeds
            )
        else:
            return min(
                loc_range.start for loc_range in reduce(
                    self.update,
                    self.maps,
                    self.seeds
                )
            )
