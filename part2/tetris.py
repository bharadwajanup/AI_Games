'''
To form a tettis game as a searching problem, we can formulate the successor funtion of a falling piece as to search throught all possbile landing rotations and positions to find out the best landing strtegy.
For a certian piece, there are maximum four rotations and 10 landing positions (if the board lenght is 10). So the search problem is in O(1), which means the computation required for each falling piece is roughtly constant.
So the key chellange we are facing in tetris is to find out a reasonable evaluation funciton (we can also think it as a heuristic funtion) to determine of all the possbile landing stratigies which is the best one. This can be achieved using priority queue.
To create a good evaluation function, the features of each new board need to be carefully examed and choosen. During the process, I borrowed three ideas form the folloing source: http://www.cnblogs.com/youngshall/archive/2009/03/24/1420682.html
There are some features that are easy to come up with: the landing height, the rows eliminated, the number of holds, the smothness of the rows and columns. The first three are easy to understand but the hard part is to find a way to quantify the smothness. I borrowed the idea from the above website to compute the number of transitions for each row and column.
After the initial implementation with the five features above, I found that the program sometimes leave a few empty columns in the middle of the board and resulting a lose. Then I implemented the number of wells into the features which greatly improve the situation. So the final version of the evaluation consits of six features.

-----------
After the implementation, there were few problems with the optimization on the feature weights. First of all, although it seemed easy to come up with the parameters for the feature weights at the glance, it was hard to come up with the systematic way to optimize the weights. Seconldy, although there were constant problems that causes the game to end, such as not filling the well, simply changing the parameters of the num_well or num_holes did not necessarily solve the problem, which made it hard to systemize the optimization. Therefore, with the initial idea that number of holes should be weighed and the wells that led to the loss of the game, I changed the parameters manually with trials. By observing the constant problems that caused the program to end, I changed the weights on that specific feature. Despite the fact that it went harder and harder to find the better parameters as the program scores better since it takes more time until the end of the game, increasing the number of trials allowed the better scores in result.
-----------

'''

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
            rotation = info[4]

            for rotate in range(rotation/90):
                tetris.rotate()

            if new_col > current_col:
                for i in range(new_col - current_col):
                    tetris.right()
                tetris.down()
            elif new_col < current_col:
                for i in range(current_col - new_col):
                    tetris.left()
                tetris.down()
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

        landing_height = 0
        for row in range(len(board)):
            if board[row][landing_col] == 'x':
                landing_height = len(board) - 1 - row - rows_elimated
                break

        col_spot_change = 0
        for col in range(len(board[0])):
            for row in range(len(board)):
                if row == 0:
                    if board[row][col] == 'x':
                        col_spot_change += 1
                    if board[row][col] != board[1][col]:
                        col_spot_change += 1
                elif row == len(board) - 1:
                    if board[row][col] == ' ':
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


        # print(landing_height, rows_elimated*len(board[0]), rows_spot_change,col_spot_change, num_holes, num_wells)

        return -(-4.94*landing_height + 4.141*rows_elimated*len(board[0]) - 3.63*rows_spot_change - 8.17*col_spot_change - 8.56*num_holes - 4.164*num_wells)

    def is_well(self, board, row, col):
        if board[row][col] == ' ':
            if col == 0 and board[row][1] == 'x':
                return True
            elif col == len(board[0])-1 and board[row][col-1] == 'x':
                    return True
            elif board[row][col-1] == 'x' and board[row][col+1] == 'x':
                return True
        return False

    # Return a list of all possible new boards
    # Use TetrisGame.place_piece((board, scoer), piece, row, col)
    def all_new_board(self, board, piece):
        container = Queue.PriorityQueue()

        flag = True
        temp_piece = piece
        while(flag):
            try:
                index = TetrisGame.PIECES.index(temp_piece)
            except ValueError:
                temp_piece = tetris.rotate_piece(temp_piece, 90)
                flag = not flag
            flag = not flag
        rotation_list = [180, 180, 90, 360, 360]

        for rotation in range(0, rotation_list[index], 90):
            new_piece = tetris.rotate_piece(piece, rotation)
            width = len(new_piece[0])
            height = len(new_piece)
            for col in range(len(board[0]) - width + 1):
                for row in range(len(board)-1):
                    if row != 0 and TetrisGame.check_collision((board, 0), new_piece, row, col):
                        try:
                            new_board = TetrisGame.place_piece((board, 0), new_piece, row-1, col)[0]
                        except IndexError:
                            new_board = TetrisGame.place_piece((board, 0), new_piece, row-2, col)[0]
                        container.put((self.evaluation(new_board, col), new_board, row-1, col, rotation))
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



