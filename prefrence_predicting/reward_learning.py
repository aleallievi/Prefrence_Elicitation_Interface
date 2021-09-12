import numpy as np
import torch.nn.functional as F
import torch.nn as nn
import pickle
import re
import matplotlib
import json
import torch
from sklearn.model_selection import train_test_split


with open('/Users/stephanehatgiskessell/Desktop/Kivy_stuff/MTURK_interface/2021_08_18_woi_questions.data', 'rb') as f:
    questions = pickle.load(f)
with open('/Users/stephanehatgiskessell/Desktop/Kivy_stuff/MTURK_interface/2021_08_18_woi_answers.data', 'rb') as f:
    answers = pickle.load(f)

dsdt_data = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/2021_07_29_dsdt_chosen.json"
dsst_data = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/2021_07_29_dsst_chosen.json"
ssst_data = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/2021_07_29_ssst_chosen.json"
sss_data = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/saved_data/2021_07_29_sss_chosen.json"
board = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/boards/2021-07-29_sparseboard2-notrap_board.json"
board_vf = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/boards/2021-07-29_sparseboard2-notrap_value_function.json"
board_rf = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/boards/2021-07-29_sparseboard2-notrap_rewards_function.json"



with open(board_vf, 'r') as j:
    board_vf = json.loads(j.read())
with open(dsdt_data, 'r') as j:
    dsdt_data = json.loads(j.read())
with open(dsst_data, 'r') as j:
    dsst_data = json.loads(j.read())
with open(ssst_data, 'r') as j:
    ssst_data = json.loads(j.read())
with open(sss_data, 'r') as j:
    sss_data = json.loads(j.read())
with open(board, 'r') as j:
    board = json.loads(j.read())
with open(board_rf, 'r') as j:
    board_rf = json.loads(j.read())


def find_action_index(action):
    actions = [[-1,0],[1,0],[0,-1],[0,1]]
    i = 0
    for a in actions:
        if a[0] == action[0] and a[1] == action[1]:
            return i
        i+=1
    return False

def is_in_blocked_area(x,y):
    val = board[x][y]
    if val == 2 or val == 8:
        return True
    else:
        return False

def get_state_feature(x,y):
    reward_feature = np.zeros(6)
    if board[x][y] == 0:
        reward_feature[0] = 1
    elif board[x][y] == 1:
        #flag
        # reward_feature[0] = 1
        reward_feature[1] = 1
    elif board[x][y] == 2:
        #house
        # reward_feature[0] = 1
        pass
    elif board[x][y] == 3:
        #sheep
        # reward_feature[0] = 1
        reward_feature[2] = 1
    elif board[x][y] == 4:
        #coin
        # reward_feature[0] = 1
        reward_feature[0] = 1
        reward_feature[3] = 1
    elif board[x][y] == 5:
        #road block
        # reward_feature[0] = 1
        reward_feature[0] = 1
        reward_feature[4] = 1
    elif board[x][y] == 6:
        #mud area
        # reward_feature[0] = 1
        reward_feature[5] = 1
    elif board[x][y] == 7:
        #mud area + flag
        reward_feature[1] = 1
    elif board[x][y] == 8:
        #mud area + house
        pass
    elif board[x][y] == 9:
        #mud area + sheep
        reward_feature[2] = 1
    elif board[x][y] == 10:
        #mud area + coin
        # reward_feature[0] = 1
        reward_feature[5] = 1
        reward_feature[3] = 1
    elif board[x][y] == 11:
        #mud area + roadblock
        # reward_feature[0] = 1
        reward_feature[5] = 1
        reward_feature[4] = 1
    return reward_feature

def find_reward_features(traj):
    traj_ts_x = traj[0][0]
    traj_ts_y = traj[0][1]
    # if is_in_gated_area(traj_ts_x,traj_ts_y):
    #     in_gated = True

    partial_return = 0
    prev_x = traj_ts_x
    prev_y = traj_ts_y

    phi = np.zeros(6)

    for i in range (1,4):
        if traj_ts_x + traj[i][0] >= 0 and traj_ts_x + traj[i][0] < 10 and traj_ts_y + traj[i][1] >=0 and traj_ts_y + traj[i][1] < 10 and not is_in_blocked_area(traj_ts_x + traj[i][0], traj_ts_y + traj[i][1]):
            # next_in_gated = is_in_gated_area(traj_ts_x + traj[i][0], traj_ts_y + traj[i][1])
            # if in_gated == False or  (in_gated and next_in_gated):
            traj_ts_x += traj[i][0]
            traj_ts_y += traj[i][1]

        phi += get_state_feature(traj_ts_x,traj_ts_y)
        prev_x = traj_ts_x
        prev_y = traj_ts_y

    return phi

