import numpy as np
import torch.nn.functional as F
import torch.nn as nn
import pickle
import re
import matplotlib
import json
import torch
from sklearn.model_selection import train_test_split
import math

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
        if (traj_ts_x,traj_ts_y) != (prev_x,prev_y):
            phi += get_state_feature(traj_ts_x,traj_ts_y)
        else:
            #only keep the gas/mud area score
            phi += (get_state_feature(traj_ts_x,traj_ts_y)*[1,0,0,0,0,1])

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


def generate_t_nt_samples(terminating, non_terminating):
    phis = []
    y = []
    rewards = []
    for i in range (min(len(terminating),len(non_terminating))):
        phis.append([terminating[i][0],non_terminating[i][0]])
        rewards.append([terminating[i][1], non_terminating[i][1]])
        #[gas, goal, sheep, coin, roadblock, mud]

        # assert (terminating[i][1] == np.dot(terminating[i][0], [-1,50,-50,1,-1,-2]))

        # print (non_terminating[i][1])
        # print (non_terminating[i][0])
        # print ("\n")
        # assert (non_terminating[i][1] == np.dot(non_terminating[i][0], [-1,50,-50,1,-1,-2]))

        if terminating[i][1] > non_terminating[i][1]:
            y.append([1,0])
        elif terminating[i][1] < non_terminating[i][1]:
            y.append([0,1])
        elif terminating[i][1] == non_terminating[i][1]:
            y.append([0.5,0.5])

    return phis,y,rewards

def get_all_statistics(questions,answers):
    pr_X = []
    vf_X = []
    none_X = []

    pr_X_terminating = []
    vf_X_terminating = []
    none_X_terminating = []

    pr_X_non_terminating = []
    vf_X_non_terminating = []
    none_X_non_terminating = []

    pr_y = []
    vf_y = []
    none_y = []

    pr_r = []
    vf_r = []
    none_r = []

    n_incorrect = 0
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

            #TODO: THIS IS A POTENTIALLY MAJOR BUG, RIGHT NOW IT IS NOT VERY IMPACTFUL BUT MAKE SURE TO FIX LATER
            if (pr1 != np.dot(phi1, [-1,50,-50,1,-1,-2])) or (pr2 != np.dot(phi2, [-1,50,-50,1,-1,-2])):
                n_incorrect+=1
                continue

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
                vf_r.append([pr1,pr2])
                vf_y.append(encoded_a)
                if quad == "dsst" or quad == "ssst":
                    vf_X_terminating.append([phi1,pr1])
                    vf_X_terminating.append([phi2,pr2])
                elif quad == "dsdt" or quad == "sss":
                    vf_X_non_terminating.append([phi1,pr1])
                    vf_X_non_terminating.append([phi2,pr2])

            elif disp_id == "pr":
                pr_X.append([phi1,phi2])
                pr_r.append([pr1,pr2])
                pr_y.append(encoded_a)
                if quad == "dsst" or quad == "ssst":
                    pr_X_terminating.append([phi1,pr1])
                    pr_X_terminating.append([phi2,pr2])
                elif quad == "dsdt" or quad == "sss":
                    pr_X_non_terminating.append([phi1,pr1])
                    pr_X_non_terminating.append([phi2,pr2])

            elif disp_id == "none":
                none_X.append([phi1,phi2])
                none_r.append([pr1,pr2])
                none_y.append(encoded_a)
                if quad == "dsst" or quad == "ssst":
                    none_X_terminating.append([phi1,pr1])
                    none_X_terminating.append([phi2,pr2])
                elif quad == "dsdt" or quad == "sss":
                    none_X_non_terminating.append([phi1,pr1])
                    none_X_non_terminating.append([phi2,pr2])

    vf_X_add, vf_y_add, vf_add_r = generate_t_nt_samples(vf_X_terminating, vf_X_non_terminating)
    pr_X_add, pr_y_add, pr_add_r = generate_t_nt_samples(pr_X_terminating, pr_X_non_terminating)
    none_X_add, none_y_add, none_add_r = generate_t_nt_samples(none_X_terminating, none_X_non_terminating)

    #adds syntheitc prefrences between termianting and non-terminating trajectory
    # vf_X.extend(vf_X_add)
    # vf_r.extend(vf_add_r)
    # vf_y.extend(vf_y_add)
    #
    # pr_X.extend(pr_X_add)
    # pr_r.extend(pr_add_r)
    # pr_y.extend(pr_y_add)
    #
    # none_X.extend(none_X_add)
    # none_r.extend(none_add_r)
    # none_y.extend(none_y_add)

    # print (n_incorrect)


    return vf_X, vf_r, vf_y, pr_X, pr_r, pr_y, none_X, none_r, none_y

def augment_data(X,Y,ytype="scalar"):
    aX = []
    ay = []
    for x,y in zip(X,Y):
        aX.append(x)
        ay.append(y)

        neg_x = [x[1],x[0]]
        aX.append(neg_x)
        if ytype == "scalar":
            ay.append(1-y)
        else:
            ay.append([y[1],y[0]])

    return np.array(aX), np.array(ay)

def format_y(Y,ytype="scalar"):
    formatted_y = []
    if ytype=="scalar":
        for y in Y:
            if y == 0:
                formatted_y.append(np.array([1,0]))
            elif y == 1:
                formatted_y.append(np.array([0,1]))
            elif y == 0.5:
                formatted_y.append(np.array([0.5,0.5]))
    else:
        formatted_y = Y
        # for y in Y:
        #     formatted_y.append([y])

    return torch.tensor(formatted_y,dtype=torch.float)

