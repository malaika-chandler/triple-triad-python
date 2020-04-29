import constants
from cards import Cards
from components import Direction
import random


class AgentState:

    def __init__(self):
        self.cards_in_hand = []
        self.is_turn = False
        pass


class GameState:

    def __init__(self):
        self.data = None

    def get_legal_actions(self):
        pass

    def get_score(self):
        return self.data.score


class GameStateData:

    def __init__(self):
        # Init game state
        pass


class GameBoardLocation:
    def __init__(self, coordinates):
        self.has_card = False
        self.placed_card = None
        self.has_element = False
        self.space_element = None
        self.grid_coordinates = (coordinates[0], coordinates[1])
        self.owner = None
        self.neighbors = self._calculate_neighbors(coordinates)

    def initialize(self):
        self.has_card = False
        self.placed_card = None
        self.has_element = False
        self.space_element = None
        self.owner = None

    def place_card(self, agent, card):
        self.has_card = True
        self.placed_card = card
        self.owner = agent

    def set_owner(self, agent):
        self.owner = agent

    def calculate_location_value(self, rank_direction):
        if self.has_card:
            if rank_direction in Direction:
                # TODO Pass data to rules method for specific calculating
                return self.placed_card.get_rank(rank_direction)
        return -1

    def get_coordinates(self):
        return self.grid_coordinates

    def _calculate_direction_of_neighbor(self, neighbor):
        if neighbor.get_coordinates in self.neighbors.values():
            direction = None
            # TODO There's got to be a better waaay
            for neighbor_direction, neighbor_coordinates in self.neighbors.values():
                if neighbor_coordinates == neighbor.get_coordinates:
                    direction = neighbor_direction
                    break
            return direction
        return None

    def __lt__(self, other):
        direction = self._calculate_direction_of_neighbor(other)
        opposite_direction = Direction.OPPOSITE(direction)
        return self.calculate_location_value(direction) < other.calculate_location_value(opposite_direction)

    def __le__(self, other):
        direction = self._calculate_direction_of_neighbor(other)
        opposite_direction = Direction.OPPOSITE(direction)
        return self.calculate_location_value(direction) <= other.calculate_location_value(opposite_direction)

    def __eq__(self, other):
        direction = self._calculate_direction_of_neighbor(other)
        opposite_direction = Direction.OPPOSITE(direction)
        return self.calculate_location_value(direction) == other.calculate_location_value(opposite_direction)

    def __ne__(self, other):
        direction = self._calculate_direction_of_neighbor(other)
        opposite_direction = Direction.OPPOSITE(direction)
        return self.calculate_location_value(direction) != other.calculate_location_value(opposite_direction)

    def __gt__(self, other):
        direction = self._calculate_direction_of_neighbor(other)
        opposite_direction = Direction.OPPOSITE(direction)
        return self.calculate_location_value(direction) > other.calculate_location_value(opposite_direction)

    def __ge__(self, other):
        direction = self._calculate_direction_of_neighbor(other)
        opposite_direction = Direction.OPPOSITE(direction)
        return self.calculate_location_value(direction) >= other.calculate_location_value(opposite_direction)

    @staticmethod
    def _calculate_neighbors(coordinates):
        neighbors = {}
        x, y = coordinates
        if x > 0:
            neighbors[Direction.LEFT] = (x - 1, y)
        if x < constants.GAME_GRID_WIDTH - 1:
            neighbors[Direction.RIGHT] = (x + 1, y)
        if y > 0:
            neighbors[Direction.TOP] = (x, y - 1)
        if y < constants.GAME_GRID_HEIGHT - 1:
            neighbors[Direction.BOTTOM] = (x, y + 1)
        return neighbors


class Grid:

    def __init__(self):
        # TODO store elsewhere?
        self.width = constants.GAME_GRID_WIDTH
        self.height = constants.GAME_GRID_HEIGHT

        self.data = [[GameBoardLocation((x, y)) for y in range(self.height)] for x in range(self.width)]

    def __getitem__(self, coordinates):
        x, y = coordinates
        return self.data[x][y]

    def __setitem__(self, coordinates, item):
        x, y = coordinates
        self.data[x][y] = item

    def initialize(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.data[x][y] is not None:
                    self.data[x][y].initialize()


class Game:

    def __init__(self, agents, display):
        self.is_game_over = False
        # This class will maintain all of the cards
        self.cards_handler = Cards()
        self.agents = agents
        self.display = display

        self.game_board = Grid()

        # Current player's turn
        self.current_turn_index = random.randint(0, constants.NUMBER_OF_PLAYERS - 1)

    def initialize(self):
        self.is_game_over = False
        self.game_board.initialize()
        self.current_turn_index = random.randint(0, constants.NUMBER_OF_PLAYERS - 1)

    def increment_agent_turn(self):
        self.current_turn_index = (self.current_turn_index + 1) % constants.NUMBER_OF_PLAYERS

    def run(self):
        """Main control loop for game play."""
        while not self.is_game_over:
            # Stuff happens

            self.increment_agent_turn()
            pass
