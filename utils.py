import random


def get_random_player_index(number_of_players):
    return random.randint(0, number_of_players - 1)


def flip_coin():
    return random.randint(0, 1)


def random_choice(list_object):
    return random.choice(list_object)

