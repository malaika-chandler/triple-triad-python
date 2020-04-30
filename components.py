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

    def character_representation(self):
        if self == Element.NONE:
            return ''
        elif self == Element.FIRE:
            return '🔥'
        elif self == Element.EARTH:
            return '🌏'
        elif self == Element.ICE:
            return '❄️'
        elif self == Element.THUNDER:
            return '⚡️'
        elif self == Element.HOLY:
            return '✨'
        elif self == Element.POISON:
            return '☠'
        elif self == Element.WIND:
            return '🌪'
        elif self == Element.WATER:
            return '💧'
        else:
            return ''


class Direction(Enum):
    TOP = 'top'
    BOTTOM = 'bottom'
    LEFT = 'left'
    RIGHT = 'right'

    OPPOSITE = {
        TOP: BOTTOM,
        BOTTOM: TOP,
        RIGHT: LEFT,
        LEFT: RIGHT
    }

    def get_opposite(self):
        if self.TOP:
            return Direction.BOTTOM
        if self.BOTTOM:
            return Direction.TOP
        if self.RIGHT:
            return Direction.LEFT
        if self.LEFT:
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
                                    self.element.character_representation())

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

    def get_rank(self, direction):
        if direction in Direction:
            return self.ranks[direction]
        return -1

    def get_element(self):
        return self.element
