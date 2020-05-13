from agents import KeyBoardAgent, FirstAvailableAgent, MinMaxAgent
from game import Game
from textdisplay import TripleTriadGraphics

import sys


class Rules:

    """Class to handle the application of rules in the Triple Triad game

    Attributes:
        is_elemental (bool): Sets the elemental rule
        is_same (bool): Sets the same rule
        is_same_wall (bool): Sets the same wall rule
        is_plus (bool): Sets the plus rule
        is_sudden_death (bool): Sets the sudden death rule

    Methods:
        handle_card_placement: handles what happens after a card is placed on the board
            using whatever rules are present in a given game and increments Agent scores.
            Currently, only Elemental rule has been implemented
    """

    def __init__(self, is_elemental=False, is_same=False, is_same_wall=False, is_plus=False, is_sudden_death=False):
        # Open and Random always
        self.is_open = True
        self.is_random = True

        # Card flip rules
        self.is_elemental = is_elemental
        self.is_same = is_same
        self.is_same_wall = is_same and is_same_wall
        self.is_plus = is_plus
        self.is_combo = self.is_same or self.is_plus

        # End of game rules
        self.is_sudden_death = is_sudden_death

    def use_elemental_rule(self):
        return self.is_elemental

    def handle_card_placement(self, challenger):
        # The challenger contains references to the neighbor spaces/cards

        # TODO implement more complicated rules
        if self.is_same:
            pass
        if self.is_same_wall:
            pass
        if self.is_plus:
            pass
        if self.is_combo:
            pass

        # Standard flip rules
        for direction, neighbor in challenger.neighbors.items():
            if neighbor.has_card and neighbor.owner.index != challenger.owner.index:
                # GameBoardLocation checks if element rule in play
                if challenger.can_flip(neighbor, direction):
                    neighbor.owner.decrement_score()
                    neighbor.set_owner(challenger.owner)
                    challenger.owner.increment_score()


def read_command(argv):
    from optparse import OptionParser
    usage_str = """
  USAGE:      python triple_triad.py <options>
  EXAMPLES:   (1) python triple_triad.py
                  - starts a game with default rules
              (2) python triple_triad.py --elemental
              OR  python triple_triad.py -e
                  - starts a game using the elemental rule
  """
    parser = OptionParser(usage_str)
    parser.add_option('-e', '--elemental', dest='use_elemental_rule', action='store_true',
                      help='the game will observe the elemental rule')
    parser.add_option('-s', '--same', dest='use_same_rule', action='store_true',
                      help='the game will observe the same rule')
    parser.add_option('-w', '--same_wall', dest='use_same_wall_rule', action='store_true',
                      help='the game will observe the same wall rule')
    parser.add_option('-p', '--plus', dest='use_plus_rule', action='store_true',
                      help='the game will observe the plus rule')
    parser.add_option('-d', '--sudden_death', dest='use_sudden_death_rule', action='store_true',
                      help='the game will observe the sudden death rule')

    options, junk = parser.parse_args(argv)
    if len(junk) != 0:
        raise Exception('Command line input not understood: ' + str(junk))

    parsed_arguments = dict()
    parsed_arguments['use_elemental_rule'] = options.use_elemental_rule or False
    parsed_arguments['use_same_rule'] = options.use_same_rule or False
    parsed_arguments['use_same_wall_rule'] = options.use_same_wall_rule or False
    parsed_arguments['use_plus_rule'] = options.use_plus_rule or False
    parsed_arguments['use_sudden_death_rule'] = options.use_sudden_death_rule or False

    return parsed_arguments


# Entry point for the triple triad game
if __name__ == '__main__':

    arguments = read_command(sys.argv[1:])

    # Set up players
    # agents = [KeyBoardAgent(agent_index) for agent_index in range(constants.NUMBER_OF_PLAYERS)]
    agents = [
        KeyBoardAgent(0),
        MinMaxAgent(1)
    ]

    # Set up display
    display = TripleTriadGraphics()

    # Set up the rules
    rules = Rules(is_elemental=arguments['use_elemental_rule'],
                  is_same=arguments['use_same_rule'],
                  is_same_wall=arguments['use_same_wall_rule'],
                  is_plus=arguments['use_plus_rule'],
                  is_sudden_death=arguments['use_sudden_death_rule'])

    # Set up the game
    game = Game(agents, display, rules)

    # Start the game
    game.run()
