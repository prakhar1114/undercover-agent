from random import randint
import random
from wordlist import word_pairs
from enum import Enum
from typing import Optional


class PlayerType(Enum):
    MR_WHITE = 1
    UNDERCOVER_AGENT = 2
    CIVILIAN = 3


def play_game(player_list, num_mr_white, num_undercover_agent, player_scores):
    num_players = len(player_list)
    current_players = player_list.copy()
    # pick num_mr_white players from players to be mr white
    mr_white_list = []
    for i in range(int(num_mr_white)):
        mr_white_list.append(player_list.pop(randint(0, num_players - 1)))
        num_players -= 1

    # pick num_undercover_agent players from the remaining players to be undercover agent
    undercover_agent_list = []
    for i in range(int(num_undercover_agent)):
        undercover_agent_list.append(player_list.pop(randint(0, num_players - 1)))
        num_players -= 1

    # the remaining players are civilians
    civilians_list = player_list

    original_player_dict = {
        PlayerType.MR_WHITE: mr_white_list.copy(),
        PlayerType.UNDERCOVER_AGENT: undercover_agent_list.copy(),
        PlayerType.CIVILIAN: civilians_list.copy(),
    }
    # # print the roles
    # print('\n')
    # print('Mr White:')
    # for player in mr_white_list:
    #     print(player)
    # print('\n')
    # print('Undercover Agent:')
    # for player in undercover_agent_list:
    #     print(player)
    # print('\n')
    # print('Civilians:')
    # for player in civilians_list:
    #     print(player)
    # print('\n')

    # select a word pair randomly from the word_pairs list
    word_pair = word_pairs[randint(0, len(word_pairs) - 1)]

    # pick one word randomly to be civilian word and other to be undercover agent word
    word_list = list(word_pair)
    civilian_word = word_list.pop(randint(0, 1))
    undercover_agent_word = word_list.pop()

    """
    Now call out the players one by one and tell them their words.
    The players should be called out in the order their names were entered.
    For civilians, tell them "<player_name>: your word is <civilian_word>"
    For undercover agent, tell them "<player_name>: your word is <undercover_agent_word>"
    For mr white, tell them "<player_name>: you are mr white"
    """

    for player in current_players:
        input(f"player {player}. Press Enter when you are the only seeing the screen")

        if player in civilians_list:
            # Prompt the user and wait for Enter key
            input(f"Your word is {civilian_word}. Please press enter to continue")

            # Clear the line after pressing Enter
            print("\033[A\033[K", end="")

        elif player in undercover_agent_list:
            # Prompt the user and wait for Enter key
            input(
                f"Your word is {undercover_agent_word}. Please press enter to continue"
            )

            # Clear the line after pressing Enter
            print("\033[A\033[K", end="")

        elif player in mr_white_list:
            # Prompt the user and wait for Enter key
            input(f"You are mr white. Please press enter to continue")

            # Clear the line after pressing Enter
            print("\033[A\033[K", end="")

    mr_white_info = []
    i = 0
    while True:
        shuffled_player_list = create_shuffled_list(current_players, mr_white_list)
        print(f"Order of play {shuffled_player_list}")

        i += 1
        print(f"Round {i} begins")
        input("May the discussions begin. Press Enter when you are ready to vote")

        print(
            "Current Players {}".format(
                [f"{i} player {player}" for i, player in enumerate(current_players)]
            )
        )
        player_num_to_eliminate = int(
            input("Which player would you like to eliminate? Write the player number: ")
        )

        player_eliminated = current_players.pop(player_num_to_eliminate)
        print(f"Player {player_eliminated} has been eliminated")

        # if mr white is eliminated, he cant get scores there
        is_game_over, player_type, who_won = check_game_over(
            player_eliminated, mr_white_list, undercover_agent_list, civilians_list
        )

        if not is_game_over:
            if player_type == PlayerType.MR_WHITE:
                mr_white_thinks = input(
                    f"Mr White has been eliminated. Guess the word player {player_eliminated}: "
                )
                if mr_white_thinks == civilian_word:
                    mr_white_info.append(
                        f"player {player_eliminated} ,this Mr White wins"
                    )
                    player_scores[player_eliminated] += 6
                else:
                    mr_white_info.append(
                        f"player {player_eliminated} ,this Mr White loses"
                    )
                    player_scores[player_eliminated] += 0

        else:
            if player_type == PlayerType.MR_WHITE:
                mr_white_thinks = input(
                    f"Mr White has been eliminated. Guess the word player {player_eliminated}: "
                )
                if mr_white_thinks == civilian_word:
                    mr_white_info.append(
                        f"player {player_eliminated} ,this Mr White wins"
                    )
                    player_scores[player_eliminated] += 6
                else:
                    mr_white_info.append(
                        f"player {player_eliminated} ,this Mr White loses"
                    )
                    player_scores[player_eliminated] += 0

            if who_won == PlayerType.CIVILIAN:
                for player in civilians_list:
                    player_scores[player] += 2

            elif who_won == PlayerType.UNDERCOVER_AGENT:
                for player in undercover_agent_list:
                    player_scores[player] += 10
                for player in mr_white_list:
                    player_scores[player] += 6
            else:
                raise ValueError(f"who_won is not a valid value")

        if is_game_over:
            break

    print("Game over \n")
    print(f"Mr Whites {original_player_dict[PlayerType.MR_WHITE]} \n")
    print(f"Undercover Agents {original_player_dict[PlayerType.UNDERCOVER_AGENT]} \n")
    print(f"Civilians {original_player_dict[PlayerType.CIVILIAN]} \n")
    print("\n")
    print(mr_white_info)
    print("\n")
    print("Final scores:")
    for player, score in player_scores.items():
        print(f"{player}: {score}")

    play_next_round = input("Play another round? (y/n): ")
    if play_next_round.lower() == "y":
        return True
    else:
        return False


