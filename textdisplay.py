import colorama  # Fore, Back, Style
from components import Direction


class TripleTriadGraphics:

    def __init__(self):
        colorama.init()
        self.color_reset = colorama.Style.RESET_ALL
        self.colors = [
            colorama.Fore.LIGHTBLUE_EX,
            colorama.Fore.LIGHTMAGENTA_EX
        ]

    def display_game_state(self, state):
        non_turn_agent = [agent for agent in state.agents if not agent.index == state.get_current_player().index]
        non_turn_agent = non_turn_agent[0]

        # Draw agents' hands and game board based on state
        self.draw_cards(non_turn_agent.hand, non_turn_agent.index)
        self.display_score(non_turn_agent)
        self.draw_game_board(state.get_game_board())
        self.display_score(state.get_current_player())
        self.draw_cards(state.get_current_player().hand, state.get_current_player().index)

    def display_end_game(self, state):
        self.draw_game_board(state.get_game_board())
        for agent in state.agents:
            self.display_score(agent)

        if state.winner:
            print(state.winner.get_name() + " wins!")
        else:
            print("Draw")

    def player_turn(self, agent):
        # Something like input?
        player_input = input("{}'s turn: ".format(
            self.colors[agent.index] + agent.get_name() + self.color_reset))
        result = player_input.split(' ')
        return int(result[0]) - 1, (int(result[1]), int(result[2]))

    # def draw_player_hands(self, agents):
    #     pass

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
                    color = self.colors[place.owner.index]
                    representation.append(color + ' ▁▁▁▁▁ ' + self.color_reset)
                    representation.append(color + '|  {}  |'.format(
                        placed_card.get_rank(Direction.TOP, as_string=True)) + self.color_reset)
                    representation.append(color + '| {}{}{} |'.format(
                        placed_card.get_rank(Direction.LEFT, as_string=True),
                        placed_card.get_element().character_representation() or ' ',
                        placed_card.get_rank(Direction.RIGHT, as_string=True)) + self.color_reset)
                    representation.append(color + '|  {}  |'.format(
                        placed_card.get_rank(Direction.BOTTOM, as_string=True)) + self.color_reset)
                    representation.append(color + ' ▔▔▔▔▔ ' + self.color_reset)
                else:
                    # Create the entire grid space as a list
                    x, y = place.get_coordinates()
                    representation.append(' ▁▁▁▁▁ ')
                    representation.append('|     |')
                    representation.append('| {},{} |'.format(x, y))
                    representation.append('|     |')
                    representation.append(' ▔▔▔▔▔ ')
                individual_grid_representations.append(representation)

            # Grid location height, based on how many lines were appended for each space
            grid_height = 3

            # Get each first list entry, concat, and append to row object
            count_representations = len(individual_grid_representations)
            for line_index in range(len(individual_grid_representations[0])):
                row_to_draw.append('  '.join(individual_grid_representations[i][line_index] for i in range(count_representations)))

            print('\n'.join(row_to_draw), sep='\n')

    def draw_cards(self, cards, agent_index):
        # Horizontally
        top_edge = '  '.join([' ▁▁{}▁▁'.format(i + 1) for i in range(len(cards))])
        top_rank = ' '.join(['|  {}  |'.format(card.get_rank(Direction.TOP, as_string=True)) for card in cards])
        middle_ranks = ' '.join(['| {}{}{} |'.format(
            card.get_rank(Direction.LEFT, as_string=True),
            card.get_element().character_representation() or ' ',
            card.get_rank(Direction.RIGHT, as_string=True)) for card in cards])
        bottom_rank = ' '.join(['|  {}  |'.format(card.get_rank(Direction.BOTTOM, as_string=True)) for card in cards])
        bottom_edge = '  '.join([' ▔▔▔▔▔' for i in cards])

        print(self.colors[agent_index], top_edge, top_rank,
              middle_ranks, bottom_rank, bottom_edge, self.color_reset, sep="\n")

        pass

    def display_score(self, agent):
        print('Score for {}{}{}: {}'.format(self.colors[agent.index], agent.get_name(),
                                            self.color_reset, agent.get_score()))
        pass
