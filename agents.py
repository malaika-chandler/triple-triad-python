from textdisplay import TripleTriadColors
from abc import ABCMeta, abstractmethod


class Agent:
    """Base class for implementing a game player

    Attributes:
        index (int): The index of the player

    Methods:
        initialize: Prepares agent for a new game
        get_action: Throws NotImplemented error; should be implemented by subclass
        increment_score: Increments player score by 1
        decrement_score: Decrements player score by 1
        place_card_in_hand: Places a given card in the player's hand
        set_hand: Deals a full hand of cards to the player
        play_card: Removes a card from the player's hand
    """

    __metaclass__ = ABCMeta

    def __init__(self, index):
        self._hand = []
        self._index = index
        self._name = "Player {}".format(index + 1)
        self._score = 0

    def __deepcopy__(self, memo_dict={}):
        copy_agent = Agent(self._index)
        copy_agent._hand = list(self._hand)
        copy_agent._name = self._name
        copy_agent._score = self._score

        return copy_agent

    def initialize(self):
        self._hand = []
        self._score = 0

    @abstractmethod
    def get_action(self, game_state):
        raise NotImplemented("Method needs to be implemented in sub class")

    @property
    def name(self):
        return self._name

    @property
    def score(self):
        return self._score

    @property
    def index(self):
        return self._index

    @property
    def hand(self):
        return self._hand

    def increment_score(self):
        self._score += 1

    def decrement_score(self):
        self._score -= 1

    def place_card_in_hand(self, card):
        self._hand.append(card)

    def set_hand(self, dealt_cards):
        self._hand.clear()
        self._hand.extend(dealt_cards)
        self._score = len(dealt_cards)

    def play_card(self, selected_card):
        if selected_card in self._hand:
            # Remove card from hand and return
            self._hand.remove(selected_card)
            return selected_card
        # Card not in player's hand
        return None

    def __eq__(self, other):
        return self.score == other.score

    def __ge__(self, other):
        return self.score >= other.score

    def __le__(self, other):
        return self.score <= other.score

    def __lt__(self, other):
        return self.score < other.score

    def __gt__(self, other):
        return self.score > other.score

    def __ne__(self, other):
        return self.score != other.score


class FirstAvailableAgent(Agent):
    def __init__(self, index):
        super().__init__(index)

    """For Testing: Uses first available card in first available space"""
    def get_action(self, game_state):
        legal_cards, legal_grid_spaces = game_state.get_legal_agent_actions(self)
        return 0, list(legal_grid_spaces.values())[0].get_coordinates()


class MinMaxAgent(Agent):
    def __init__(self, index):
        super().__init__(index)

    def __deepcopy__(self, memo_dict={}):
        new_agent = MinMaxAgent(self._index)
        new_agent._index = self._index
        new_agent._hand = list(self._hand)
        new_agent._name = self.name
        new_agent._score = self.score

        return new_agent

    def get_action(self, game_state):
        legal_cards, legal_grid_spaces = game_state.get_legal_agent_actions(self)
        max_action = 0, list(legal_grid_spaces.values())[0].get_coordinates()
        value = float('-inf')
        depth = 9 % game_state.get_count_turns_remaining()

        print("Thinking...")

        # Go through each available card
        for card_index in range(len(legal_cards)):
            # Go through each available space on the board
            for coordinates, grid_space in legal_grid_spaces.items():
                # Generate possible game state successor
                result = self.dive_down(
                    game_state.generate_successor(self._index, (card_index, coordinates)),
                    depth
                )
                if value < result:
                    value = result
                    max_action = card_index, coordinates

        return max_action

    def dive_down(self, game_state, depth):
        game_state.increment_player_turn()
        current_agent = game_state.get_current_player()

        agents = game_state.get_agents()
        other_player_index = (self._index + 1) % len(agents)
        current_result = 100 * (agents[self._index].score - agents[other_player_index].score)
        if depth == 0:
            return current_result

        legal_cards, legal_grid_spaces = game_state.get_legal_agent_actions(current_agent)

        if current_agent.index == self._index:
            # Maximize own interests
            value = float('-inf')
            for card_index in range(len(legal_cards)):
                # Go through each available space on the board
                for coordinates, grid_space in legal_grid_spaces.items():
                    result = self.dive_down(
                        game_state.generate_successor(self._index, (card_index, coordinates)),
                        depth - 1
                    )
                    value = max(value, result + current_result)
            return value
        else:
            # Minimize opponent interests
            # TODO Can only check cards if open rule is in play
            value = float('-inf')
            for card_index in range(len(legal_cards)):
                # Go through each available space on the board
                for coordinates, grid_space in legal_grid_spaces.items():
                    result = self.dive_down(
                        game_state.generate_successor(self._index, (card_index, coordinates)),
                        depth - 1
                    )
                    value = max(value, result + current_result)
            return value


class KeyBoardAgent(Agent):
    def __init__(self, index):
        super().__init__(index)
        self.self_color = TripleTriadColors.AGENT_COLORS[index]

    def __deepcopy__(self, memo_dict={}):
        new_agent = KeyBoardAgent(self._index)
        new_agent._index = self._index
        new_agent._hand = list(self._hand)
        new_agent._name = self._name
        new_agent._score = self._score

        return new_agent

    def get_action(self, game_state):
        # Get legal cards/spaces
        legal_cards, legal_grid_spaces = game_state.get_legal_agent_actions(self)

        # Get player move
        card_index, coordinates = -1, None
        while not (0 <= card_index < len(legal_cards) and coordinates in legal_grid_spaces):
            player_input = input("{}'s turn: ".format(
                        self.self_color + self._name + TripleTriadColors.COLOR_RESET))
            result = player_input.split(' ')
            card_index, coordinates = int(result[0]) - 1, (int(result[1]), int(result[2]))

        return card_index, coordinates


class MouseAgent(Agent):
    def get_action(self, game_state):
        pass
    pass
