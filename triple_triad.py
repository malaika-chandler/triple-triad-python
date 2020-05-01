from game import Game
import constants
# from graphicsdisplay import TripleTriadGraphics
from textdisplay import TripleTriadGraphics


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


class Rules:

    def __init__(self):
        # Open and Random always
        self.is_open = True
        self.is_random = True

        # Card flip rules
        self.is_elemental = False
        self.is_same = False
        self.is_same_wall = False
        self.is_plus = False
        self.is_combo = self.is_same or self.is_plus

        # End of game rules
        self.is_sudden_death = False

    def handle_card_placement(self, challenger):
        # The challenger contains references to the neighbor spaces/cards

        # Maintain number of cards flipped; zero sum game means for all
        # cards flipped, that's points gained by one agent and lost by
        # the other
        count_cards_flipped = 0

        # Standard flip rules
        # TODO add checks in for elemental for standard flips
        for direction, neighbor in challenger.neighbors.items():
            if neighbor.has_card and neighbor.owner.index != challenger.owner.index:
                if challenger.can_flip(neighbor, direction):
                    neighbor.owner.decrement_score()
                    neighbor.set_owner(challenger.owner)
                    challenger.owner.increment_score()

        # TODO implement more complicated rules
        if self.is_same:
            pass
        if self.is_same_wall:
            pass
        if self.is_plus:
            pass
        if self.is_combo:
            pass

        return count_cards_flipped


# Entry point for the triple triad game
if __name__ == '__main__':

    # Set up players
    agents = [Agent(agent_index) for agent_index in range(constants.NUMBER_OF_PLAYERS)]

    # Set up display
    display = TripleTriadGraphics()

    # Set up the rules
    rules = Rules()

    # Set up the game
    game = Game(agents, display, rules)

    # Start the game
    game.run()
