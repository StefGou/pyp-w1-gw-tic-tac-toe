from .exceptions import InvalidMovement, GameOver
# internal helpers
def _position_is_empty_in_board(position, board):
    """
    Checks if given position is empty ("-") in the board.

    :param position: Two-elements tuple representing a
                     position in the board. Example: (0, 1)
    :param board: Game board.

    Returns True if given position is empty, False otherwise.
    """
    return board[position[0]][position[1]] == "-"


def _position_is_valid(position):
    """
    Checks if given position is a valid. To consider a position as valid, it
    must be a two-elements tuple, containing values from 0 to 2.
    Examples of valid positions: (0,0), (1,0)
    Examples of invalid positions: (0,0,1), (9,8), False

    :param position: Two-elements tuple representing a
                     position in the board. Example: (0, 1)

    Returns True if given position is valid, False otherwise.
    """
    # print(position)
    if not isinstance(position, tuple) \
            or len(position) > 2 \
            or not all(isinstance(x, int) for x in position) \
            or any(i > 2 for i in position) \
            or any(x for x in position if x < 0):
        return False

    return True


def _board_is_full(board):
    """
    Returns True if all positions in given board are occupied.

    :param board: Game board.
    """
    for row in board:
        for colum in row:
            if colum == "-":
                return False
    return True


def _is_winning_combination(board, combination, player):
    """
    Checks if all 3 positions in given combination are occupied by given player.

    :param board: Game board.
    :param combination: Tuple containing three position elements.
                        Example: ((0,0), (0,1), (0,2))

    Returns True of all three positions in the combination belongs to given
    player, False otherwise.
    """
    for c in combination:
        if board[c[0]][c[1]] != player:
            return False
    return True


def _check_winning_combinations(board, player):
    """
    There are 8 posible combinations (3 horizontals, 3, verticals and 2 diagonals)
    to win the Tic-tac-toe game.
    This helper loops through all these combinations and checks if any of them
    belongs to the given player.

    :param board: Game board.
    :param player: One of the two playing players.

    Returns the player (winner) of any of the winning combinations is completed
    by given player, or None otherwise.
    """
    winning_combinations = (
        ((0, 0), (0, 1), (0, 2)),
        ((1, 0), (1, 1), (1, 2)),
        ((2, 0), (2, 1), (2, 2)),
        ((0, 0), (1, 0), (2, 0)),
        ((0, 1), (1, 1), (2, 1)),
        ((0, 2), (1, 2), (2, 2)),
        ((0, 0), (1, 1), (2, 2)),
        ((0, 2), (1, 1), (2, 0))
    )

    for combination in winning_combinations:
        if _is_winning_combination(board, combination, player):
            return player
    return None

# public interface
def start_new_game(player1, player2):
    """
    Creates and returns a new game configuration.
    """
    return {
    'player1': "X",
    'player2': "O",
    'board': [
        ["-", "-", "-"],
        ["-", "-", "-"],
        ["-", "-", "-"],
    ],
    'next_turn': "X",
    'winner': None
}


def get_winner(game):
    """
    Returns the winner player if any, or None otherwise.
    """
    return game['winner']


def move(game, player, position):
    """
    Performs a player movement in the game. Must ensure all the pre requisites
    checks before the actual movement is done.
    After registering the movement it must check if the game is over.
    """
    #print("p:", player, get_next_turn(game))
    if not get_next_turn(game) == player:
        if _board_is_full(game['board']) or game['winner'] != None:
            raise InvalidMovement('Game is over.')
        else:
            raise InvalidMovement('"' + str(get_next_turn(game)) + '" moves next.')

    print(_position_is_valid(position))

    if _position_is_valid(position) == False:
        raise InvalidMovement("Position out of range.")

    if not _position_is_empty_in_board(position, game['board']):
        raise InvalidMovement("Position already taken.")

    if _board_is_full(game['board']):
            raise GameOver('Game is over.')

    else:
        game['board'][position[0]][position[1]] = player

        game['winner'] = _check_winning_combinations(game['board'], player)
        print("Win:", _check_winning_combinations(game['board'], player), game['winner'])

        if game['winner'] != None:
            raise GameOver('"' + str(player) + '" wins!')

        elif _board_is_full(game['board']):
            raise GameOver('Game is tied!')

        if player == "O":
            next_player = "X"
        else:
            next_player = "O"
        #print("next:", next_player)
        game['next_turn'] = next_player
        #print("after:", game['next_turn'])


def get_board_as_string(game):
    """
    Returns a string representation of the game board in the current state.
    """
    str_board = "\n"
    row = 0
    for i in range(1, 6):
        if i % 2 != 0:
            str_board += "{}  |  {}  |  {}".format(game['board'][row][0], game['board'][row][1], game['board'][row][2])
            row += 1
        else:
            str_board += "--------------"

        str_board += "\n"

    return str_board


def get_next_turn(game):
    """
    Returns the player who plays next, or None if the game is already over.
    """
    return game['next_turn']
