import heapq
from sys import argv as argv

# import time
try:
    from board import Board as Board
    import queue as Queue
except ImportError:
    from board import Board as Board
    import Queue

if len(argv) != 5:
    print("Arguments not valid")
    exit(1)

n = int(argv[1])
k = int(argv[2])

if k > n:
    print("Invalid K value")
    exit(1)
identifier = 0


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
duration = int(argv[4])  # TODO: Work on implementing time

Board.N = n
Board.K = k


def get_index(r, c):
    return r * n + c


def player(s):
    return ['b', 'w'] if s.count('w') > s.count('b') else ['w', 'b']


def set_players(board):
    players = player(board)

    max_player = players[0]
    min_player = players[1]
    # print("It's %s's turn" % max_player)
    Board.origin_max_player = max_player
    Board.origin_min_player = min_player


def add_piece(board, i):
    if board.state[i] != ".":
        return False
    players = player(board.state)
    return Board.new_board(board.state, players[0], players[1], i)


def get_next_move(board):
    successors = []
    for i in filter(lambda x: board.state[x] == '.', range(0, len(board))):
        potential_next_move = add_piece(board, i)

        if potential_next_move and potential_next_move.score == 100:
            # print(str(potential_next_move) + " Score %d" % potential_next_move.score)
            return potential_next_move
        elif potential_next_move:
            # print(str(potential_next_move) + " Score %d" % potential_next_move.score)
            heapq.heappush(successors, potential_next_move)
    if len(successors) == 0:
        return board
    return heapq.heappop(successors)


def check_for_lost_combination(string):
    str1 = Board.origin_max_player * k
    str2 = Board.origin_min_player * k
    if string.count(str1) > 0 or string.count(str2) > 0:
        return True
    return False


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
    # Tempororily set k to n
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


def actions(s):
    return [add_piece(s, i) for i in range(0, len(s)) if s.state[i] == "."]


def get_actual_score(b):
    if b.score >= 0:
        return b.score
    if b.min_player == Board.origin_max_player:
        return -b.score
    return b.score


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

        temp_lst.put(((-score), a))
        if a.score == 100:
            break

    top_of_the_line = temp_lst.get()
    if top_of_the_line[0] == -(Board.K * 10):
        temp2 = local_max
    else:
        temp2 = top_of_the_line[1]
    print("Position: %s" % str(temp2.get_row_col(temp2.latest_change)))
    print(temp2)
    return temp2


# start_time = time.time()
board = play(str(board))
# print(" %s seconds" % (round((time.time() - start_time), 4)))

# while True:
#     start_time = time.time()
#     board = play(str(board))
#     if terminal_test(board) or str(board).count('.') == 0:
#         print(" %s seconds" % (round((time.time() - start_time), 4)))
#         break
#     print(" %s seconds" % round((time.time() - start_time),4))
#
# print(board.get_board())
# if board.score < 0:
#     print("%s won the game" % board.min_player)
# else:
#     print("Match drawn")
#
# print(board.latest_change)












# def utility(s, p):
#     # if s.max_player == p:
#     #     return s
#     # s.score = -s.score
#     return s



# def result(s, a):
#     global identifier
#     a.id = s.id + [identifier]
#     identifier += 1
#     return a


# def minimax_decision(state):
#     max_node = state
#     for a in actions(state):
#         max_node = max(max_node, min_value(result(state, a)))
#     return max_node
#
#
# def max_value(state):
#     if terminal_test(state):
#         return utility(state, Board.origin_max_player)
#     v = -float("inf")
#     for a in actions(state):
#         v = max(v, min_value(result(state, a)))
#     return v
#
#
# def min_value(state):
#     if terminal_test(state):
#         return utility(state, Board.origin_max_player)
#     v = float("inf")
#     for a in actions(state):
#         v = min(v, max_value(result(state, a)))
#     return v

# set_players(board)
# s0 = Board.new_board(board, Board.origin_max_player, Board.origin_min_player)

# next_move = minimax_decision(s0)

# print(next_move.get_board())
# print(next_move.id)
