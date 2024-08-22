import random


def prompts():
    prompts = {
        "non_parsed": {
            "hole_cards": "what are your hole cards? ",
            "board": "what cards are currently on the board?: ",
        },
        "parse_as_int": {
            "total_players": "how many players in total? ",
            "live_players": "how many players in the hand? ",
        },
    }

    str_prompts = {}
    converted_prompts = {}  # user cards, total/live players, input board cards

    for key, values in prompts.items():
        for param, question in values.items():
            user_input = input(question)
            str_prompts[param] = user_input
            if key == "parse_as_int":
                converted_prompts[param] = int(user_input)

    all_prompts = {**str_prompts, **converted_prompts}

    return all_prompts


def get_user_input():

    user_input = prompts()

    board_texture = list(user_input["board"])
    number_of_board_cards = len(board_texture)
    user_params = {**user_input, "board_texture": board_texture}

    return user_params, number_of_board_cards


def create_players(total_players):
    return [{"name": f"player {i}", "hand": []} for i in range(total_players)]


def select_round_players(all_players, round_players):
    return random.sample(all_players, round_players)


def seat_and_deal_hands(players, deck):
    random.shuffle(deck)

    for _ in range(2):
        for player in players:
            player["hand"].append(deck.pop())

    print(f"resulting deck:       {deck}")
    print(players)

    return deck


def create_deck():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    return [(rank, suit) for suit in suits for rank in ranks]


def determine_round(board_size):
    card_amount = board_size
    round = 0
    match card_amount:
        case 0:
            print("pre-flop")
        case 3:
            round += 1
            print("flop")
        case 4:
            round += 2
            print("turn")
        case 5:
            round += 3
            print("river")
    return round


def game_loop():
    BOARD = []
    unshuffled_deck = create_deck()

    rank_values = {
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9",
        "10": "10",
        "J": "J" or "j",
        "Q": "Q" or "q",
        "K": "K" or "k",
        "A": "A" or "a",
    }

    user_params, number_of_board_cards = get_user_input()
    total_players_count = user_params.get("total_players")
    number_of_players_in_current_round = user_params.get("live_players")
    round_from_params = determine_round(number_of_board_cards)
    all_game_players = create_players(total_players_count)

    updated_deck = seat_and_deal_hands(all_game_players, unshuffled_deck)
    current_rounds_players = select_round_players(all_game_players, number_of_players_in_current_round)

    all_dealt_cards = [card for player in all_game_players for card in player["hand"]]
    intersection = set(all_dealt_cards) & set(updated_deck)


game_loop()
