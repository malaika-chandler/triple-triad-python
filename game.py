import constants
from cards import Cards
from components import Direction, Element
import utils
import copy


class GameState:

    """ Class to handle the state of the game

    Attributes:
        agents (List[Agent]): The player agents
        rules (Rules): The game rules

    Methods:
        initialize: Returns game state to initial state
        get_count_turns_remaining: Returns the int count of remaining turns
        get_agents: Returns list of player agents
        get_current_player: Returns current playing Agent
        get_game_board: Returns the GameBoard object
        increment_player_turn: Increments turn index to next player
        get_legal_agent_actions: Returns a list of legal playable cards and
            a list of legal playable grid locations for a given player Agent
        generate_successor: Returns a deepcopy of the game state where a
            player Agent has placed a given card in a given location
        get_score: Returns the int score for a given player Agent
    """

    def __init__(self, agents, rules):
        self.data = GameStateData(agents=agents, game_board=Grid(rules))
        self.current_turn_index = 0
        self.rules = rules

        self.initialize()

    def initialize(self):
        self.data.initialize()
        # Random player goes first
        self.current_turn_index = utils.get_random_player_index(constants.NUMBER_OF_PLAYERS)

    def __deepcopy__(self, memo_dict={}):
        copied_agents = [copy.deepcopy(agent) for agent in self.data.agents]
        copied_state = GameState(copied_agents, self.rules)
        copied_state.data.game_board = copy.deepcopy(self.get_game_board())

        # Update Agent data stored in game board to reflect copied agents
        copied_state.get_game_board().remap_owners_for_deepcopy(copied_agents)

        return copied_state

    def get_count_turns_remaining(self):
        return self.data.game_board.count_free_spaces

    def get_agents(self):
        return self.data.agents

    def get_current_player(self):
        return self.data.agents[self.current_turn_index]

    def get_game_board(self):
        return self.data.game_board

    def increment_player_turn(self):
        self.current_turn_index = (self.current_turn_index + 1) % constants.NUMBER_OF_PLAYERS

    def get_legal_agent_actions(self, agent):
        legal_cards = agent.hand
        legal_grid_spaces = self.data.game_board.get_free_spaces_dict()

        return legal_cards, legal_grid_spaces

    def generate_successor(self, agent_index, action):
        # return a copy of the current game state after agent has taken action
        state_copy = copy.deepcopy(self)
        card_index, coordinates = action
        # TODO Make sure card and grid space are legal and valid
        agent = state_copy.data.agents[agent_index]
        state_copy.get_game_board().place_card(agent, agent.hand[card_index], coordinates)
        return state_copy

    def get_score(self, agent_index):
        return self.data.agents[agent_index].get_score()


class GameStateData:

    def __init__(self, agents, game_board):
        # Init game state
        self.agents = agents
        self.game_board = game_board

    def initialize(self):
        self.game_board.initialize()


