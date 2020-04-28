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


class Card:

    def __init__(self, name, top, left, right, bottom, element=Element.NONE):
        self.name = name
        self.top = top
        self.left = left
        self.right = right
        self.bottom = bottom
        self.element = element

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if other is None:
            return False
        if other.name == self.name:
            return True
        return False

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


class AgentState:

    def __init__(self):
        self.cards_in_hand = []
        self.is_turn = False
        pass


class GameStateData:

    def __init__(self):
        # Init game state
        pass


class Grid:

    def __init__(self):

        # TODO store elsewhere?
        self.WIDTH = constants.GAME_GRID_WIDTH
        self.HEIGHT = constants.GAME_GRID_HEIGHT

        pass


class Game:

    def __init__(self):
        pass

    def run(self):
        """Main control loop for game play."""
