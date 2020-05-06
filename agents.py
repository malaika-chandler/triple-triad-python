from textdisplay import TripleTriadColors


class Agent:
    def __init__(self, index):
        self.hand = []
        self.index = index
        self.name = "Player {}".format(index + 1)
        self.score = 0

    def initialize(self):
        self.hand = []
        self.score = 0

    def get_action(self, game_state):
        raise NotImplemented("Method needs to be implemented in sub class")

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

    def get_name(self):
        return self.name

    def get_score(self):
        return self.score

    def increment_score(self):
        self.score += 1

    def decrement_score(self):
        self.score -= 1

    def set_hand(self, dealt_cards):
        self.hand.clear()
        self.hand.extend(dealt_cards)
        self.score = len(dealt_cards)

    def play_card(self, selected_card):
        if selected_card in self.hand:
            # Remove card from hand and return
            self.hand.remove(selected_card)
            return selected_card
        # Card not in player's hand
        return None


class FirstAvailableAgent(Agent):
    def __init__(self, index):
        super().__init__(index)

    """For Testing: Uses first available card in first available space"""
    def get_action(self, game_state):
        legal_cards, legal_grid_spaces = game_state.get_legal_agent_actions(self)
        return 0, list(legal_grid_spaces.values())[0].get_coordinates()


class KeyBoardAgent(Agent):
    def __init__(self, index):
        super().__init__(index)
        self.self_color = TripleTriadColors.AGENT_COLORS[index]

    def get_action(self, game_state):
        # Get legal cards/spaces
        legal_cards, legal_grid_spaces = game_state.get_legal_agent_actions(self)

        # Get player move
        card_index, coordinates = -1, None
        while not (0 <= card_index < len(legal_cards) and coordinates in legal_grid_spaces):
            player_input = input("{}'s turn: ".format(
                        self.self_color + self.get_name() + TripleTriadColors.COLOR_RESET))
            result = player_input.split(' ')
            card_index, coordinates = int(result[0]) - 1, (int(result[1]), int(result[2]))

        return card_index, coordinates


class MouseAgent(Agent):
    def get_action(self, game_state):
        pass
    pass