def format_X(X):
    return torch.tensor(X,dtype=torch.float)

def sigmoid(val):
    return 1 / (1 + math.exp(-val))

def generate_synthetic_prefs(rewards,mode):
    synth_y = []
    for r in rewards:
        if mode == "sigmoid":
            pref = [sigmoid(r[0]-r[1]),sigmoid(r[1]-r[0])] #TODO: im pretty sure it is r2-r1 and not r1-r2
        elif mode == "max":
            if r[0] > r[1]:
                pref = [1,0]
            elif r[1] > r[0]:
                pref = [0,1]
            elif r[1] == r[0]:
                pref = [0.5,0.5]
        synth_y.append(pref)
    return synth_y


def reward_pred_loss(output, target):
    batch_size = output.size()[0]
    output = torch.squeeze(output)
    output = torch.log(output)
    res = torch.mul(output,target)
    return -torch.sum(res)/batch_size


def validate_synth_data(X,y):
    for i in range(len(X)):
        r1 = np.dot(X[i][0], [-1,50,-50,1,-1,-2])
        r2 = np.dot(X[i][1], [-1,50,-50,1,-1,-2])

        pref_prob = [sigmoid(r1-r2),sigmoid(r2-r1)]
        if pref_prob[0] > pref_prob[1]:
            recovered_pref = [1,0]
        elif pref_prob[1] > pref_prob[0]:
            recovered_pref = [0,1]
        else:
            recovered_pref = [0.5,0.5]
        # synth_loss = reward_pred_loss(torch.tensor([recovered_pref],dtype=torch.float),torch.tensor([y[i]],dtype=torch.float))
        # assert (synth_loss == 0)
        assert (recovered_pref[0] == y[i][0] and recovered_pref[1] == y[i][1])



class RewardFunction(torch.nn.Module):
    def __init__(self,n_features=6):
        super(RewardFunction, self).__init__()
        self.n_features = n_features
        # self.w = torch.nn.Parameter(torch.tensor(np.zeros(n_features).T,dtype = torch.float,requires_grad=True))
        self.linear1 = torch.nn.Linear(self.n_features, 1,bias=False)

    def forward(self, phi):
        # phi = torch.matmul(phi,self.w)
        # phi_logit =  torch.sigmoid(phi)
        phi_logit = torch.sigmoid(self.linear1(phi))
        return phi_logit

vf_X, vf_r, vf_y, pr_X, pr_r, pr_y, none_X, none_r, none_y = get_all_statistics(questions,answers)

synth_sig_y = generate_synthetic_prefs(pr_r,"sigmoid")
synth_max_y = generate_synthetic_prefs(pr_r,"max")


# aX, ay = augment_data(pr_X,pr_y,"scalar")
aX, ay = augment_data(pr_X,synth_sig_y,"arr")
# aX, ay = augment_data(pr_X,synth_max_y,"arr")
# validate_synth_data(aX,ay)
# print (len(aX))

def model_eval(w,X,Y):
    # w = np.array([ 2.2874,  0.4489,  0.0879,  0.0262, -0.0747,  0.9900]).T
    n_correct = 0
    total= 0
    # for (x,y) in zip(X_test,y_test):
    #     # if y == 0.5:
    #     #     continue
    #     total +=1
    #     y_hat = np.matmul(x,w)
    #     # print (y_hat)
    #     if (y_hat[0] > y_hat[1]):
    #         res = [1,0]
    #     elif (y_hat[1] > y_hat[0]):
    #         res = [0,1]
    #     else:
    #         res = [0.5,0.5]
    #     if res[0] == y[0] and res[1] == y[1]:
    #         n_correct += 1
    # print (n_correct/total)
    # #
    for (x,y) in zip(X,Y):
        # if y == 0.5:
        #     continue
        total +=1
        r = np.matmul(x,w)
        y_hat = [sigmoid(r[0]-r[1]),sigmoid(r[1]-r[0])]
        # print (r)
        # print (y)
        # print ("\n")
        if (y_hat[0] > y_hat[1]):
            res = [1,0]
        elif (y_hat[1] > y_hat[0]):
            res = [0,1]
        else:
            res = [0.5,0.5]

        if (y[0] > y[1]):
            y_f = [1,0]
        elif (y[1] > y[0]):
            y_f = [0,1]
        else:
            y_f = [0.5,0.5]

        if res[0] == y_f[0] and res[1] == y_f[1]:
            n_correct += 1
    print (n_correct/total)


def train(aX, ay):
    torch.manual_seed(0)
    X_train, X_test, y_train, y_test = train_test_split(aX, ay,test_size=.2,random_state= 0,shuffle=True)
    #
    X_train = format_X(X_train)
    y_train = format_y(y_train,"arr")

    model = RewardFunction()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

    for epoch in range(50000):

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
        print (loss)
    for param in model.parameters():
        print (param)

    #double check x*w = prefrence
    #plot training/testing curve (ie: should not be exactly identical)
    #check outputted logits from model.forward() - maybe generate synthetic dataset (ie: phi1, ph2, gt pr's, logits, gt prefrence, pred prefrence)
    #try removing trajectories with terminating states and see what results we get
    #[gas, goal, sheep, coin, roadblock, mud]
    model_eval(X_train,y_train,np.array([ 2.2874,  0.4489,  0.0879,  0.0262, -0.0747,  0.9900]).T)
    model_eval(X_test,y_test,np.array([ 2.2874,  0.4489,  0.0879,  0.0262, -0.0747,  0.9900]).T)


        # print (model.parameters())
train(aX, ay)
