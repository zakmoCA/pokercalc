import random
from enum import IntEnum
from itertools import combinations

def parse_card(card_str):
    rank_values = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
        "t": 10, "j": 11, "q": 12, "k": 13, "a": 14
    }
    card = card_str.lower()
    rank = rank_values.get(card[0], None)
    if rank is None:
        raise ValueError(f"invalid card rank: {card}")
    return rank

def prompts():
    prompts = {
        "non_parsed": {
            "hole_cards": "what are your hole cards? ",
            "board": "what cards are currently on the board? ",
        },
        "parse_as_int": {
            "total_players": "how many players in total? ",
            "live_players": "how many players in the hand? ",
        },
    }

    str_prompts = {}
    converted_prompts = {}

    for key, values in prompts.items():
        for param, question in values.items():
            user_input = input(question)
            str_prompts[param] = user_input
            if key == "parse_as_int":
                converted_prompts[param] = int(user_input)

    all_prompts = {**str_prompts, **converted_prompts}
    return all_prompts

def get_input(prompts):
    user_input = {}
    for key, question in prompts.items():
        response = input(question)
        split_response = [*response]
        user_input[key] = int(response) if key in {"total_players", "live_players"} else split_response
    return user_input

def get_user_input():
    user_input = prompts()
    hole_cards = user_input["hole_cards"]
    board_cards = user_input["board"]
    parsed_hole_cards = [parse_card(card) for card in hole_cards]
    parsed_board_cards = [parse_card(card) for card in board_cards] if board_cards != "0" else []
    board_length = len(board_cards)
    user_params = {
        **user_input,
        "parsed_hole_cards": parsed_hole_cards,
        "parsed_board_cards": parsed_board_cards
    }
    return user_params, board_length

def create_players(total_players, user_params):
    user = {"name": "User", "hand": list(user_params["hole_cards"])}
    pc_players = [{"name": f"Player {i+1}", "hand": []} for i in range(total_players - 1)]
    return user, pc_players

def create_deck():
    suits = ['h', 'd', 'c', 's']
    ranks = list(range(2, 15))
    return [(rank, suit) for suit in suits for rank in ranks]

def deal_hands(pc_players, deck):
    random.shuffle(deck)
    for _ in range(2):
        for player in pc_players:
            player["hand"].append(deck.pop())
    return deck

def select_round_players(all_players, round_players):
    return random.sample(all_players, round_players)

def determine_round(board_size):
    match board_size:
        case 0:
            print("pre-flop")
        case 3:
            print("flop")
        case 4:
            print("turn")
        case 5:
            print("river")
    return board_size

class HandRank(IntEnum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

def generate_combinations(cards, r):
    if len(cards) < r:
        return []
    return list(combinations(cards, r))

def get_possible_hands(hole_cards, board_cards, remaining_deck):
    all_cards = hole_cards + board_cards
    cards_needed = 5 - len(all_cards)
    
    if cards_needed > 0:
        possible_additions = generate_combinations(remaining_deck, cards_needed)
        user_combos = [tuple(all_cards + list(addition)) for addition in possible_additions]
    else:
        user_combos = generate_combinations(all_cards, 5)

    opponent_hole_combos = generate_combinations(remaining_deck, 2)
    opponent_hands = [
        combo for hole_pair in opponent_hole_combos
        for combo in generate_combinations(list(hole_pair) + board_cards, 5)
    ]
    
    return user_combos, opponent_hands

def evaluate_hand(hand):
    pass

def check_straight(ranks):
    sorted_ranks = sorted(set(ranks))
    if len(sorted_ranks) < 5:
        return False
    if 14 in ranks:  # Ace high
        sorted_ranks.append(1)
    for i in range(len(sorted_ranks) - 4):
        if sorted_ranks[i + 4] - sorted_ranks[i] == 4:
            return True
    return False

def compare_hands(hand1, hand2):
    pass

def compare_tie_breakers(tie_break1, tie_break2):
    pass

def calculate_equity(player_hand, opponent_hands):
    total_hands = len(opponent_hands)
    wins = 0
    for opponent_hand in opponent_hands:
        result = 1
        # result = compare_hands(player_hand, opponent_hand)
        if result > 0:
            wins += 1
        elif result == 0:
            wins += 0.5
    return wins / total_hands


def simulate_round(live_deck, user_hole_cards, pc_hole_cards, board_cards, total_players, active_players):
    if len(user_hole_cards) + len(board_cards) < 3:
        return 0

    remaining_deck = [
        card for card in live_deck
        if card not in user_hole_cards
        and card not in board_cards
        and not any(card in player_hand for player_hand in pc_hole_cards)
    ]

    user_combos, opponent_hands = get_possible_hands(user_hole_cards, board_cards, remaining_deck)
    
    if not user_combos:
        return 0

    total_equity = 0
    for user_combo in user_combos:
        total_equity += calculate_equity(user_combo, opponent_hands)

    return total_equity / len(user_combos)

def game_loop():
    unshuffled_deck = create_deck()
    user_params, board_length = get_user_input()
    board_texture = user_params.get("board")
    user_hand = user_params.get("hole_cards")
    total_players_count = user_params.get("total_players")
    number_of_players_in_current_round = user_params.get("live_players")

    user, pc_players = create_players(total_players_count, user_params)
    all_game_players = [user] + pc_players

    updated_deck = deal_hands(pc_players, unshuffled_deck)
    current_rounds_players = select_round_players(
        pc_players, number_of_players_in_current_round - 1
    )

    round_simulation = simulate_round(
        updated_deck,
        user_params["parsed_hole_cards"],
        [player["hand"] for player in pc_players],
        user_params["parsed_board_cards"],
        total_players_count,
        current_rounds_players + [user]
    )

    print(f"round simulation result: {round_simulation}")

game_loop()