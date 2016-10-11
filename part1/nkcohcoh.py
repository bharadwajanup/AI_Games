from sys import argv as argv
import heapq

try:
    from part1.board import Board as Board
except ImportError:
    from board import Board as Board

if len(argv) != 5:
    print("Arguments not valid")
    exit(1)

n = int(argv[1])
k = int(argv[2])

if k > n:
    print("Invalid K value")
    exit(1)


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
time = int(argv[4])  # TODO: Work on implementing time

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
    print("It's %s's turn" % max_player)
    Board.max_player = max_player
    Board.min_player = min_player


def add_piece(board, i):
    if board[i] != ".":
        return False
    return Board.new_board(board, i)


def get_next_move(board):
    successors = []
    for i in range(0, len(board)):
        potential_next_move = add_piece(board, i)

        if potential_next_move and potential_next_move.score == 100:
            # print(str(potential_next_move) + " Score %d" % potential_next_move.score)
            return potential_next_move
        elif potential_next_move:
            # print(str(potential_next_move) + " Score %d" % potential_next_move.score)
            heapq.heappush(successors, potential_next_move)
    return heapq.heappop(successors)


while True:
    set_players(str(board))
    board = get_next_move(str(board))
    print("Next Move = " + board.get_board())
    print("Score = %d" % board.score)

    if board.score < 0:
        print("%s won the game" % Board.min_player)
        break
    if str(board).count('.') == 0 and board.score > 0:
        print("Match Drawn")
        break
