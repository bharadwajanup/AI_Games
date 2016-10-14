# Simple tetris program! v0.2
# D. Crandall, Sept 2016

from AnimatedTetris import *
from SimpleTetris import *
from kbinput import *
import time, sys, Queue

class HumanPlayer:
    def get_moves(self, tetris):
        print "Type a sequence of moves using: \n  b for move left \n  m for move right \n  n for rotation\nThen press enter. E.g.: bbbnn\n"
        moves = raw_input()
        return moves

    def control_game(self, tetris):
        while 1:
            c = get_char_keyboard()
            commands =  { "b": tetris.left, "n": tetris.rotate, "m": tetris.right, " ": tetris.down }
            commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
    # This function should generate a series of commands to move the piece into the "optimal"
    # position. The commands are a string of letters, where b and m represent left and right, respectively,
    # and n rotates. tetris is an object that lets you inspect the board, e.g.:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    def get_moves(self, tetris):
        # super simple current algorithm: just randomly move left, right, and rotate a few times
        return random.choice("mnb") * random.randint(1, 10)

    # This is the version that's used by the animted version. This is really similar to get_moves,
    # except that it runs as a separate thread and you should access various methods and data in
    # the "tetris" object to control the movement. In particular:
    #   - tetris.col, tetris.row have the current column and row of the upper-left corner of the 
    #     falling piece
    #   - tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
    #   - tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
    #     issue game commands
    #   - tetris.get_board() returns the current state of the board, as a list of strings.
    #
    def control_game(self, tetris):
        # another super simple algorithm: just move piece to the least-full column
        while 1:
            # time.sleep(0.1)

            board = tetris.get_board()
            piece_info = tetris.get_piece()
            piece = piece_info[0]
            current_row = piece_info[1]
            current_col = piece_info[2]

            column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [len(board),] ) for c in range(0, len(board[0]) ) ]
            index = column_heights.index(max(column_heights))

            fringe = self.all_new_board(board, piece)
            info = fringe.get()
            new_col = info[3]
            self.new_col = new_col
            rotation = info[4]


            for rotate in range(rotation/90):
                tetris.rotate()

            if new_col > current_col:
                for i in range(new_col - current_col):
                    tetris.right()
            elif new_col < current_col:
                for i in range(current_col - new_col):
                    tetris.left()
            else:
                tetris.down()

            # if(index < tetris.col):
            #     tetris.left()
            # elif(index > tetris.col):
            #     tetris.right()
            # else:
            #     tetris.down()


    # For the given new board, compute the quality of this board
    def evaluation(self, board, landing_col):
        landing_height = 0
        for row in range(len(board)):
            if board[row][landing_col] == 'x':
                landing_height = len(board) - row
        rows_elimated = 0
        rows_spot_change = 0
        for row in range(len(board)):
            if board[row] == 'x'*len(board[0]):
                rows_elimated += 1
            for col in range(len(board[0])):
                if col == 0:
                    if board[row][col] == ' ':
                        rows_spot_change += 1
                    if board[row][col] != board[row][col+1]:
                        rows_spot_change += 1
                elif col == len(board[0])-1:
                    if board[row][col] == ' ':
                        rows_spot_change += 1
                elif board[row][col] != board[row][col+1]:
                    rows_spot_change += 1

        col_spot_change = 0
        for col in range(len(board[0])):
            for row in range(len(board)):
                if row == 0:
                    if board[row][col] == 'x':
                        col_spot_change += 1
                    if board[row][col] != board[row+1][col]:
                        col_spot_change += 1
                elif row == len(board) - 1:
                    if board[row][col] == '':
                        col_spot_change += 1
                elif board[row][col] != board[row+1][col]:
                    col_spot_change += 1

        num_holes = 0
        for col in range(len(board[0])):
            for row in range(len(board) - 1):
                if board[row][col] == 'x':
                    for i in range(row+1, len(board)):
                        if board[i][col] == ' ':
                            num_holes += 1
                    break

        num_wells = 0
        for col in range(len(board[0])):
            well_depth = 0
            for row in range(len(board)):
                if self.is_well(board, row, col):
                    well_depth += 1
                else:
                    if well_depth > 0:
                        num_wells += sum(range(well_depth+1))
                        well_depth = 0

        # return -(-45*landing_height + 34*rows_elimated - 32*rows_spot_change - 93*col_spot_change - 79*num_holes -34*num_wells)
        return -(-4*landing_height + 3*rows_elimated - 4*rows_spot_change - 1*col_spot_change - 5*num_holes -3*num_wells)

    def is_well(self, board, row, col):
        if board[row][col] == ' ':
            return False
        elif col == 0:
            if board[row][1] == 'x':
                return True
        elif col == len(board[0])-1:
            if board[row][col-1] == 'x':
                return True
        elif board[row][col-1] == 'x' and board[row][col+1] == 'x':
            return True
        else:
            return False

    # Return a list of all possible new boards
    # Use TetrisGame.place_piece((board, scoer), piece, row, col)
    def all_new_board(self, board, piece):
        container = Queue.PriorityQueue()
        for rotation in range(0, 360, 90):
            new_piece = tetris.rotate_piece(piece, rotation)
            width = len(new_piece[0])
            for col in range(len(board[0]) - width + 1):
                for row in range(len(board)):
                    if TetrisGame.check_collision((board, 0), new_piece, row, col):
                        new_board = TetrisGame.place_piece((board, 0), new_piece, row-1, col)[0]
                        container.put((self.evaluation(new_board, col), new_board, row, col, rotation))
                        break
        return container


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
    if player_opt == "human":
        player = HumanPlayer()
    elif player_opt == "computer":
        player = ComputerPlayer()
    else:
        print "unknown player!"

    if interface_opt == "simple":
        tetris = SimpleTetris()
    elif interface_opt == "animated":
        tetris = AnimatedTetris()
    else:
        print "unknown interface!"

    tetris.start_game(player)

except EndOfGame as s:
    print "\n\n\n", s



