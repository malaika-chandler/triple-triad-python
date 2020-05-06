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
    def get_action(self):
        pass

    pass


class KeyBoardAgent(Agent):
    def __init__(self, index):
        super().__init__(index)
        self.self_color = TripleTriadColors.AGENT_COLORS[index]

    def get_action(self):
        # Something like input?
        player_input = input("{}'s turn: ".format(
            self.self_color + self.get_name() + TripleTriadColors.COLOR_RESET))
        result = player_input.split(' ')
        return int(result[0]) - 1, (int(result[1]), int(result[2]))

    pass


class MouseAgent(Agent):
    def get_action(self):
        pass
    pass
