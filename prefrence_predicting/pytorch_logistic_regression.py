from sklearn.model_selection import train_test_split
import prefrence_stats_analysis
import torch
import numpy as np
import torch.nn.functional as F
import torch.nn as nn
from torch.autograd import Variable
from sklearn.model_selection import KFold,cross_val_score
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import random

def augment_data(X,Y):
    aX = []
    ay = []
    for x,y in zip(X,Y):
        aX.append(x)
        ay.append(y)
        neg_x = []
        for val in x:
            if val != 0:
                neg_x.append(-1*val)
            else:
                neg_x.append(val)

        aX.append(neg_x)
        if y == 0:
            ay.append(1)
        elif y == 1:
            ay.append(0)
        else:
            ay.append(0.5)
    return np.array(aX), np.array(ay)

def format_y(Y):
    formatted_y= []
    n_lefts = 0
    n_rights = 0
    n_sames = 0

    for y in Y:
        if y == 0:
            n_lefts +=1
            formatted_y.append([0])
        elif y == 0.5:
            n_sames +=1
            formatted_y.append([0.5])
        elif y ==1:
            n_rights +=1
            formatted_y.append([1])
    return torch.tensor(formatted_y,dtype=torch.float), [n_lefts/len(Y), n_rights/len(Y), n_sames/len(Y)]

def format_X (X):
    formatted_X= []
    for x in X:
        formatted_X.append([x[0] + x[1] - x[2]])
    return torch.tensor(formatted_X,dtype=torch.float)

def prefrence_pred_loss(output, target):
    batch_size = output.size()[0]
    output = torch.log(output)
    res = torch.mul(output,target)
    return -torch.sum(res)/batch_size

class LogisticRegression(torch.nn.Module):
     def __init__(self):
        super(LogisticRegression, self).__init__()
        self.linear1 = torch.nn.Linear(1, 2)
     def forward(self, x):
        y_pred = torch.sigmoid(self.linear1(x))
        return y_pred

# class PrefrenceBCELoss(nn.Module):
#     def __init__(self, **kwargs):
#         pass
#
#     def forward(self, output, target):
#         output = Variable(output, requires_grad=True)
#         target = Variable(target, requires_grad=True)
#         #torch.log
#         loss = torch.sum([torch.add(torch.mul(t[0],torch.log(o[0])),torch.mul(t[1],torch.log(o[1]))) for o,t in zip(output,target)])
#         loss = torch.mul(loss,(1 / target.size()[0]))
#         return loss


aX,ay = augment_data(prefrence_stats_analysis.X,prefrence_stats_analysis.y)


def train_and_eval(aX, ay):
    torch.manual_seed(0)
    # print (len(aX))
    aX = np.array(aX)
    ay = np.array(ay)

    kf = KFold(n_splits=10,random_state = 0,shuffle=True)
    total_testing_log_loss = 0
    total_training_log_loss = 0
    total_random_log_loss = 0
    fold = 0
    # for train_index, test_index in kf.split(aX):
    X_train, X_test, y_train, y_test = train_test_split(aX, ay,
                                                       test_size=.2, stratify=ay,
                                                       random_state= 0)

    fold+=1
    print ("On fold " + str(fold))
    # X_train = aX[train_index]
    # y_train = ay[train_index]
    # X_test = aX[test_index]
    # y_test = ay[test_index]


    X_train =format_X(X_train)
    y_train,_ = format_y(y_train)
    model = LogisticRegression()
    # criterion = torch.nn.BCELoss()
    # criterion = PrefrenceBCELoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.005)

    for epoch in range(3000):
        model.train()
        optimizer.zero_grad()
        # Forward pass
        y_pred = model(X_train)
        # Compute Loss
        loss = prefrence_pred_loss(y_pred, y_train)
        # Backward pass
        loss.backward()
        optimizer.step()
    total_training_log_loss += prefrence_pred_loss(y_pred, y_train)

    with torch.no_grad():
        y_test,class_probs = format_y(y_test)
        X_test =format_X(X_test)
        y_pred_test = model(X_test)
        total_testing_log_loss+=prefrence_pred_loss(y_pred_test, y_test)
        for param_name, param in model.named_parameters():
            print (param_name)
            print (param)
        print ("\n")
            #
            # random_pred = torch.tensor([[0.5,0.5] for i in range(len(y_test))],dtype=torch.float)
            # total_random_log_loss+=prefrence_pred_loss(random_pred, y_test)


    print("%0.5f mean testing log loss across 10 folds" % (total_testing_log_loss/fold))
    print("%0.5f mean training log loss across 10 folds" % (total_training_log_loss/fold))

train_and_eval(aX, ay)
