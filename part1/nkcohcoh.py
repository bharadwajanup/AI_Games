import heapq
from sys import argv as argv

import time

try:
    from board import Board as Board
    import queue as Queue
except ImportError:
    from board import Board as Board
    import Queue

"""
Design:
The program takes the current state of the board from the command line arguments, along with n and k values,
identifies whose turn is it now, evaluates the current state of the board and returns the best possible state
which could potentially lead to a win.

Assumptions:
If the game is already over (i.e. some player lost already), it would simply return the same board
The time limit parameter is ignored as the code puts out the local optimal state in under a second and then proceeds
to think about a better one if any.
The (row, col) value displayed on the terminal follow zero based indexes.
Tired of holding the "." key to complete the board? This program also takes 'new' as an argument in the command line
which would generate an empty board and starts playing.

Implementation Details:
Both priority queue and a heap is used to ensure the best move always stays on the top.
Class Board at file board.py has all state and evaluation related implementation. This file creates an object
of class Board using the board given in the command line, switches between players who try to play their best
possible move and puts the next state into a priority queue with the utility score. The queue always holds the best possible
move at its head.

Evaluation of moves:
The program tries to find the safest spot on the board where there are no other pieces 'k' spots from the row,
column or diagonal. Such positions get the highest point and are most likely to be chosen as the next move.
Once all such moves are exhausted, the program assigns penalty of ten for pieces it finds of itself and five for
obstructing the opponent's sequence which might have led to a losing scenario for the other player. The closer the
player is to losing the game, the more penalty will be put to his score. Once all the possible states are evaluated,
the priority queue picks the best possible move and puts it on the screen.

Some special cases:
1) As mentioned in assumptions, if the game is already over before evaluating, the program returns the same board
2) If all the successors somehow end up with the same terminal score, the program picks the best possible move
from its successors (i.e. one step from the initial state)
3) If the tree ends up with something that leads to a win (full points in terminal score), the loop traversal is stopped
and the subsequent next move is decided to be the next move.

I have tried to add comments in the code wherever possible.
"""

# Check if the arguments supplied are valid
if len(argv) != 5:
    print("Arguments not valid")
    exit(1)

n = int(argv[1])
k = int(argv[2])

if k > n:
    print("Invalid K value")
    exit(1)
identifier = 0  # Not used.


# Check if the supplied board is valid.
def has_valid_elements(argument):
    pattern = 'wb.'
    if argument.strip(pattern):
        return False
    return True


def validate_and_return_board(argument):
    global n
    if argument == "new":
        string = '.' * (n * n)
        return string
    if len(argument) != n * n or not has_valid_elements(argument):
        print("Invalid Board\n")
        exit(1)
    return argument


board = validate_and_return_board(argv[3])
duration = int(argv[4])  # Parameter ignored.

Board.N = n
Board.K = k


# Identify the max and min players.
def player(s):
    return ['b', 'w'] if s.count('w') > s.count('b') else ['w', 'b']


# Keep track of the original players when the initial board was supplied.
# This is to ensure that we don't lose track of whom should have the best next move possible.
def set_players(board):
    players = player(board)

    max_player = players[0]
    min_player = players[1]
    # print("It's %s's turn" % max_player)
    Board.origin_max_player = max_player
    Board.origin_min_player = min_player


# Adds a piece to the board at the given index.
# Returns a Board object.
def add_piece(board, i):
    if board.state[i] != ".":
        return False
    players = player(board.state)
    return Board.new_board(board.state, players[0], players[1], i)


# For the given board, get the next best possible move.
def get_next_move(board):
    successors = []
    for i in filter(lambda x: board.state[x] == '.', range(0, len(board))):
        potential_next_move = add_piece(board, i)

        if potential_next_move and potential_next_move.score == Board.K * 10:
            # print(str(potential_next_move) + " Score %d" % potential_next_move.score)
            return potential_next_move
        elif potential_next_move:
            # print(str(potential_next_move) + " Score %d" % potential_next_move.score)
            heapq.heappush(successors, potential_next_move)
    if len(successors) == 0:
        return board
    return heapq.heappop(successors)


