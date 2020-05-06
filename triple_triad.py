from agents import KeyBoardAgent, FirstAvailableAgent
from game import Game
import constants
# from graphicsdisplay import TripleTriadGraphics
from textdisplay import TripleTriadGraphics


class Rules:

    def __init__(self, is_elemental=False):
        # Open and Random always
        self.is_open = True
        self.is_random = True

        # Card flip rules
        self.is_elemental = is_elemental
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
        for direction, neighbor in challenger.neighbors.items():
            if neighbor.has_card and neighbor.owner.index != challenger.owner.index:
                # GameBoardLocation checks if element rule in play
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
    # agents = [KeyBoardAgent(agent_index) for agent_index in range(constants.NUMBER_OF_PLAYERS)]
    agents = [
        KeyBoardAgent(0),
        FirstAvailableAgent(1)
    ]

    # Set up display
    display = TripleTriadGraphics()

    # Set up the rules
    rules = Rules(is_elemental=True)

    # Set up the game
    game = Game(agents, display, rules)

    # Start the game
    game.run()
