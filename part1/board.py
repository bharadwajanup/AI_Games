import itertools
class Board:
    N = 0
    K = 0
    max_player = ""
    min_player = ""

    def __init__(self, state, latest_change=None):
        self.state = state
        self.latest_change = latest_change
        self.score = self.get_score(latest_change)

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
        return -self.score == -other.score

    def __lt__(self, other):
        return -int(self.score) < -int(other.score)

    def __str__(self):
        return self.state

    def get_board(self):
        string = "\n"
        s = 0
        e = int(self.N)
        for i in range(1, int(self.N) + 1):
            #print(self.state[s:e])
            string += self.state[s:e] + "\n"
            s = e
            e = int(self.N) * (i + 1)
        return string

    @classmethod
    def new_board(cls, state, i):
        new_state = state[:i] + cls.max_player + state[i + 1:]

        return cls(new_state, i)

    def get_value(self, r, c):
        index = self.get_index(r,c)
        return self.state[index]

    def get_index(self,r,c):
        return int(r * int(self.N) + c)

    def get_score_for_pos(self, i):
        board = self.state
        val = board[i]
        initial_score = 100
        if val == '.' or val == self.min_player:
            return 0
        if self.eval(i, self.max_player) >= int(self.K):
            return -100
        if self.eval(i, self.min_player) > (0 if self.state[i] != self.min_player else 1):
            initial_score -= 20
        if self.eval(i, self.max_player) > (0 if self.state[i] != self.max_player else 1):
            initial_score -= 40
        return initial_score

    def eval(self, i, player):
        r, c = self.get_row_col(i)
        row_col = self.check_row_col(r,c,player)#self.check_row_col(i, player)
        diag = self.check_diagonal(r, c, player)
        # print("%d,%d" %(row_col,diag))
        return max(row_col, diag)

    def get_row_col(self, i):
        c = int(i) % int(int(self.N))
        r = (i - c) / int(int(self.N))
        return r, c

    def check_row_col(self, r, c, player):
        start = self.get_limit(c, 'U')
        end = self.get_limit(c, 'L')
        row_string = self.state[self.get_index(r, start):self.get_index(r, end)+1]#self.get_comparator_string(start, end, r, "R")

        start = self.get_limit(r, 'U')
        end = self.get_limit(r, 'L')
        col_string = self.get_comparator_string(start, end, c, "C")

        return self.find_max_pattern(row_string, col_string, player)

    def find_max_pattern(self, str1, str2, player):
        str1_count = self.find_max_continuous_player(str1, player)
        str2_count = self.find_max_continuous_player(str2, player)
        return max(str1_count, str2_count)

    def check_diagonal(self, r, c, player):
        diagonal_24 = self.get_diagonal_comparator_string(r, c, 'LR')
        diagonal_13 = self.get_diagonal_comparator_string(r, c, 'RL')
        return self.find_max_pattern(diagonal_13, diagonal_24, player)

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
            return str;
        else:
            while start <= end:
                str += self.get_value(start, val)
                start += 1
            return str;

    def get_limit(self, val, type):
        if type == "U":
            res = val - int(self.K) - 1
            return 0 if res < 0 else res
        else:
            res = val + int(self.K) - 1
            return int(self.N) - 1 if res >= int(self.N) else res

    def find_max_continuous_player(self, str1, player):
        str_len = len(str1)
        i = 0
        k = int(self.K)
        max_val = 0
        while k + i <= str_len:
            sub_str = str1[i:(k + i)]
            grp_plyr_lst = [len(list(g)) if k == player else 0 for k, g in itertools.groupby(sub_str)]
            max_val = max(max_val, max(grp_plyr_lst))
            i += 1
        return max_val

    # def row_col_test(self, r, c, player):
    #     temp = c
    #     max_col_count = 0
    #     counter = 0
    #     step_counter = 0
    #     while temp < int(self.N):
    #         if self.get_value(r, temp) == player:
    #             counter += 1
    #         if step_counter == int(self.K):
    #             break
    #         step_counter += 1
    #         temp += 1
    #     max_col_count = max(max_col_count, counter)
    #
    #     temp = c
    #     counter = 0
    #     step_counter = 0
    #     while temp >= 0:
    #         if self.get_value(r, temp) == player:
    #             counter += 1
    #         if step_counter == int(self.K):
    #             break
    #         step_counter += 1
    #         temp -= 1
    #     max_col_count = max(max_col_count, counter)
    #
    #     if max_col_count == int(self.K):
    #         return max_col_count
    #
    #     max_row_count = 0
    #     temp = r
    #     counter = 0
    #     step_counter = 0
    #     while temp >= 0:
    #
    #         if self.get_value(temp, c) == player:
    #             counter += 1
    #         if step_counter == int(self.K):
    #             break
    #         step_counter += 1
    #         temp -= 1
    #
    #     max_row_count = max(max_row_count, counter)
    #
    #     if max_row_count == int(self.K):
    #         return max_row_count
    #
    #     temp = r
    #     counter = 0
    #     step_counter = 0
    #     while temp < int(self.N):
    #
    #         if self.get_value(temp, c) == player:
    #             counter += 1
    #         if step_counter == int(self.K):
    #             break
    #         step_counter += 1
    #         temp += 1
    #
    #     max_row_count = max(max_row_count, counter)
    #     return max(max_row_count, max_col_count)
    #
    # def diagonal_test(self, row, col, player):
    #     temp_row = row
    #     temp_col = col
    #     counter = 0
    #     self_counter = 0
    #     max_counter = counter
    #     N = int(self.N)
    #     # quad 1
    #     while temp_row < N and temp_col < N:
    #
    #         if self.get_value(temp_row, temp_col) == player:
    #             counter += 1
    #
    #         if counter == int(self.K):
    #             return counter
    #         if self_counter == int(self.K):
    #             break
    #         self_counter += 1
    #         temp_row += 1
    #         temp_col += 1
    #     max_counter = max(max_counter, counter)
    #     temp_row = row
    #     temp_col = col
    #     counter = 0
    #     self_counter = 0
    #
    #     # quad 2
    #     while temp_row >= 0 and temp_col < N:
    #         if self.get_value(temp_row, temp_col) == player:
    #             counter += 1
    #         if counter == int(self.K):
    #             return counter
    #         if self_counter == int(self.K):
    #             break
    #         self_counter += 1
    #         temp_row -= 1
    #         temp_col += 1
    #
    #     max_counter = max(max_counter, counter)
    #     temp_row = row
    #     temp_col = col
    #     counter = 0
    #     self_counter = 0
    #     # quad 3
    #     while temp_row >= 0 and temp_col >= 0:
    #         if self.get_value(temp_row, temp_col) == player:
    #             counter += 1
    #         if counter == int(self.K):
    #             return counter
    #         if self_counter == int(self.K):
    #             break
    #         self_counter += 1
    #         temp_row -= 1
    #         temp_col -= 1
    #
    #     max_counter = max(max_counter, counter)
    #     temp_row = row
    #     temp_col = col
    #     counter = 0
    #     self_counter = 0
    #
    #     # quad 4
    #     while temp_row < N and temp_col >= 0:
    #         if self.get_value(temp_row, temp_col) == player:
    #             counter += 1
    #         if counter == int(self.K):
    #             return counter
    #         if self_counter == int(self.K):
    #             break
    #         self_counter += 1
    #         temp_row += 1
    #         temp_col -= 1
    #
    #     max_counter = max(max_counter, counter)
    #
    #     return max_counter




