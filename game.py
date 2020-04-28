import constants
from cards import Cards


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
        # This class will maintain all of the cards
        cards_handler = Cards()
        print(cards_handler)
        pass

    def run(self):
        """Main control loop for game play."""
