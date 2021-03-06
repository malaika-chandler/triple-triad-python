from components import Element, Card
import constants

import random


class Cards:

    """Class to handling generating and dealing cards for game usage"""

    def __init__(self):
        self.cards = {
            "1": [
                Card("Geezard", 1, 5, 4, 1, Element.NONE),
                Card("Funguar", 5, 3, 1, 1, Element.NONE),
                Card("Bite Bug", 1, 5, 3, 3, Element.NONE),
                Card("Red Bat", 6, 2, 1, 1, Element.NONE),
                Card("Blobra", 2, 5, 3, 1, Element.NONE),
                Card("Gayla", 2, 4, 1, 4, Element.THUNDER),
                Card("Gesper", 1, 1, 5, 4, Element.NONE),
                Card("Fastitocalon-F", 3, 1, 5, 2, Element.EARTH),
                Card("Blood Soul", 2, 1, 1, 6, Element.NONE),
                Card("Caterchipillar", 4, 3, 2, 4, Element.NONE),
                Card("Cockatrice", 2, 6, 1, 2, Element.THUNDER),
            ],
            "2": [
                Card("Grat", 7, 1, 1, 3, Element.NONE),
                Card("Buel", 6, 3, 2, 2, Element.NONE),
                Card("Mesmerize", 5, 4, 3, 3, Element.NONE),
                Card("Glacial Eye", 6, 3, 1, 4, Element.ICE),
                Card("Belhelmel", 3, 3, 4, 5, Element.NONE),
                Card("Thrustaevis", 5, 5, 3, 2, Element.WIND),
                Card("Anacondaur", 5, 5, 1, 3, Element.POISON),
                Card("Creeps", 5, 2, 2, 5, Element.THUNDER),
                Card("Grendel", 4, 2, 4, 5, Element.THUNDER),
                Card("Jelleye", 3, 7, 2, 1, Element.NONE),
                Card("Grand Mantis", 5, 3, 2, 5, Element.NONE),
            ],
            "3": [
                Card("Forbidden", 6, 2, 6, 3, Element.NONE),
                Card("Armadodo", 6, 6, 3, 1, Element.EARTH),
                Card("Tri-Face", 3, 5, 5, 5, Element.POISON),
                Card("Fastitocalon", 7, 3, 5, 1, Element.EARTH),
                Card("Snow Lion", 7, 3, 1, 5, Element.ICE),
                Card("Ochu", 5, 3, 6, 3, Element.NONE),
                Card("SAM08G", 5, 4, 6, 2, Element.FIRE),
                Card("Death Claw", 4, 2, 4, 7, Element.FIRE),
                Card("Cactuar", 6, 3, 2, 6, Element.NONE),
                Card("Tonberry", 3, 4, 6, 4, Element.NONE),
                Card("Abyss Worm", 7, 5, 2, 3, Element.EARTH),
            ],
            "4": [
                Card("Turtapod", 2, 7, 3, 6, Element.NONE),
                Card("Vysage", 6, 5, 5, 4, Element.NONE),
                Card("T-Rexaur", 4, 7, 6, 2, Element.NONE),
                Card("Bomb", 2, 3, 7, 6, Element.FIRE),
                Card("Blitz", 1, 7, 6, 4, Element.THUNDER),
                Card("Wendigo", 7, 6, 3, 1, Element.NONE),
                Card("Torama", 7, 4, 4, 4, Element.NONE),
                Card("Imp", 3, 6, 7, 3, Element.NONE),
                Card("Blue Dragon", 6, 3, 2, 7, Element.POISON),
                Card("Adamantoise", 4, 6, 5, 5, Element.EARTH),
                Card("Hexadragon", 7, 3, 5, 4, Element.FIRE),
            ],
            "5": [
                Card("Iron Giant", 6, 5, 5, 6, Element.NONE),
                Card("Behemoth", 3, 7, 6, 5, Element.NONE),
                Card("Chimera", 7, 3, 6, 5, Element.WATER),
                Card("PuPu", 3, 1, 10, 2, Element.NONE),
                Card("Elastoid", 6, 7, 2, 6, Element.NONE),
                Card("GIM47N", 5, 4, 5, 7, Element.NONE),
                Card("Malboro", 7, 2, 7, 4, Element.POISON),
                Card("Ruby Dragon", 7, 4, 2, 7, Element.FIRE),
                Card("Elnoyle", 5, 6, 3, 7, Element.NONE),
                Card("Tonberry King", 4, 4, 6, 7, Element.NONE),
                Card("Biggs, Wedge", 6, 7, 6, 2, Element.NONE),
            ],
            "6": [
                Card("Fujin, Raijin", 2, 4, 8, 8, Element.NONE),
                Card("Elvoret", 7, 4, 8, 3, Element.WIND),
                Card("X-ATM092", 4, 3, 8, 7, Element.NONE),
                Card("Granaldo", 7, 5, 2, 8, Element.NONE),
                Card("Gerogero", 1, 3, 8, 8, Element.POISON),
                Card("Iguion", 8, 2, 2, 8, Element.NONE),
                Card("Abadon", 6, 5, 8, 4, Element.NONE),
                Card("Trauma", 4, 6, 8, 5, Element.NONE),
                Card("Oilboyle", 1, 8, 8, 4, Element.NONE),
                Card("Shumi Tribe", 6, 4, 5, 8, Element.NONE),
                Card("Krysta", 7, 1, 5, 8, Element.NONE),
            ],
            "7": [
                Card("Propagator", 8, 8, 4, 4, Element.NONE),
                Card("Jumbo Cactuar", 8, 4, 8, 4, Element.NONE),
                Card("Tri-Point", 8, 8, 5, 2, Element.THUNDER),
                Card("Gargantua", 5, 8, 6, 6, Element.NONE),
                Card("Mobile Type 8", 8, 3, 6, 7, Element.NONE),
                Card("Sphinxara", 8, 8, 3, 5, Element.NONE),
                Card("Tiamat", 8, 4, 8, 5, Element.NONE),
                Card("BGH251F2", 5, 5, 7, 8, Element.NONE),
                Card("Red Giant", 6, 7, 8, 4, Element.NONE),
                Card("Catoblepas", 1, 7, 8, 7, Element.NONE),
                Card("Ultima Weapon", 7, 8, 7, 2, Element.NONE),
            ],
            "8": [
                Card("Chubby Chocobo", 4, 9, 4, 8, Element.NONE),
                Card("Angelo", 9, 3, 6, 7, Element.NONE),
                Card("Gilgamesh", 3, 6, 7, 9, Element.NONE),
                Card("MiniMog", 9, 2, 3, 9, Element.NONE),
                Card("Chicobo", 9, 4, 4, 8, Element.NONE),
                Card("Quezacotl", 2, 4, 9, 9, Element.THUNDER),
                Card("Shiva", 6, 9, 7, 4, Element.ICE),
                Card("Ifrit", 9, 8, 6, 2, Element.FIRE),
                Card("Siren", 8, 2, 9, 6, Element.NONE),
                Card("Sacred", 5, 9, 1, 9, Element.EARTH),
                Card("Minotaur", 9, 9, 5, 2, Element.EARTH),
            ],
            "9": [
                Card("Carbuncle", 8, 4, 4, 10, Element.NONE),
                Card("Diablos", 5, 3, 10, 8, Element.NONE),
                Card("Leviathan", 7, 7, 10, 1, Element.WATER),
                Card("Odin", 8, 5, 10, 3, Element.NONE),
                Card("Pandemona", 10, 7, 1, 7, Element.WIND),
                Card("Cerberus", 7, 10, 4, 6, Element.NONE),
                Card("Alexander", 9, 2, 10, 4, Element.HOLY),
                Card("Phoenix", 7, 10, 2, 7, Element.FIRE),
                Card("Bahamut", 10, 6, 8, 2, Element.NONE),
                Card("Doomtrain", 3, 10, 1, 10, Element.POISON),
                Card("Eden", 4, 10, 4, 9, Element.NONE),
            ],
            "10": [
                Card("Ward", 10, 8, 7, 2, Element.NONE),
                Card("Kiros", 6, 10, 7, 6, Element.NONE),
                Card("Laguna", 5, 9, 10, 3, Element.NONE),
                Card("Selphie", 10, 4, 8, 6, Element.NONE),
                Card("Quistis", 9, 2, 6, 10, Element.NONE),
                Card("Irvine", 2, 10, 6, 9, Element.NONE),
                Card("Zell", 8, 6, 5, 10, Element.NONE),
                Card("Rinoa", 4, 10, 10, 2, Element.NONE),
                Card("Edea", 10, 3, 10, 3, Element.NONE),
                Card("Seifer", 6, 4, 9, 10, Element.NONE),
                Card("Squall", 10, 9, 4, 6, Element.NONE),
            ],
        }

        self._wall_card = Card('WALL', 10, 10, 10, 10)

        # Only one of these cards in play at a time
        self.no_duplicates_in_play_level = 8

    def __str__(self):
        """
        Returns a concatenated string of Cards contained in the class
        :return:
        """
        return "\n".join("\n".join(str(card) for card in cards) for cards in self.cards.values())

    @property
    def wall_card(self):
        return self._wall_card

    def deal_cards(self):
        """ Uses a normal distribution to deal cards into hands.
            Prevents duplicate cards at or above the given level.
        """
        # TODO use rules to specify distribution of cards to return

        # Returns a list of lists of cards by level
        cards_to_filter = list(self.cards.values())

        # arbitrary for now
        standard_deviation = 15

        # Total number of cards divided by 2
        cards_per_level = len(cards_to_filter[0])
        total_cards = len(cards_to_filter) * cards_per_level
        mean = total_cards / 2

        hands = []
        while len(hands) < constants.NUMBER_OF_CARDS_IN_HAND * constants.NUMBER_OF_PLAYERS:
            number = round(random.gauss(mean, standard_deviation))
            if 0 <= number < total_cards:
                # Cards in lists separated by card level
                card_level_index = number // cards_per_level

                # List is 0 indexed, so level is index plus 1
                card_level = card_level_index + 1

                # Card itself will be at some index in level list
                card_index_in_level = number % cards_per_level

                selected_card = cards_to_filter[card_level_index][card_index_in_level]

                # Only one card in play after a certain level
                # And only one PuPu card!
                if (card_level >= self.no_duplicates_in_play_level or selected_card.name == 'PuPu') \
                        and selected_card in hands:
                    continue

                hands.append(selected_card)

        # Split into separate hands and return
        return tuple(hands[i:i + constants.NUMBER_OF_CARDS_IN_HAND]
                     for i in range(0, len(hands), constants.NUMBER_OF_CARDS_IN_HAND))

