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


class Card:

    def __init__(self, name, top, left, right, bottom, element=Element.NONE):
        self.name = name
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom
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
                                    self.get_string_rank(self.top), 'Element',
                                    self.get_string_rank(self.left) + ' ' + self.get_string_rank(self.right),
                                    string_element, self.get_string_rank(self.bottom), self.element.character_representation())

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

    def get_top(self):
        return self.top

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_bottom(self):
        return self.bottom

    def get_element(self):
        return self.element