# Is the supplied string constitutes as losing position for the player?
def check_for_lost_combination(string):
    str1 = Board.origin_max_player * k
    str2 = Board.origin_min_player * k
    if string.count(str1) > 0 or string.count(str2) > 0:
        return True
    return False


# Checks if the game is over or not.
def terminal_test(s):
    global n, k
    val = ""
    for row in range(0, n):
        val = s.state[n * row:n * (row + 1)]
        if check_for_lost_combination(val):
            return True

    for col in range(0, n):
        val = s.get_comparator_string(0, n - 1, col, "C")
        if check_for_lost_combination(val):
            return True
    # Temporarily set k to n
    s.K = n
    # go col-wise
    for col in range(0, (n - k + 1)):
        val = s.get_diagonal_comparator_string(0, col, 'LR')
        if check_for_lost_combination(val):
            return True
    # now row-wise
    for row in range(0, (n - k + 1)):
        val = s.get_diagonal_comparator_string(row, 0, 'LR')
        if check_for_lost_combination(val):
            return True
    s.K = k
    return False


# Gets all of the possible moves for the given board.
def actions(s):
    return [add_piece(s, i) for i in range(0, len(s)) if s.state[i] == "."]


# The Board object holds the score with respect to the "Max" player who played the last.
# This method adjusts the score to accomodate the actual "Max" player who started to play.
def get_actual_score(b):
    if b.score >= 0:
        return b.score
    if b.min_player == Board.origin_max_player:
        return -b.score
    return b.score


# Core method which takes a board string and returns the best possible move.
def play(board):
    set_players(board)
    initial_board = Board.new_board(board, Board.origin_max_player, Board.origin_min_player)
    temp_lst = Queue.PriorityQueue()
    if terminal_test(initial_board):
        action_lst = [initial_board]
    else:
        action_lst = actions(initial_board)

    heapq.heapify(action_lst)

    local_max = action_lst[0]
    # Print the best possible move locally first.
    print(str(local_max))
    score = -float("inf")
    max_score = - 2 * Board.K * 10
    while len(action_lst) > 0:
        a = heapq.heappop(action_lst)
        cur_board = a
        while True:

            cur_board = get_next_move(cur_board)

            if cur_board.score < 0:
                # print("%s won the game" % cur_board.min_player)
                score = get_actual_score(cur_board)
                if score > 0 and score > max_score:
                    print(a)
                    max_score = score
                break
            if str(cur_board).count('.') == 0 and cur_board.score > 0:
                # print("Match Drawn")
                score = get_actual_score(cur_board)
                if score > max_score:
                    print(a)
                    max_score = score
                break
        # negate the score as priority score always has the least number at the head of the list.
        temp_lst.put(((-score), a))
        if a.score == 100:
            break

    top_of_the_line = temp_lst.get()
    # If every possible move leads to a loss, print the local max.
    if top_of_the_line[0] == -(Board.K * 10):
        temp2 = local_max
    else:
        temp2 = top_of_the_line[1]
    print("Position: %s" % str(temp2.get_row_col(temp2.latest_change)))
    print(temp2)
    return temp2


# It all begins here.
board = play(str(board))

# Uncomment the below lines to make the program play by itself till the end.


# while True:
#     start_time = time.time()
#     board = play(str(board))
#     if terminal_test(board) or str(board).count('.') == 0:
#         print(" %s seconds" % (round((time.time() - start_time), 4)))
#         break
#     print(" %s seconds" % round((time.time() - start_time), 4))
#
# print(board.get_board())
# if board.score < 0:
#     print("%s won the game" % board.min_player)
# else:
#     print("Match drawn")
#
# print(board.latest_change)
