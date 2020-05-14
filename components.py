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

    """Class to represent a card

    Attributes:
        name (str): The name of the card
        top (int): The value of the top rank
        left (int): The value of the left rank
        right (int): The value of the right rank
        bottom (int): The value of the bottom rank
        element (Element): The element of the card

    Methods:
        get_rank: Returns card rank by direction, with option for string rank
    """

    def __init__(self, name, top, left, right, bottom, element=Element.NONE):
        self._name = name
        self._ranks = {
            Direction.TOP: top,
            Direction.BOTTOM: bottom,
            Direction.LEFT: left,
            Direction.RIGHT: right
        }
        self._element = element

    def __str__(self):
        full_width = str(constants.MAXIMUM_CHARACTERS_IN_CARD_NAME)
        half_width = str(round(constants.MAXIMUM_CHARACTERS_IN_CARD_NAME / 2))

        string_element = 'N/A'
        if self._element != Element.NONE:
            string_element = str(self._element)

        format_string = '{:^' + full_width + 's}\n' \
                        '{:^' + half_width + 's}{:^' + half_width + 's}\n' \
                        '{:^' + half_width + 's}{:^' + half_width + 's}\n' \
                        '{:^' + half_width + 's}{:^' + half_width + 's}\n'
        return format_string.format(self.name,
                                    Card.get_string_rank(self._ranks[Direction.TOP]), 'Element',
                                    Card.get_string_rank(self._ranks[Direction.LEFT]) + ' ' +
                                    Card.get_string_rank(self._ranks[Direction.RIGHT]),
                                    string_element, Card.get_string_rank(self._ranks[Direction.BOTTOM]),
                                    str(self._element))

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

    def get_rank(self, direction, as_string=False):
        if direction in Direction:
            if as_string:
                return Card.get_string_rank(self._ranks[direction])
            return self._ranks[direction]
        return -1

    @property
    def name(self):
        return self._name

    @property
    def element(self):
        return self._element
