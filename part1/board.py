import itertools


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

    def get_score(self, change_index):
        score = 0
        if change_index is not None:
            return self.get_score_for_pos(change_index)
        return score
        # for i in range(0, len(self.state)):
        #     score += self.get_score_for_pos(i)
        # return score

    def __eq__(self, other):
        if isinstance(other, Board):
            return -self.score == -other.score
        return -self.score == -other

    def __lt__(self, other):
        if isinstance(other, Board):
            return -int(self.score) < -int(other.score)
        return -int(self.score) < -other

    def __gt__(self, other):
        if isinstance(other, Board):
            return -int(self.score) > -int(other.score)
        return -int(self.score) > -other

    def __str__(self):
        return self.state  # + " "+str(self.score)

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

    @classmethod
    def new_board(cls, state, max_player, min_player, i=None):
        new_state = state if i is None else state[:i] + max_player + state[i + 1:]

        return cls(new_state, max_player, min_player, i)

    def get_value(self, r, c):
        index = self.get_index(r, c)
        return self.state[index]

    def get_index(self, r, c):
        return int(r * int(self.N) + c)

    # def get_score_for_pos(self, i):
    #     board = self.state
    #     val = board[i]
    #     initial_score = 100
    #     if val == '.' or val == self.min_player:
    #         return 0
    #     coverage_list = self.get_coverage_list(i)
    #     min_distance = self.find_max_pattern(coverage_list, self.max_player)
    #     if min_distance == 0:
    #         return -100
    #     if self.is_obstructing_opponent(coverage_list, self.min_player):
    #         initial_score -= 20
    #     if min_distance != self.K-1:  # (0 if self.state[i] != self.max_player else 1):
    #         initial_score -= 40
    #     return initial_score

    def get_score_for_pos(self, i):
        board = self.state
        val = board[i]
        initial_score = self.K * 10
        if val == '.' or val == self.min_player:
            return 0
        coverage_list = self.get_coverage_list(i)
        min_distance_for_max = self.find_max_pattern(coverage_list, self.max_player)
        self.state = self.state[:i] + self.min_player + self.state[i+1:]
        coverage_list_min = self.get_coverage_list(i);
        self.state = self.state[:i] + self.max_player + self.state[i + 1:]
        min_distance_for_min = self.find_max_pattern(coverage_list_min, self.min_player)
        close_coeff_max = self.K - min_distance_for_max
        close_coeff_min = self.K - min_distance_for_min
        if min_distance_for_max == 0:
            return -initial_score

        initial_score -= 5 * close_coeff_min
        initial_score -= 10 * close_coeff_max if close_coeff_max > 1 else 0

        return initial_score

    def get_coverage_list(self, i):
        r, c = self.get_row_col(i)
        row_col = self.get_row_col_elements(r, c)
        diagonals = self.get_diagonal_elements(r, c)
        return row_col + diagonals

    def get_row_col(self, i):
        if i is None:
            return None
        c = int(i) % int(int(self.N))
        r = (i - c) / int(int(self.N))
        return r, c

    def get_row_col_elements(self, r, c):
        start = self.get_limit(c, 'U')
        end = self.get_limit(c, 'L')
        row_string = self.state[self.get_index(r, start):self.get_index(r,
                                                                        end) + 1]  # self.get_comparator_string(start, end, r, "R")

        start = self.get_limit(r, 'U')
        end = self.get_limit(r, 'L')
        col_string = self.get_comparator_string(start, end, c, "C")

        return [row_string, col_string]

    def find_max_pattern(self, lst, player):
        min_len = self.K + 1
        for string in lst:
            count = self.find_min_distance(string, player)
            min_len = min(min_len, count)
        return min_len

    def get_diagonal_elements(self, r, c):
        diagonal_24 = self.get_diagonal_comparator_string(r, c, 'LR')
        diagonal_13 = self.get_diagonal_comparator_string(r, c, 'RL')
        return [diagonal_24, diagonal_13]

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

    def get_limit(self, val, type):
        if type == "U":
            res = val - int(self.K) - 1
            return 0 if res < 0 else res
        else:
            res = val + int(self.K) - 1
            return int(self.N) - 1 if res >= int(self.N) else res

    # def find_max_continuous_player(self, str1, player):
    #     str_len = len(str1)
    #     i = 0
    #     k = int(self.K)
    #     max_val = 0
    #     while k + i <= str_len:
    #         sub_str = str1[i:(k + i)]
    #         grp_plyr_lst = [len(list(g)) if k == player else 0 for k, g in itertools.groupby(sub_str)]
    #         max_val = max(max_val, max(grp_plyr_lst))
    #         i += 1
    #     return max_val

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

    # def is_obstructing_opponent(self, string_lst, player):
    #     for string in string_lst:
    #         if string.count(player) > 0:
    #             return True
    #     return False

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