def find_end_state(traj):
    in_gated =False
    traj_ts_x = traj[0][0]
    traj_ts_y = traj[0][1]
    # if is_in_gated_area(traj_ts_x,traj_ts_y):
    #     in_gated = True

    partial_return = 0
    prev_x = traj_ts_x
    prev_y = traj_ts_y

    for i in range (1,4):
        if traj_ts_x + traj[i][0] >= 0 and traj_ts_x + traj[i][0] < 10 and traj_ts_y + traj[i][1] >=0 and traj_ts_y + traj[i][1] < 10 and not is_in_blocked_area(traj_ts_x + traj[i][0], traj_ts_y + traj[i][1]):
            # next_in_gated = is_in_gated_area(traj_ts_x + traj[i][0], traj_ts_y + traj[i][1])
            # if in_gated == False or  (in_gated and next_in_gated):
            traj_ts_x += traj[i][0]
            traj_ts_y += traj[i][1]

            a = [traj_ts_x - prev_x, traj_ts_y - prev_y]
        else:
            a = [traj_ts_x + traj[i][0] - prev_x, traj_ts_y + traj[i][1] - prev_y]

        r = board_rf[prev_x][prev_y][find_action_index(a)]

        partial_return += r
        prev_x = traj_ts_x
        prev_y = traj_ts_y

    return traj_ts_x, traj_ts_y,partial_return

def get_all_statistics(questions,answers):
    pr_X = []
    vf_X = []
    none_X = []

    pr_y = []
    vf_y = []
    none_y = []

    pr_r = []
    vf_r = []
    none_r = []


    for i in range(len(questions)):
        assignment_qs = questions[i]
        assignment_as = answers[i]
        sample_n = assignment_as[0]
        disp_id = None
        cords_id = [0,0]
        for q,a in zip(assignment_qs, assignment_as):
            if a == "dis":
                continue
            if q == "observationType":
                if a == "0":
                    disp_id = "pr"
                elif a == "1":
                    disp_id = "vf"
                elif a == "2":
                    disp_id = "none"
                else:
                    print (a)
                    print ("disp id error")
                # print (disp_id)
                cords_id[1] = int(a)
                continue
            if q == "sampleNumber":
                # print (a)
                cords_id[0] = int(a)
                continue

            sample_dict_path = "/Users/stephanehatgiskessell/Desktop/Kivy_stuff/MTURK_interface/2021_07_29_data_samples/"  + disp_id + "_sample" + str(sample_n) + "/" + "sample" + str(sample_n) + "_dict.pkl"

            with open(sample_dict_path, 'rb') as f:
                sample_dict = pickle.load(f)
            num = int(q.replace("query",""))
            point = sample_dict.get(num)
            quad = point.get("quadrant")

            split_name = point.get("name").split("/")[-1].split("_")
            if (split_name[0] == "vf" or split_name[0] == "none"):
                pt = split_name[1]
                index = split_name[2]
            else:
                pt = split_name[0]
                index = split_name[1]


            if quad == "dsdt":
                traj_pairs = dsdt_data.get(pt)
            if quad == "dsst":
                traj_pairs = dsst_data.get(pt)
            if quad == "ssst":
                traj_pairs = ssst_data.get(pt)
            if quad == "sss":
                traj_pairs = sss_data.get(pt)


            pt_ = pt.replace("(","")
            pt_ = pt_.replace(")","")
            pt_ = pt_.split(",")
            x = float(pt_[0])
            y = float(pt_[1])

            poi = traj_pairs[int(index)]
            traj1 = poi[0]
            traj1_ts_x,traj1_ts_y, pr1 =find_end_state(traj1)
            traj1_v_s0 = board_vf[traj1[0][0]][traj1[0][1]]
            traj1_v_st = board_vf[traj1_ts_x][traj1_ts_y]

            phi1 = find_reward_features(traj1)

            traj2 = poi[1]
            traj2_ts_x,traj2_ts_y, pr2 =find_end_state(traj2)
            traj2_v_s0 = board_vf[traj2[0][0]][traj2[0][1]]
            traj2_v_st = board_vf[traj2_ts_x][traj2_ts_y]

            phi2 = find_reward_features(traj2)

            #make sure that our calculated pr/sv are the same as what the trajectory pair is marked as
            assert ((traj2_v_st - traj2_v_s0) - (traj1_v_st - traj1_v_s0) == x)
            assert (pr2 - pr1 == y)

            disp_type = point.get("disp_type")
            dom_val = point.get("dom_val")

            if a == "left":
                encoded_a = 0
            elif a == "right":
                encoded_a = 1
            elif a == "same":
                encoded_a = 0.5
            else:
                # print (a)
                encoded_a = None

            if disp_id == "vf":
                vf_X.append([phi1,phi2])
                vf_r.append([phi1,phi2])
                vf_y.append(encoded_a)
            elif disp_id == "pr":
                pr_X.append([phi1,phi2])
                pr_r.append([phi1,phi2])
                pr_y.append(encoded_a)
            elif disp_id == "none":
                none_X.append([phi1,phi2])
                none_r.append([phi1,phi2])
                none_y.append(encoded_a)
    return vf_X, vf_r, vf_y, pr_X, pr_r, pr_y, none_X, none_r, none_y

