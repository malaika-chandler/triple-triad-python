import colorama  # Fore, Back, Style
from components import Direction, Element


class TripleTriadColors:
    COLOR_RESET = colorama.Style.RESET_ALL
    AGENT_COLORS = [
        colorama.Fore.LIGHTBLUE_EX,
        colorama.Fore.LIGHTMAGENTA_EX
    ]
    COLOR_NEGATIVE = colorama.Fore.RED
    COLOR_POSITIVE = colorama.Fore.GREEN


class TripleTriadGraphics:

    def __init__(self):
        colorama.init()
        self.colors = TripleTriadColors

    def display_game_state(self, state):
        non_turn_agent = [agent for agent in state.get_agents() if not agent.index == state.get_current_player().index]
        non_turn_agent = non_turn_agent[0]

        # Draw agents' hands and game board based on state
        self.draw_cards(non_turn_agent.hand, non_turn_agent.index)
        self.display_score(non_turn_agent)
        self.draw_game_board(state.get_game_board())
        self.display_score(state.get_current_player())
        self.draw_cards(state.get_current_player().hand, state.get_current_player().index)

    def display_end_game(self, state):
        self.draw_game_board(state.get_game_board())
        for agent in state.get_agents():
            self.display_score(agent)

        if state.winner:
            print(state.winner.get_name() + " wins!")
        else:
            print("Draw")

    def draw_game_board(self, game_board):
        height = game_board.height
        for row_index in range(height):
            row = game_board.get_row(row_index)
            row_to_draw = []

            individual_grid_representations = []
            for i, place in enumerate(row):
                representation = []
                if place.has_card:
                    # Create the entire card as a list
                    placed_card = place.placed_card
                    color = self.colors.AGENT_COLORS[place.owner.index]
                    representation.append(color + ' ▁▁▁▁▁ ' + self.colors.COLOR_RESET)
                    representation.append(color + '|  {} {}|'.format(
                        placed_card.get_rank(Direction.TOP, as_string=True),
                        self.get_elemental_result(place) + color) + self.colors.COLOR_RESET),
                    representation.append(color + '| {}{}{} |'.format(
                        placed_card.get_rank(Direction.LEFT, as_string=True),
                        self._get_element_char(placed_card.get_element()) or ' ',
                        placed_card.get_rank(Direction.RIGHT, as_string=True)) + self.colors.COLOR_RESET)
                    representation.append(color + '|  {}  |'.format(
                        placed_card.get_rank(Direction.BOTTOM, as_string=True)) + self.colors.COLOR_RESET)
                    representation.append(color + ' ▔▔▔▔▔ ' + self.colors.COLOR_RESET)
                else:
                    # Create the entire grid space as a list
                    x, y = place.get_coordinates()
                    representation.append(' ▁▁▁▁▁ ')
                    representation.append('|  {}  |'.format(self._get_element_char(place.get_element()) or ' '))
                    representation.append('| {},{} |'.format(x, y))
                    representation.append('|     |')
                    representation.append(' ▔▔▔▔▔ ')
                individual_grid_representations.append(representation)

            # Get each first list entry, concat, and append to row object
            count_representations = len(individual_grid_representations)
            for line_index in range(len(individual_grid_representations[0])):
                row_to_draw.append('  '.join(
                    individual_grid_representations[i][line_index] for i in range(count_representations)
                ))

            print('\n'.join(row_to_draw), sep='\n')

    def get_elemental_result(self, place):
        if place.has_card:
            if place.has_elemental_conflict():
                return self.colors.COLOR_NEGATIVE + '↓' + self.colors.COLOR_RESET
            elif place.has_elemental_agreement():
                return self.colors.COLOR_POSITIVE + '↑' + self.colors.COLOR_RESET
        return ' '

    def draw_cards(self, cards, agent_index):
        # Horizontally
        top_edge = '  '.join([' ▁▁{}▁▁'.format(i + 1) for i in range(len(cards))])
        top_rank = ' '.join(['|  {}  |'.format(card.get_rank(Direction.TOP, as_string=True)) for card in cards])
        middle_ranks = ' '.join(['| {}{}{} |'.format(
            card.get_rank(Direction.LEFT, as_string=True),
            self._get_element_char(card.get_element()) or ' ',
            card.get_rank(Direction.RIGHT, as_string=True)) for card in cards])
        bottom_rank = ' '.join(['|  {}  |'.format(card.get_rank(Direction.BOTTOM, as_string=True)) for card in cards])
        bottom_edge = '  '.join([' ▔▔▔▔▔' for _ in cards])

        print(self.colors.AGENT_COLORS[agent_index], top_edge, top_rank,
              middle_ranks, bottom_rank, bottom_edge, self.colors.COLOR_RESET, sep="\n")

    def display_score(self, agent):
        print('Score for {}{}{}: {}'.format(self.colors.AGENT_COLORS[agent.index], agent.get_name(),
                                            self.colors.COLOR_RESET, agent.get_score()))

    @staticmethod
    def _get_element_char(element):
        if element == Element.FIRE:
            return '♨'  # '🔥'
        elif element == Element.EARTH:
            return '☄︎'  # '🌏'
        elif element == Element.ICE:
            return '❄︎'  # '❄️'
        elif element == Element.THUNDER:
            return '⚡︎'  # '⚡'
        elif element == Element.HOLY:
            return '✟'  # '✨'
        elif element == Element.POISON:
            return '☠'
        elif element == Element.WIND:
            return '᭝'  # '🌪'
        elif element == Element.WATER:
            return '☔︎'  # '💧'
        else:
            return ''
