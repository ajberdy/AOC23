from collections import Counter
from enum import Enum

from solver import Solver


class HandTypes(int, Enum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    PAIR = 1
    HIGH_CARD = 0


class Card:

    def __init__(self, value: str, uses_jokers: bool = False):
        self.order = (
            "J23456789TQKA"
            if uses_jokers
            else "23456789TJQKA"
        )
        self.value = value

    def __lt__(self, other):
        return self.order.find(self.value) < self.order.find(other.value)

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(self.value)


class Hand:

    def __init__(self, cards: str, uses_jokers: bool = False):
        self.uses_jokers = uses_jokers
        self.cards = tuple(Card(card, uses_jokers=uses_jokers) for card in cards)
        self.card_counter = Counter(self.cards)

    def __str__(self):
        return "".join(str(card) for card in self.cards)

    def __repr__(self):
        return f'Hand("{str(self)}")'

    def groups(self):
        """Yield groups by strength"""
        cards_and_counts = [(count, card) for card, count in self.card_counter.items()]
        for count, card in sorted(cards_and_counts, reverse=True):
            yield count, card

    def categorization(self):
        """Get hand name"""
        joker_bonus = 0

        if self.uses_jokers:
            joker_bonus = self.card_counter.get("J", 0)

            if joker_bonus == 5:
                return HandTypes.FIVE_OF_A_KIND

        groups = self.groups()
        first_count, first_card = next(groups)
        if first_card == "J":
            first_count, first_card = next(groups)

        first_count += joker_bonus

        if first_count == 5:
            return HandTypes.FIVE_OF_A_KIND
        elif first_count == 4:
            return HandTypes.FOUR_OF_A_KIND

        second_count, second_card = next(groups)
        if second_card == "J":
            second_count, second_card = next(groups)

        if first_count == 3:
            if second_count == 2:
                return HandTypes.FULL_HOUSE
            else:
                return HandTypes.THREE_OF_A_KIND
        elif first_count == 2:
            if second_count == 2:
                return HandTypes.TWO_PAIR
            else:
                return HandTypes.PAIR
        else:
            return HandTypes.HIGH_CARD

    def __lt__(self, other):
        self_categorization = self.categorization()
        other_categorization = other.categorization()

        if self_categorization == other_categorization:
            return self.cards < other.cards
        return self_categorization < other_categorization


class Puzzle7Solver(Solver):
    def __init__(self, part: int = 1):
        super().__init__(7, part)
        self.hands = self.get_input()

    def process_input(self, content: str):
        return {
            Hand(hand, uses_jokers=(self.puzzle_part == 2)): int(bid)
            for hand, bid in [
                line.split() for line in content.splitlines()
            ]
        }

    def solve(self):
        return sum(
            i * bid
            for i, (hand, bid)
            in enumerate(sorted(self.hands.items()), start=1)
        )
