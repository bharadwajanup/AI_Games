from sys import argv as argv
import heapq
try:
    from part1.board import Board as Board
except ImportError:
    from board import Board as Board

if len(argv) != 5:
    print("Arguments not valid")
    exit(1)

n = argv[1]
k = argv[2]
board = argv[3]  # TODO: Check if the board is valid.
time = argv[4]  # TODO: Work on implementing time

Board.N = n
Board.K = k



def get_index(r, c):
    return r*n+c


def player(s):
    return ['b', 'w'] if s.count('w') > s.count('b') else ['w', 'b']


def set_players(board):
    players = player(board)
    max_player = players[0]
    min_player = players[1]

    Board.max_player = max_player
    Board.min_player = min_player

def add_piece(board,i):
    if board[i] != ".":
        return False
    return Board.new_board(board, i)


def get_next_move(board):
    successors = []
    for i in range(0, len(board)):
        potential_next_move = add_piece(board,i)

        if potential_next_move and potential_next_move.score == 100:
            print(str(potential_next_move) + " Score %d" % potential_next_move.score)
            return potential_next_move
        elif potential_next_move:
            print(str(potential_next_move) + " Score %d" % potential_next_move.score)
            heapq.heappush(successors, potential_next_move)
    return heapq.heappop(successors)

while True:
    set_players(str(board))
    board = get_next_move(str(board))
    print("Next Move = " + str(board))

    if board.score < 0:
        print("%s won the game" %Board.min_player)
        break
    if str(board).count('.') == 0 and board.score > 0:
        print("Match Drawn")
        break




