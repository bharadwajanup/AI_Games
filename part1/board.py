class Board:
    N = 0
    K = 0
    max_player = ""
    min_player = ""

    def __init__(self, state,latest_change = None):
        self.state = state
        self.score = self.get_score(latest_change)

    def __len__(self):
        return len(self.state)

    def get_score(self,change_index):
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
        # s = 0
        # e = int(self.N)
        # for i in range(1,int(self.N)+1):
        #     print(self.state[s:e])
        #     s = e
        #     e = int(self.N) * (i+1)
        return self.state

    @classmethod
    def new_board(cls, state, i):
        new_state = state[:i] + cls.max_player + state[i+1:]

        return cls(new_state, i)

    def get_value(self, r, c):
        index = int(r * int(self.N) + c)
        return self.state[index]

    def get_score_for_pos(self, i):
        board = self.state
        val = board[i]
        initial_score = 100
        if val == '.' or val == self.min_player:
            return 0
        if self.eval(i, self.max_player) == int(self.K):
            return -100
        if self.eval(i, self.min_player) > (0 if self.state[i] != self.min_player else 1):
            initial_score -= 20
        if self.eval(i, self.max_player) > (0 if self.state[i] != self.max_player else 1):
            initial_score -= 40
        return initial_score



    def eval(self, i,player):
        r, c = self.get_row_col(i)
        row_col = self.check_row_col(r, c,player)
        diag = self.check_diagonal(r, c,player)
        #print("%d,%d" %(row_col,diag))
        return max(row_col,diag )

    def get_row_col(self, i):
        c = int(i) % int(int(self.N))
        r = (i - c) / int(int(self.N))
        return r, c

    def check_row_col(self,r,c,player):
        start = self.get_limit(r, 'U')
        end = self.get_limit(r,'L')
        row_string = self.get_comparator_string(start,end,r,"R")

        start = self.get_limit(c,'U')
        end = self.get_limit(c,'L')
        col_string = self.get_comparator_string(start,end,c,"C")

        return self.find_max_pattern(row_string,col_string,player)

    def find_max_pattern(self,str1,str2,player):
        # check_str = player * int(self.K)
        # kay = int(self.K)
        #
        # while kay > 0:
        #     if str1.count(check_str[:kay]) > 0 or str2.count(check_str[:kay]) > 0:
        #         return kay
        #     kay -= 1
        # return kay
        # onecount = 0
        # for i in range(0,len(str1)):
        #     if str1[i] == player:
        #         onecount += 1
        #     if str1[i] != player and str1[i] != '.':
        #         onecount = 0
        #         break
        # twocount = 0
        # for i in range(0, len(str2)):
        #     if str2[i] == player:
        #         twocount += 1
        #     if str2[i] != player and str2[i] != '.':
        #         twocount = 0
        #         break

        return max(str1.count(player),str2.count(player))

    def check_diagonal(self,r,c,player):
        diagonal_24 = self.get_diagonal_comparator_string(r,c,'LR')
        diagonal_13 = self.get_diagonal_comparator_string(r,c,'RL')
        return self.find_max_pattern(diagonal_13,diagonal_24,player)

    def get_diagonal_comparator_string(self,r,c,type):
        row = r
        col = c
        counter = 0
        str = ""
        if type == 'LR':
            while row >= 0 and col >= 0 and counter < int(self.K):
                str = self.get_value(row, col) + str
                counter += 1
                row -= 1
                col -= 1
            row = r+1
            col = c+1
            counter = 0
            while row < int(self.N) and col < int(self.N) and counter < int(self.K):
                str += self.get_value(row,col)
                counter +=1
                row += 1
                col +=1
        else:
            while row >= 0 and col < int(self.N) and counter < int(self.K):
                str = self.get_value(row, col) + str
                counter += 1
                row -= 1
                col += 1
            row = r+1
            col = c-1
            counter = 0
            while row < int(self.N) and col >= 0 and counter < int(self.K):
                str += self.get_value(row, col)
                counter += 1
                row += 1
                col -= 1
        return str


    def get_comparator_string(self,start,end,val,type):
        str = ""
        if type == "R":
            while start <= end:
                str += self.get_value(val,start)
                start += 1
            return str;
        else:
            while start <= end:
                str += self.get_value(start,val)
                start += 1
            return str;

    def get_limit(self,val,type):
        if type == "U":
            res = val - int(self.K) - 1
            return  0 if res < 0 else res
        else:
            res = val + int(self.K) + 1
            return int(self.N)-1 if res >= int(self.N) else res

    def row_col_test(self, r, c,player):
        temp = c
        max_col_count = 0
        counter = 0
        step_counter = 0
        while temp < int(self.N):
            if self.get_value(r,temp) == player:
                counter += 1
            if step_counter == int(self.K):
                break
            step_counter += 1
            temp += 1
        max_col_count = max(max_col_count,counter)

        temp = c
        counter = 0
        step_counter = 0
        while temp >= 0:
            if self.get_value(r,temp) == player:
                counter += 1
            if step_counter == int(self.K):
                break
            step_counter += 1
            temp -= 1
        max_col_count = max(max_col_count, counter)

        if max_col_count == int(self.K):
            return max_col_count

        max_row_count = 0
        temp = r
        counter = 0
        step_counter = 0
        while temp >= 0:

            if self.get_value(temp,c) == player:
                counter += 1
            if step_counter == int(self.K):
                break
            step_counter += 1
            temp -= 1

        max_row_count = max(max_row_count,counter)

        if max_row_count == int(self.K):
            return max_row_count

        temp = r
        counter = 0
        step_counter = 0
        while temp < int(self.N):

            if self.get_value(temp,c) == player:
                counter += 1
            if step_counter == int(self.K):
                break
            step_counter += 1
            temp += 1

        max_row_count = max(max_row_count,counter)
        return max(max_row_count, max_col_count)

    def diagonal_test(self, row,col,player):
        temp_row = row
        temp_col = col
        counter = 0
        self_counter = 0
        max_counter = counter
        N = int(self.N)
        # quad 1
        while temp_row < N and temp_col < N:

            if self.get_value(temp_row,temp_col) == player:
                counter += 1

            if counter == int(self.K):
                return counter
            if self_counter == int(self.K):
                break
            self_counter += 1
            temp_row += 1
            temp_col += 1
        max_counter = max(max_counter,counter)
        temp_row = row
        temp_col = col
        counter = 0
        self_counter = 0

        # quad 2
        while temp_row >= 0 and temp_col < N:
            if self.get_value(temp_row,temp_col) == player:
                counter += 1
            if counter == int(self.K):
                return counter
            if self_counter == int(self.K):
                break
            self_counter += 1
            temp_row -= 1
            temp_col += 1

        max_counter = max(max_counter, counter)
        temp_row = row
        temp_col = col
        counter = 0
        self_counter = 0
        # quad 3
        while temp_row >= 0 and temp_col >= 0:
            if self.get_value(temp_row,temp_col) == player:
                counter += 1
            if counter == int(self.K):
                return counter
            if self_counter == int(self.K):
                break
            self_counter += 1
            temp_row -= 1
            temp_col -= 1

        max_counter = max(max_counter, counter)
        temp_row = row
        temp_col = col
        counter = 0
        self_counter = 0

        # quad 4
        while temp_row < N and temp_col >= 0:
            if self.get_value(temp_row,temp_col) == player:
                counter += 1
            if counter == int(self.K):
                return counter
            if self_counter == int(self.K):
                break
            self_counter += 1
            temp_row += 1
            temp_col -= 1

        max_counter = max(max_counter, counter)

        return max_counter