def augment_data(X,Y):
    aX = []
    ay = []
    for x,y in zip(X,Y):
        aX.append(x)
        ay.append(y)

        neg_x = [x[1],x[0]]
        aX.append(neg_x)
        if y == 0:
            ay.append(1)
        elif y == 1:
            ay.append(0)
        else:
            ay.append(0.5)
    return np.array(aX), np.array(ay)

def format_y(Y):
    formatted_y = []
    for y in Y:
        if y == 0:
            formatted_y.append(np.array([[1,0]]))
        elif y == 1:
            formatted_y.append(np.array([[0,1]]))
        elif y == 0.5:
            formatted_y.append(np.array([[0.5,0.5]]))
        # else:
        #     print (y)
    return torch.tensor(formatted_y,dtype=torch.float)

def format_X(X):
    return torch.tensor(X,dtype=torch.float)

class RewardFunction(torch.nn.Module):
    def __init__(self,n_features=6):
        super(RewardFunction, self).__init__()
        self.n_features = n_features
        # self.w = torch.nn.Parameter(torch.tensor(np.zeros(n_features).T,dtype = torch.float,requires_grad=True))
        self.linear1 = torch.nn.Linear(n_features, 1,bias=False)

    def forward(self, phi):
        # phi = torch.matmul(phi,self.w)
        # phi_logit =  torch.sigmoid(phi)
        phi_logit = torch.sigmoid(self.linear1(phi))
        return phi_logit


vf_X, vf_r, vf_y, pr_X, pr_r, pr_y, none_X, none_r, none_y = get_all_statistics(questions,answers)

aX, ay = augment_data(pr_X,pr_y)

def reward_pred_loss(output, target):
    batch_size = output.size()[0]
    output = torch.log(output)
    res = torch.mul(output,target)
    return -torch.sum(res)/batch_size

def train(aX, ay):
    torch.manual_seed(0)
    X_train, X_test, y_train, y_test = train_test_split(aX, ay,test_size=.2,random_state= 0)

    X_train = format_X(X_train)
    y_train = format_y(y_train)


    model = RewardFunction()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

    for epoch in range(5000):

        model.train()
        optimizer.zero_grad()
        # Forward pass
        y_pred = model(X_train)
        # Compute Loss
        # loss = F.cross_entropy(y_pred, y_train)
        loss = reward_pred_loss(y_pred, y_train)
        # Backward pass
        loss.backward()
        optimizer.step()
        # print (loss)
    for param in model.parameters():
        print (param)


    # print ("\n")
    # w = np.array([2.2008, 0.0672, 0.0669, 0.0925, 0.4213, 1.5453]).T
    # n_correct = 0
    # total= 0
    # for (x,y) in zip(X_test,y_test):
    #     # if y == 0.5:
    #     #     continue
    #     total +=1
    #     y_hat = np.matmul(x,w)
    #     if (y_hat[0] > y_hat[1]):
    #         res = 0
    #     elif (y_hat[1] > y_hat[0]):
    #         res = 1
    #     else:
    #         res = 0.5
    #     if res == y:
    #         n_correct += 1
    # print (n_correct/total)

        # print (model.parameters())
train(aX, ay)
