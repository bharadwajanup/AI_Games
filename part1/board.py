class Board:
    N = 0
    K = 0
    origin_max_player = ""
    origin_min_player = ""
    distance_cache = {}
    min_distance_cache = {}

    def __init__(self, state, maxp, minp, latest_change):
        self.state = state
        self.latest_change = latest_change
        self.max_player = maxp
        self.min_player = minp
        self.score = -200 if latest_change is None else self.get_score(latest_change)
        self.id = []

    def __len__(self):
        return len(self.state)

    # Calculate the score for the current state
    def get_score(self, change_index):
        score = 0
        if change_index is not None:
            return self.get_score_for_pos(change_index)
        return score

    # Conflict resolution while inserting objects into a heap or a priority queue
    def __eq__(self, other):
        if isinstance(other, Board):
            return -self.score == -other.score
        return -self.score == -other

    # Conflict resolution while inserting objects into a heap or a priority queue
    def __lt__(self, other):
        if isinstance(other, Board):
            return -int(self.score) < -int(other.score)
        return -int(self.score) < -other

    # Conflict resolution while inserting objects into a heap or a priority queue
    def __gt__(self, other):
        if isinstance(other, Board):
            return -int(self.score) > -int(other.score)
        return -int(self.score) > -other

    # Return the string representation of the board.
    def __str__(self):
        return self.state  # + " "+str(self.score)

    # Returns the human readable format of the board.
    def get_board(self):
        string = "\n"
        s = 0
        e = int(self.N)
        for i in range(1, int(self.N) + 1):
            # print(self.state[s:e])
            string += "\t".join(self.state[s:e]) + "\n"
            s = e
            e = int(self.N) * (i + 1)
        return string.replace('.', '-')

    # Gets a new instance of this class after adding the piece at the desired position.
    @classmethod
    def new_board(cls, state, max_player, min_player, i=None):
        new_state = state if i is None else state[:i] + max_player + state[i + 1:]

        return cls(new_state, max_player, min_player, i)

    # get the value at a particular row and column
    def get_value(self, r, c):
        index = self.get_index(r, c)
        return self.state[index]

    # Covert into 1d array index
    def get_index(self, r, c):
        return int(r * int(self.N) + c)

    # Calculates how good placing a piece at this position can be.
    def get_score_for_pos(self, i):
        board = self.state
        val = board[i]
        initial_score = self.K * 10
        if val == '.' or val == self.min_player:
            return 0
        coverage_list = self.get_coverage_list(i)
        min_distance_for_max = self.find_max_pattern(coverage_list, self.max_player)
        # Temporarily change the piece to observe the effect on min player
        self.state = self.state[:i] + self.min_player + self.state[i+1:]
        coverage_list_min = self.get_coverage_list(i)
        # Switch it back to how it was.
        self.state = self.state[:i] + self.max_player + self.state[i + 1:]
        min_distance_for_min = self.find_max_pattern(coverage_list_min, self.min_player)
        close_coeff_max = self.K - min_distance_for_max
        close_coeff_min = self.K - min_distance_for_min

        # The game is lost. Return the least possible score
        if min_distance_for_max == 0:
            return -initial_score

        # Assign penalties.
        initial_score -= 5 * close_coeff_min
        initial_score -= 10 * close_coeff_max if close_coeff_max > 1 else 0

        return initial_score

    # gets the string along k spots along the row, column and diagonal.
    def get_coverage_list(self, i):
        r, c = self.get_row_col(i)
        row_col = self.get_row_col_elements(r, c)
        diagonals = self.get_diagonal_elements(r, c)
        return row_col + diagonals

    # Convert 1d array index to a 2d index
    def get_row_col(self, i):
        if i is None:
            return None
        c = int(i) % int(int(self.N))
        r = (i - c) / int(int(self.N))
        return r, c

    # Get row and col string
    def get_row_col_elements(self, r, c):
        start = self.get_limit(c, 'U')
        end = self.get_limit(c, 'L')
        row_string = self.state[self.get_index(r, start):self.get_index(r,
                                                                        end) + 1]  # self.get_comparator_string(start, end, r, "R")

        start = self.get_limit(r, 'U')
        end = self.get_limit(r, 'L')
        col_string = self.get_comparator_string(start, end, c, "C")

        return [row_string, col_string]

    # Finds the least distance from the losing combination for the given coverage list for the player.
    def find_max_pattern(self, lst, player):
        min_len = self.K + 1
        for string in lst:
            count = self.find_min_distance(string, player)
            min_len = min(min_len, count)
        return min_len

    # Returns the elements along the diagonal.
    def get_diagonal_elements(self, r, c):
        diagonal_24 = self.get_diagonal_comparator_string(r, c, 'LR')
        diagonal_13 = self.get_diagonal_comparator_string(r, c, 'RL')
        return [diagonal_24, diagonal_13]

    # Helper to get diagonal elements
    def get_diagonal_comparator_string(self, r, c, diag_type):
        row = r
        col = c
        counter = 0
        diag_str = ""
        if diag_type == 'LR':
            while row >= 0 and col >= 0 and counter < int(self.K):
                diag_str = self.get_value(row, col) + diag_str
                counter += 1
                row -= 1
                col -= 1
            row = r + 1
            col = c + 1
            counter = 0
            while row < int(self.N) and col < int(self.N) and counter < int(self.K):
                diag_str += self.get_value(row, col)
                counter += 1
                row += 1
                col += 1
        else:
            while row >= 0 and col < int(self.N) and counter < int(self.K):
                diag_str = self.get_value(row, col) + diag_str
                counter += 1
                row -= 1
                col += 1
            row = r + 1
            col = c - 1
            counter = 1
            while row < int(self.N) and col >= 0 and counter < int(self.K):
                diag_str += self.get_value(row, col)
                counter += 1
                row += 1
                col -= 1
        return diag_str

    # Finds and returns the elements along the row or column
    def get_comparator_string(self, start, end, val, type):
        str = ""
        if type == "R":
            while start <= end:
                str += self.get_value(val, start)
                start += 1
            return str
        else:
            while start <= end:
                str += self.get_value(start, val)
                start += 1
            return str

    # Get the boundaries of the board adjusted to 'k' positions.
    def get_limit(self, val, type):
        if type == "U":
            res = val - int(self.K) - 1
            return 0 if res < 0 else res
        else:
            res = val + int(self.K) - 1
            return int(self.N) - 1 if res >= int(self.N) else res

    # Finds the min distance to lose
    def find_min_distance(self, str1, player):
        key = str1+"|"+player
        if key not in self.min_distance_cache:
            str_len = len(str1)
            i = 0
            k = int(self.K)
            min_val = k + 1
            losing_string = player * k
            while k + i <= str_len:
                sub_str = str1[i:(k + i)]
                distance = k if sub_str.strip(player + '.') else self.find_distance(sub_str, losing_string)
                min_val = min(min_val, distance)
                i += 1
            self.min_distance_cache[key] = min_val

        return self.min_distance_cache[key]

    # Calculates how many positions are different from the losing combination
    def find_distance(self, str1, str2):
        if len(str1) != len(str2):
            print("Length of two strings not the same. Debug")
        if str1 not in self.distance_cache:
            c = 0
            for i in range(0, len(str1)):
                if str1[i] != str2[i]:
                    c += 1
            self.distance_cache[str1] = c
        return self.distance_cache[str1]