def check_game_over(
    player_eliminated, mr_white_list, undercover_agent_list, civilians_list
) -> tuple[bool, Enum, Optional[Enum]]:
    if player_eliminated in mr_white_list:
        mr_white_list.remove(player_eliminated)
        player_type = PlayerType.MR_WHITE
    elif player_eliminated in undercover_agent_list:
        undercover_agent_list.remove(player_eliminated)
        player_type = PlayerType.UNDERCOVER_AGENT
    elif player_eliminated in civilians_list:
        civilians_list.remove(player_eliminated)
        player_type = PlayerType.CIVILIAN
    else:
        raise ValueError(f"Player {player_eliminated} not found in any list")

    if len(mr_white_list) == 0 and len(undercover_agent_list) == 0:
        print("Game over. Civilians win")
        return True, player_type, PlayerType.CIVILIAN
    elif len(civilians_list) == 1:
        print("Undercover Agent and Mr White wins")
        return True, player_type, PlayerType.UNDERCOVER_AGENT
    else:
        return False, player_type, None


def create_shuffled_list(original_list, exclusion_list):
    print("generating a 'random' order of players")
    while True:
        # Shuffling the original list
        shuffled_list = original_list.copy()
        random.shuffle(shuffled_list)

        # Check if the first element is not in the exclusion list
        if shuffled_list[0] not in exclusion_list:
            return shuffled_list


if __name__ == "__main__":
    players = input("Enter comma separated player names: ")

    player_list = players.split(",")

    print("Players playing:")
    for player in player_list:
        print(player)

    num_mr_white = input("Enter number of mr white: ")
    num_undercover_agent = input("Enter number of undercover agent: ")

    player_scores = {player: 0 for player in player_list}

    while True:
        play_another_round = play_game(
            player_list.copy(), num_mr_white, num_undercover_agent, player_scores
        )
        if not play_another_round:
            break

    print("Thanks for playing")
    print("Hope you enjoyed the game")
