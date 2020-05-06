import constants
from cards import Cards
from components import Direction, Element
import utils


class GameState:

    def __init__(self, agents, rules):
        self.data = None
        self.agents = agents
        self.game_board = Grid(rules)
        self.current_turn_index = 0

        self.initialize()

    def initialize(self):
        self.game_board.initialize()
        # Random player goes first
        self.current_turn_index = utils.get_random_player_index(constants.NUMBER_OF_PLAYERS)

    def get_current_player(self):
        return self.agents[self.current_turn_index]

    def get_game_board(self):
        return self.game_board

    def increment_player_turn(self):
        self.current_turn_index = (self.current_turn_index + 1) % constants.NUMBER_OF_PLAYERS

    def get_legal_agent_actions(self, agent):
        legal_cards = agent.hand
        legal_grid_spaces = self.game_board.get_free_spaces_dict()

        return legal_cards, legal_grid_spaces

    def get_score(self, agent_index):
        return self.agents[agent_index].getScore()


class GameStateData:

    def __init__(self):
        # Init game state
        pass


class GameBoardLocation:
    def __init__(self, coordinates, is_elemental_rule_in_play=False):
        self.has_card = False
        self.placed_card = None

        self.is_elemental_rule_in_play = is_elemental_rule_in_play
        self.has_element = False
        self.element = Element.NONE
        self._get_element_for_grid()

        self.grid_coordinates = (coordinates[0], coordinates[1])
        self.owner = None

        self.neighbors_coordinates = self._calculate_neighbors(coordinates)
        self.neighbors = {}

    def initialize(self):
        self.has_card = False
        self.placed_card = None
        self.has_element = False
        self.owner = None

        self._get_element_for_grid()

    def place_card(self, agent, card):
        self.has_card = True
        self.placed_card = card
        self.owner = agent

    def set_owner(self, agent):
        self.owner = agent

    def calculate_location_value(self, rank_direction):
        if self.has_card:
            elemental_addend = 0
            # TODO Pass data to rules method for specific calculating
            if self.is_elemental_rule_in_play and self.has_element:
                if self.element == self.placed_card.get_element():
                    elemental_addend = 1
                else:
                    elemental_addend = -1
            return self.placed_card.get_rank(rank_direction) + elemental_addend
        return -1

    def get_coordinates(self):
        return self.grid_coordinates

    def get_element(self):
        return self.element

    def has_elemental_conflict(self):
        return self.has_card and self.element != Element.NONE and self.element != self.placed_card.get_element()

    def has_elemental_agreement(self):
        return self.has_card and self.element != Element.NONE and self.element == self.placed_card.get_element()

    def can_flip(self, neighbor, direction):
        if self is neighbor:
            return False
        opposite_direction = direction.get_opposite()
        return self.calculate_location_value(direction) > neighbor.calculate_location_value(opposite_direction)

    def _get_element_for_grid(self):
        if self.is_elemental_rule_in_play:
            if utils.flip_coin():
                self.element = utils.random_choice([e for e in Element])
                if self.element != Element.NONE:
                    self.has_element = True
            else:
                self.element = Element.NONE
        else:
            self.element = Element.NONE

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

    def __init__(self, rules):
        # TODO store elsewhere?
        self.width = constants.GAME_GRID_WIDTH
        self.height = constants.GAME_GRID_HEIGHT
        self.count_free_spaces = 0
        self.rules = rules

        # Create a GameBoardLocation object for each space in the grid
        self.data = [
            [GameBoardLocation((x, y), is_elemental_rule_in_play=rules.is_elemental) for x in range(self.width)]
            for y in range(self.height)]

        # Link GameBoardLocations now that they're initialized
        for x in range(self.width):
            for y in range(self.height):
                for key, value in self[(x, y)].neighbors_coordinates.items():
                    self[(x, y)].neighbors[key] = self[value]

        self.initialize()

    def get_row(self, row_index):
        if 0 <= row_index < self.height:
            return self.data[row_index]
        return None

    def __getitem__(self, coordinates):
        x, y = coordinates
        return self.data[y][x]

    def get_free_spaces_dict(self):
        free_spaces = {}
        for x in range(self.width):
            for y in range(self.height):
                if self[(x, y)] is not None and not self[(x, y)].has_card:
                    free_spaces[(x, y)] = (self[(x, y)])
        return free_spaces

    def place_card(self, agent, card, coordinates):
        if not self[coordinates].has_card:
            self[coordinates].place_card(agent, card)
            self.count_free_spaces -= 1

            self.rules.handle_card_placement(self[coordinates])
            return True
        return False

    def initialize(self):
        for x in range(self.width):
            for y in range(self.height):
                if self[(x, y)] is not None:
                    self[(x, y)].initialize()

        self.count_free_spaces = self.width * self.height


class Game:

    def __init__(self, agents, display, rules):
        self.is_game_over = False
        # This class will maintain all of the cards
        self.cards_handler = Cards()
        self.display = display
        self.rules = rules

        self.game_state = GameState(agents, rules)
        self.agents = agents

    def initialize(self):
        self.is_game_over = False
        self.game_state.initialize()

    def increment_agent_turn(self):
        self.game_state.increment_player_turn()

    def calculate_winner(self):
        res = all(agent == self.agents[0] for agent in self.agents)
        if res:
            return None
        else:
            return max(self.agents)

    def run(self):
        # Start the game
        game_board = self.game_state.get_game_board()

        # TODO make this better/easier to read
        # Deal the cards
        hands = self.cards_handler.deal_cards()
        for i in range(constants.NUMBER_OF_PLAYERS):
            self.agents[i].set_hand(hands[i])

        """Main control loop for game play."""
        while not self.is_game_over:
            # Player's turn
            current_player = self.game_state.get_current_player()

            self.display.display_game_state(self.game_state)

            legal_cards, legal_grid_spaces = self.game_state.get_legal_agent_actions(current_player)

            # Get player move
            card_index, coordinates = -1, None
            while not (0 <= card_index < len(legal_cards) and coordinates in legal_grid_spaces):
                # result = self.display.player_turn(current_player)
                result = current_player.get_action()
                card_index, coordinates = result

            game_board.place_card(current_player,
                                  current_player.play_card(legal_cards[card_index]),
                                  coordinates)

            self.is_game_over = game_board.count_free_spaces == 0

            self.increment_agent_turn()

        self.game_state.winner = self.calculate_winner()
        self.display.display_end_game(self.game_state)
