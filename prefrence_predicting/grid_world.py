import numpy as np
import json

class GridWorldEnv:
    def __init__(self,board_name):
        board_fp = "../assets/boards/" + board_name + "_board.json"
        reward_fp = "../assets/boards/" + board_name + "_rewards_function.json"
        #2021-07-29_sparseboard2-notrap_board.json
        with open(board_fp, 'r') as j:
            self.board = json.loads(j.read())

        with open(reward_fp, 'r') as j:
            self.reward_function = json.loads(j.read())
        self.observation_space = len(self.board)*len(self.board[0])
        self.action_space = 4

        self.reward_array = np.zeros(self.observation_space)
        actions = [[-1,0],[1,0],[0,-1],[0,1]]

        for x in range(len(self.board)):
            for y in range(len(self.board[0])):
                N = x + len(self.board[0])*y
                for action_index in range (len(actions)):
                    a = actions[action_index]
                    if self.is_valid_move(x,y,[-1*a[0], -1*a[1]]):
                        self.reward_array[N] = self.reward_function[x-a[0]][y-a[1]][action_index]
                        break

    def set_start_state(self,ss):
        self.ss = ss
        self.pos = ss

    def reset(self):
        self.pos = self.ss
        x,y = self.pos
        N = x + len(self.board[0])*y
        return N

    def state2tab(self,x,y):
        N = x + len(self.board[0])*y
        ones = np.zeros(self.observation_space)
        ones[N] = 1
        return ones

    def is_valid_move(self,x,y,a):
        if (x + a[0] >= 0 and x + a[0] < len(self.board) and y + a[1] >= 0 and y + a[1] < len(self.board)) and self.board[x + a[0]][y + a[1]] != 2 and self.board[x + a[0]][y + a[1]] != 8:
            return True
        else:
            return False

    def get_next_state(self,s,a_index):

        x,y = s
        done = False
        actions = [[-1,0],[1,0],[0,-1],[0,1]]
        a = actions[a_index]

        if self.board[x][y] == 3 or self.board[x][y] == 1 or self.board[x][y] == 7 or self.board[x][y] == 9:
            done = True

        reward = self.reward_function[x][y][a_index]

        if self.is_valid_move(x,y,a):
            x = x + a[0]
            y = y + a[1]
        next_state = (x,y)

        return next_state, reward, done, None

    def step(self,a_index):
        if self.pos == None:
            print ("MUST SET START STATE FIRST")

        x,y = self.pos
        
        if self.board[x][y] == 3 or self.board[x][y] == 1 or self.board[x][y] == 7 or self.board[x][y] == 9:
            done = True

        reward = self.reward_function[x][y][a_index]

        done = False
        actions = [[-1,0],[1,0],[0,-1],[0,1]]
        a = actions[a_index]
        if self.is_valid_move(x,y,a):
            x = x + a[0]
            y = y + a[1]


        self.pos = (x,y)
        assert a_index == self.find_action_index(a)


        # if np.abs(reward) == 50:
        #     done = True
        #To retrieve tile coordinates from number:
        # Col = N % Width
        # Row = N // Width
        N = x + len(self.board[0])*y
        return N, reward, done, None


    def find_action_index(self, action):
        actions = [[-1,0],[1,0],[0,-1],[0,1]]
        i = 0
        for a in actions:
            if a[0] == action[0] and a[1] == action[1]:
                return i
            i+=1
        return False
