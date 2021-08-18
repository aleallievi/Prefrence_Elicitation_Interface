import numpy as np
import prefrence_stats_analysis
from sklearn import metrics
from sklearn.model_selection import KFold,cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import random

class LogisticPrefs:
    def __init__(self,c, n_features = 1,random_state = None):
        self.random_state = random_state
        self.n_features = n_features
        self.beta = np.array([[c] for i in range(2)]).T
        self.lr = 0.005
        self.epochs = 500

    def set_beta(self,b1,b2):
        self.beta = np.array([[b1],[b2]]).T

    def normalize(self,X):
        return X - X.mean()

    def predict(self, X):
        #returns probability of preferring the right trajectory
        if len(X.shape) == 1:
            return 1/(1+np.exp(np.dot(X,self.beta)))
        return np.array([1/(1+np.exp(np.dot(x,self.beta))) for x in X])

    def evaluate(self,X,Y):
        X = self.normalize(X)
        loss = (1 / len(X))*-1*sum([y[1]*np.log(self.predict(x)[1]) + (y[0])*np.log(1 - self.predict(x)[1]) for x,y in zip(X,Y)])
        return loss

    def fit(self,X,Y):
        #Y: 0 for left, 0.5 for same, 1 for right
        X = self.normalize(X)
        for epoch in range(self.epochs):
            y_pred = self.predict(X)
            #https://math.stackexchange.com/questions/2503428/derivative-of-binary-cross-entropy-why-are-my-signs-not-right
            pd = (1 / len(X))*np.dot(X.T,(y_pred - Y))
            self.beta = np.add(self.beta,self.lr*pd)

            loss = (1 / len(X))*-1*sum([y[1]*np.log(self.predict(x)[1]) + y[0]*np.log(1 - self.predict(x)[1]) for x,y in zip(X,Y)])
            print (loss)

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
            formatted_y.append([1,0])
        elif y == 0.5:
            n_sames +=1
            formatted_y.append([0.5,0.5])
        elif y ==1:
            n_rights +=1
            formatted_y.append([0,1])
    return np.array(formatted_y), [n_lefts/len(Y), n_rights/len(Y), n_sames/len(Y)]

def format_X (X):
    formatted_X= []
    for x in X:
        formatted_X.append([x[0] + x[1] - x[2]])
    return np.array(formatted_X)


aX,ay = augment_data(prefrence_stats_analysis.X,prefrence_stats_analysis.y)
X_train, X_test, y_train, y_test = train_test_split(aX, ay,
                                                   test_size=.2, stratify=ay,
                                                   random_state= 0)


y_train,_ = format_y(y_train.T)
X_train =format_X(X_train)
model = LogisticRegression(random_state=0,multi_class="ovr")
model.fit(X_train, y_train)


#
# y_train,_ = format_y(y_train)
# X_train =format_X(X_train)
#
# model = LogisticPrefs(1)
# model.fit(X_train,y_train)
#
# y_test_,class_probs = format_y(y_test)
# X_test =format_X(X_test)
#
# # pred = model.predict(X_test[:3])
#
# log_loss = model.evaluate(X_test,y_test_)
# print("\n%0.2f log loss" % log_loss)
#
# probabilities = [class_probs for _ in range(len(y_test_))]
# random_log_loss = metrics.log_loss(formatted_y_test, probabilities)

# kf = KFold(n_splits=10,random_state = 0,shuffle=True)
# total_log_loss = 0
# total_random_log_loss = 0
# fold = 0
# for train_index, test_index in kf.split(aX):
#     fold+=1
#     print ("On fold " + str(fold))
#     X_train = aX[train_index]
#     y_train = ay[train_index]
#     X_test = aX[test_index]
#     y_test = ay[test_index]
#
#     y_train,_ = format_y(y_train)
#     X_train =format_X(X_train)
#     model = LogisticPrefs(1)
#     model.fit(X_train,y_train)
#
#     formatted_y_test = []
#     for y in y_test:
#         if y == 0:
#             formatted_y_test.append(-1)
#         elif y == 0.5:
#             formatted_y_test.append(0)
#         elif y ==1:
#             formatted_y_test.append(1)
#     #
#     #
#     y_test_,class_probs = format_y(y_test)
#     X_test =format_X(X_test)
#     log_loss = model.evaluate(X_test,y_test_)
#     total_log_loss+=log_loss

    #
    # probabilities = [class_probs for _ in range(len(y_test_))]
    # random_log_loss = metrics.log_loss(formatted_y_test, probabilities)
    # total_random_log_loss+=random_log_loss
# print("%0.2f mean log loss" % (total_log_loss/10))
    # probabilities = [class_probs for _ in range(len(y_test_))]
    # random_log_loss = metrics.log_loss(formatted_y_test, probabilities)
# print('Baseline: Log Loss=%.3f' % (total_random_log_loss/10))
#0.70 mean log loss