class GameBoardLocation:

    """ Class to handle the individual spaces on the game board grid

    Attributes:
        coordinates (Tuple(int)): The x and y coordinates the object is located on the game board
        is_elemental_rule_in_play (bool): Whether or not elemental rule is in play for the game

    Methods:
        initialize: Returns the space to a fresh instance
        place_card: Handles placing a card in the given space
        set_owner: Handles setting the owner of the space to a given Agent
        calculate_location_value: Calculates the total rank of a space given a Direction
        get_location_rank: Returns the rank of the placed card given a direction
        get_coordinates: Returns the coordinates of the GameBoardLocation object
        get_combo_neighbors: Returns all neighbors with smaller adjoining ranks for use with Combo rule
        has_elemental_conflict: Returns true if space has non-NONE element and it doesn't match containing card's
        has_elemental_agreement: Returns true if space has non-NONE element and it does match the containing card's
        can_flip: Returns true if the card can flip its neighbor in a given Direction
        is_equal: Returns true if the card's and neighbor's card have equal ranks in a given Direction
        get_sum: Returns sum of the card's and neighbor's card ranks in a given Direction
        is_greater: Returns true if location rank is greater than neighboring rank
        _get_element_for_grid: For initialization purposes; returns an element to assign to the space
        _calculate_neighbors: For initialization purposes; generates a dictionary of neighboring GameBoardLocations
    """

    def __init__(self, coordinates, is_elemental_rule_in_play=False, is_same_wall_rule_in_play=False):
        self._has_card = False
        self._placed_card = None

        self._use_elemental_rule = is_elemental_rule_in_play
        self._use_same_wall_rule = is_same_wall_rule_in_play
        self._has_element = False
        self._element = Element.NONE
        self._get_element_for_grid()

        self._grid_coordinates = (coordinates[0], coordinates[1])
        self.owner = None

        self._neighbors_coordinates = self._calculate_neighbors(coordinates)
        self.neighbors = {}

    def __deepcopy__(self, memo_dict={}):
        if self._grid_coordinates in memo_dict:
            return memo_dict[self._grid_coordinates]

        copy_space = GameBoardLocation(self._grid_coordinates, self._use_elemental_rule)
        copy_space._has_card = self._has_card
        copy_space._placed_card = self._placed_card
        copy_space._has_element = self._has_element
        copy_space._element = self._element
        copy_space.owner = self.owner
        copy_space._neighbors_coordinates = self._neighbors_coordinates
        memo_dict[self._grid_coordinates] = copy_space

        return copy_space

    def initialize(self):
        self._has_card = False
        self._placed_card = None
        self._has_element = False
        self.owner = None

        self._get_element_for_grid()

    @property
    def has_card(self):
        return self._has_card

    @property
    def placed_card(self):
        return self._placed_card

    @property
    def neighbors_coordinates(self):
        return self._neighbors_coordinates

    @property
    def element(self):
        return self._element

    def place_card(self, agent, card):
        self._has_card = True
        self._placed_card = card
        self.owner = agent

    def set_owner(self, agent):
        self.owner = agent

    def calculate_location_value(self, rank_direction):
        if self._has_card:
            elemental_addend = 0
            if self._use_elemental_rule:
                if self.has_elemental_agreement():
                    elemental_addend = 1
                elif self.has_elemental_conflict():
                    elemental_addend = -1
            return self._placed_card.get_rank(rank_direction) + elemental_addend
        return -1

    def get_location_rank(self, rank_direction):
        if self._has_card:
            return self._placed_card.get_rank(rank_direction)
        return -1

    def get_coordinates(self):
        return self._grid_coordinates

    def get_combo_neighbors(self):
        return {
            direction: neighbor
            for direction, neighbor in self.neighbors.items()
            if self.is_greater(neighbor, direction)
        }

    def has_elemental_conflict(self):
        return self._has_card and self._element != Element.NONE and self._element != self._placed_card.element

    def has_elemental_agreement(self):
        return self._has_card and self._element != Element.NONE and self._element == self._placed_card.element

    def can_flip(self, neighbor, direction):
        if self is neighbor:
            return False
        opposite_direction = direction.get_opposite()
        return self.calculate_location_value(direction) > neighbor.calculate_location_value(opposite_direction)

    def is_equal(self, neighbor, direction):
        if self is neighbor:
            return False
        opposite_direction = direction.get_opposite()
        return self.get_location_rank(direction) == neighbor.get_location_rank(opposite_direction)

    def get_sum(self, neighbor, direction):
        if self is neighbor:
            return False
        opposite_direction = direction.get_opposite()
        return self.get_location_rank(direction) + neighbor.get_location_rank(opposite_direction)

    def is_greater(self, neighbor, direction):
        if self is neighbor:
            return False
        opposite_direction = direction.get_opposite()
        return self.get_location_rank(direction) > neighbor.get_location_rank(opposite_direction)

    def _get_element_for_grid(self):
        if self._use_elemental_rule:
            if utils.flip_coin():
                self._element = utils.random_choice([e for e in Element])
                if self._element != Element.NONE:
                    self._has_element = True
            else:
                self._element = Element.NONE
        else:
            self._element = Element.NONE

    def _calculate_neighbors(self, coordinates):
        neighbors = {}
        x, y = coordinates
        if self._use_same_wall_rule:
            # Walls will be included as "neighbors"
            neighbors[Direction.LEFT] = (x - 1, y)
            neighbors[Direction.RIGHT] = (x + 1, y)
            neighbors[Direction.TOP] = (x, y - 1)
            neighbors[Direction.BOTTOM] = (x, y + 1)
        else:
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

    """ Class to handle the actual game board grid logic for GameBoardPlaces.

    Attributes:
        rules (Rules): The rules of the game
    """

    def __init__(self, rules):
        self._width = constants.GAME_GRID_WIDTH
        self._height = constants.GAME_GRID_HEIGHT
        self._count_free_spaces = 0
        self.rules = rules

        # Create a GameBoardLocation object for each space in the grid
        # Pass the game board specific rules needed
        self.data = [
            [GameBoardLocation((x, y),
                               is_elemental_rule_in_play=rules.is_elemental,
                               is_same_wall_rule_in_play=rules.is_same_wall) for x in range(self._width)]
            for y in range(self._height)]

        # Link GameBoardLocations now that they're initialized
        for x in range(self._width):
            for y in range(self._height):
                for key, value in self[(x, y)].neighbors_coordinates.items():
                    if value[0] not in range(self._width) or value[1] not in range(self._height):
                        # This is a wall
                        self[(x, y)].neighbors[key] = GameBoardLocation(value)
                        self[(x, y)].neighbors[key].place_card(None, Cards.wall_card)
                    else:
                        self[(x, y)].neighbors[key] = self[value]

        self.initialize()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def count_free_spaces(self):
        return self._count_free_spaces

    def get_row(self, row_index):
        if 0 <= row_index < self._height:
            return self.data[row_index]
        return None

    def __getitem__(self, coordinates):
        x, y = coordinates
        return self.data[y][x]

    def __deepcopy__(self, memo_dict={}):
        copy_grid = Grid(self.rules)
        copy_grid._count_free_spaces = self._count_free_spaces
        copy_grid.data = [[copy.deepcopy(self[(x, y)]) for x in range(self._width)] for y in range(self._height)]

        # Map copied neighbors to each other
        for x in range(copy_grid._width):
            for y in range(copy_grid._height):
                for key, value in copy_grid[(x, y)].neighbors_coordinates.items():
                    if value[0] not in range(self._width) or value[1] not in range(self._height):
                        # This is a wall
                        copy_grid[(x, y)].neighbors[key] = GameBoardLocation(value)
                        copy_grid[(x, y)].neighbors[key].place_card(None, Cards.wall_card)
                    else:
                        copy_grid[(x, y)].neighbors[key] = copy_grid[value]

        return copy_grid

    def remap_owners_for_deepcopy(self, copied_agents):
        for x in range(self._width):
            for y in range(self._height):
                if self[(x, y)].owner is not None:
                    self[(x, y)].set_owner(copied_agents[self[(x, y)].owner.index])

    def get_free_spaces_dict(self):
        free_spaces = {}
        for x in range(self._width):
            for y in range(self._height):
                if self[(x, y)] is not None and not self[(x, y)].has_card:
                    free_spaces[(x, y)] = (self[(x, y)])
        return free_spaces

    def place_card(self, agent, card, coordinates):
        if not self[coordinates].has_card:
            self[coordinates].place_card(agent, card)
            self._count_free_spaces -= 1

            self.rules.handle_card_placement(self[coordinates])
            return True
        return False

    def initialize(self):
        for x in range(self._width):
            for y in range(self._height):
                if self[(x, y)] is not None:
                    if self.rules.is_sudden_death and self[(x, y)].has_card:
                        # Put cards owned by players into corresponding hand
                        self[(x, y)].owner.place_card_in_hand(self[(x, y)].placed_card)
                    self[(x, y)].initialize()

        self._count_free_spaces = self._width * self._height


