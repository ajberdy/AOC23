import importlib

from solver import Solver


def get_solver(problem_number: int, part: int = 1) -> Solver:
    module_name = f"puzzle_{problem_number}"
    solver_name = f"Puzzle{problem_number}Solver"
    return getattr(importlib.import_module(module_name), solver_name)(part)


def run_solution(problem_number: int, part: int = 1):
    return get_solver(problem_number, part).solve()


if __name__ == '__main__':
    problem = (9, 2)
    answer = run_solution(*problem)
    print(f"Solution to Problem {problem[0]}.{problem[1]}: {answer}")
