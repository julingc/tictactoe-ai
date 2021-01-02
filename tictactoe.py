"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """   
    # Make board state in one list 
    movecounts = board[0] + board[1] + board[2]

    # Count the number of X and O
    X_movecounts = movecounts.count(X)
    O_movecounts = movecounts.count(O)

    if X_movecounts == O_movecounts:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """   
    # Initialize an empty possible actions set
    possible_actions = set()

    # Loop over all possible actions which are EMPTY
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Deep copy the board to avoid being modified
    new_board = copy.deepcopy(board)

    # Raise exception if action is not a valid action
    if action not in actions(board):
        raise Exception("Action is invalid.")
    else:
        i = action[0]
        j = action[1]
        new_board[i][j] = player(board)
        return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check if one wins game with 3 of their moves in a row horizontally and vertically
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]

    # Check if one wins game with 3 of their moves in a row diagonally
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    # Make board state in one list to count the number of EMPTY
    movecounts = board[0] + board[1] + board[2]

    # Check if either O or X has won, or game has ended in a tie
    if winner(board) == O or winner(board) == X or movecounts.count(EMPTY) == 0:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Return None if board is terminal board
    while terminal(board) == True:
        return None
    else:
        if player(board) == X:
            v, optimal_action = max_value_action(board)
            return optimal_action
        if player(board) == O:
            v, optimal_action = min_value_action(board)
            return optimal_action
    raise NotImplementedError

def min_value_action(board):
    """
    Returns best value and the optimal action (i, j) for O player
    """
    if terminal(board) == True:
        return utility(board), None
    
    v = math.inf
    v_temp = math.inf
    for action in actions(board):
        X_value, X_action = max_value_action(result(board, action))
        v = min(v, X_value)

        if v < v_temp:
            v_temp = v
            O_action = action

        # Alpha-beta pruning
        if v < X_value:
            break    
    return v, O_action

def max_value_action(board):
    """
    Returns best value and the optimal action (i, j) for X player
    """
    if terminal(board) == True:
        return utility(board), None

    v = -math.inf  
    v_temp = -math.inf
    for action in actions(board):
        O_value, O_action = min_value_action(result(board, action))
        v = max(v, O_value)

        if v > v_temp:
            v_temp = v
            X_action = action

        # Alpha-beta pruning
        if O_value < v:
            break    
    return v, X_action
