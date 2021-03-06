from agents import KeyBoardAgent, MinMaxAgent
from game import Game
from textdisplay import TripleTriadGraphics

import sys


class Rules:

    """Class to handle the application of rules in the Triple Triad game

    Attributes:
        use_elemental (bool): Sets the elemental rule
        use_same (bool): Sets the same rule
        use_same_wall (bool): Sets the same wall rule
        use_plus (bool): Sets the plus rule
        use_sudden_death (bool): Sets the sudden death rule

    Methods:
        handle_card_placement: handles what happens after a card is placed on the board
            using whatever rules are present in a given game and increments Agent scores.
            Currently, only Elemental rule has been implemented
        _handle_combo:
        _handle_score_change:
    """

    def __init__(self,
                 use_elemental=False,
                 use_same=False,
                 use_same_wall=False,
                 use_plus=False,
                 use_sudden_death=False):
        # Open and Random always
        self._is_open = True
        self._is_random = True

        # Card flip rules
        self._is_elemental = use_elemental
        self._is_same = use_same
        self._is_same_wall = use_same and use_same_wall
        self._is_plus = use_plus
        self._is_combo = self._is_same or self._is_plus

        # End of game rules
        self._is_sudden_death = use_sudden_death

    @property
    def is_elemental(self):
        return self._is_elemental

    @property
    def is_same_wall(self):
        return self._is_same_wall

    @property
    def is_sudden_death(self):
        return self._is_sudden_death

    def handle_card_placement(self, challenger):
        # The challenger contains references to the neighbor spaces/cards

        count_opposing_player_spaces = 0
        neighbors_with_cards = {}
        for direction, neighbor in challenger.neighbors.items():
            if neighbor.has_card:
                neighbors_with_cards[direction] = neighbor
                if neighbor.owner and neighbor.owner.index != challenger.owner.index:
                    count_opposing_player_spaces += 1

        if self._is_same:
            if count_opposing_player_spaces > 0 and len(neighbors_with_cards) > 1:
                # Same Wall neighbors will be included if added to rules already
                same_neighbors = {
                    direction: neighbor
                    for direction, neighbor in neighbors_with_cards.items()
                    if challenger.is_equal(neighbor, direction)
                }
                if len(same_neighbors) >= 2:
                    # They will be flipped
                    # TODO display should be notified of SAME success
                    print("SAME!")
                    combo_occurred = False
                    for direction, neighbor in same_neighbors.items():
                        Rules._handle_ownership_change(challenger, neighbor)

                        if self._is_combo:
                            combo_result = self._handle_combo(challenger, neighbor.get_combo_neighbors().values())
                            combo_occurred = combo_occurred or combo_result

                    if combo_occurred:
                        # TODO display should be notified of COMBO success
                        print("COMBO!")

        if self._is_plus:
            combo_occurred = False
            if count_opposing_player_spaces > 0:
                plus_neighbors = {}
                for direction, neighbor in neighbors_with_cards.items():
                    # Don't grab the wall entities
                    if neighbor.owner:
                        plus_value = challenger.get_sum(neighbor, direction)
                        if str(plus_value) in plus_neighbors:
                            plus_neighbors[str(plus_value)][direction] = neighbor
                        else:
                            plus_neighbors[str(plus_value)] = {direction: neighbor}

                # Only care about sums with more than one neighbor
                for affected_neighbors in plus_neighbors.values():
                    if len(affected_neighbors) >= 2:
                        # They will be flipped
                        # TODO display should be notified of PLUS success
                        print("PLUS!")

                        # These neighbors share a sum with the challenger, so flip them
                        for affected_neighbor in affected_neighbors.values():
                            Rules._handle_ownership_change(challenger, affected_neighbor)

                            if self._is_combo:
                                neighbors_neighbors = affected_neighbor.get_combo_neighbors().values()
                                combo_result = self._handle_combo(challenger, neighbors_neighbors)
                                combo_occurred = combo_occurred or combo_result

                if combo_occurred:
                    # TODO display should be notified of COMBO success
                    print("COMBO!")

        # Standard flip rules
        for direction, neighbor in neighbors_with_cards.items():
            if neighbor.owner and neighbor.owner.index != challenger.owner.index:
                # GameBoardLocation checks if element rule in play
                if challenger.can_flip(neighbor, direction):
                    Rules._handle_ownership_change(challenger, neighbor)

    @staticmethod
    def _handle_combo(challenger, affected_neighbors):
        # Flip all neighbors of the flipped neighbor with smaller ranks on directional sides
        combo_occurred = False
        for neighbors_neighbor in affected_neighbors:
            if neighbors_neighbor.owner and neighbors_neighbor.owner.index != challenger.owner.index:
                combo_occurred = True
                Rules._handle_ownership_change(challenger, neighbors_neighbor)

        return combo_occurred

    @staticmethod
    def _handle_ownership_change(challenger, neighbor):
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
    parser.add_option('-w', '--same-wall', dest='use_same_wall_rule', action='store_true',
                      help='the game will observe the same wall rule')
    parser.add_option('-p', '--plus', dest='use_plus_rule', action='store_true',
                      help='the game will observe the plus rule')
    parser.add_option('-d', '--sudden-death', dest='use_sudden_death_rule', action='store_true',
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
    rules = Rules(use_elemental=arguments['use_elemental_rule'],
                  use_same=arguments['use_same_rule'],
                  use_same_wall=arguments['use_same_wall_rule'],
                  use_plus=arguments['use_plus_rule'],
                  use_sudden_death=arguments['use_sudden_death_rule'])

    # Set up the game
    game = Game(agents, display, rules)

    # Start the game
    game.run()