class Game:

    """ Class that handles the game process

    Attributes:
        agents (List[Agent]): The players of the game
        display (Display): The Display class to show game status
        rules (Rules): The rules the game should use

    Methods:
        initialize: Handles initializing a Game instance for playing
        increment_agent_turn: Changes index indicating which Agent's turn it is
        calculate_winner: Compares Agent's scores and determines the winner
        run: Handles the actual game loop
    """

    def __init__(self, agents, display, rules):
        self.is_game_over = False
        # This class will maintain all of the cards
        self.cards_handler = Cards()
        self.display = display
        self.rules = rules

        self.game_state = GameState(agents, rules)
        self.game_board = self.game_state.get_game_board()
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

    def main_loop(self):
        """Main control loop for game play."""
        while not self.is_game_over:
            # Player's turn
            current_player = self.game_state.get_current_player()
            self.display.display_game_state(self.game_state)
            legal_cards, legal_grid_spaces = self.game_state.get_legal_agent_actions(current_player)
            card_index, coordinates = current_player.get_action(self.game_state)
            self.game_board.place_card(current_player, current_player.play_card(legal_cards[card_index]), coordinates)

            self.is_game_over = self.game_board.count_free_spaces == 0
            self.increment_agent_turn()

    def run(self):
        """Start the game"""

        # Deal the cards
        hands = self.cards_handler.deal_cards()
        for i in range(constants.NUMBER_OF_PLAYERS):
            self.agents[i].set_hand(hands[i])

        while True:
            self.main_loop()

            if self.rules.is_sudden_death and self.calculate_winner() is None:
                # Sudden death is in effect; prepare for next round
                self.game_board.initialize()
                self.is_game_over = False

            # TODO Tell display sudden death has occurred
                print("SUDDEN DEATH IN PLAY")

            else:
                break

        self.game_state.winner = self.calculate_winner()
        self.display.display_end_game(self.game_state)
