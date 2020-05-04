from enum import Enum, auto
import constants


class Element(Enum):
    NONE = auto()
    FIRE = auto()
    EARTH = auto()
    ICE = auto()
    THUNDER = auto()
    HOLY = auto()
    POISON = auto()
    WIND = auto()
    WATER = auto()

    def __str__(self):
        return self.name.capitalize()


class Direction(Enum):
    TOP = 'top'
    BOTTOM = 'bottom'
    LEFT = 'left'
    RIGHT = 'right'

    def get_opposite(self):
        if self is self.TOP:
            return Direction.BOTTOM
        if self is self.BOTTOM:
            return Direction.TOP
        if self is self.RIGHT:
            return Direction.LEFT
        if self is self.LEFT:
            return Direction.RIGHT
        return None


class Card:

    def __init__(self, name, top, left, right, bottom, element=Element.NONE):
        self.name = name
        self.ranks = {
            Direction.TOP: top,
            Direction.BOTTOM: bottom,
            Direction.LEFT: left,
            Direction.RIGHT: right
        }
        self.element = element

    def __str__(self):
        full_width = str(constants.MAXIMUM_CHARACTERS_IN_CARD_NAME)
        half_width = str(round(constants.MAXIMUM_CHARACTERS_IN_CARD_NAME / 2))

        string_element = 'N/A'
        if self.element != Element.NONE:
            string_element = str(self.element)

        format_string = '{:^' + full_width + 's}\n' \
                        '{:^' + half_width + 's}{:^' + half_width + 's}\n' \
                        '{:^' + half_width + 's}{:^' + half_width + 's}\n' \
                        '{:^' + half_width + 's}{:^' + half_width + 's}\n'
        return format_string.format(self.name,
                                    self.get_string_rank(self.ranks[Direction.TOP]), 'Element',
                                    self.get_string_rank(self.ranks[Direction.LEFT]) + ' ' +
                                    self.get_string_rank(self.ranks[Direction.RIGHT]),
                                    string_element, self.get_string_rank(self.ranks[Direction.BOTTOM]),
                                    str(self.element))

    def __eq__(self, other):
        if other is None:
            return False
        if other.name == self.name:
            return True
        return False

    @staticmethod
    def get_string_rank(int_rank):
        if int_rank in range(1, 10):
            return str(int_rank)
        # Rank is 10
        return 'A'

    def get_name(self):
        return self.name

    def get_rank(self, direction, as_string=False):
        if direction in Direction:
            if as_string:
                return self.get_string_rank(self.ranks[direction])
            return self.ranks[direction]
        return -1

    def get_element(self):
        return self.element
