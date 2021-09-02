import gym
import numpy as np
from collections import defaultdict
# import plotting
from grid_world import GridWorldEnv
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def value_iteration():

    # env = GridworldEnv()
    env = GridWorldEnv("2021-07-29_sparseboard2-notrap")

    GAMMA = 1
    FGAMMA = 1
    THETA = 0.001
    # initialize Q
    # Q = defaultdict(lambda: np.zeros(env.action_space))
    V = np.zeros((int(np.sqrt(env.observation_space)), int(np.sqrt(env.observation_space))))
    M = [[np.zeros(env.observation_space) for i in range(int(np.sqrt(env.observation_space)))] for j in range (int(np.sqrt(env.observation_space)))]

    actions = [[-1,0],[1,0],[0,-1],[0,1]]
    n = 0

    #----------------------------------------------------------------------------------------------------------------------------------------
    #iterativley learn state value
    #----------------------------------------------------------------------------------------------------------------------------------------
    while True:
        #loop through every state
        delta = 0
        for i in range (10):
            for j in range (10):
                v = V[i][j]
                state_Qs = []
                for a_index in range(len(actions)):
                    next_state, reward, done, _ = env.get_next_state((i,j),a_index)
                    ni,nj = next_state
                    if not done:
                        Q = reward + GAMMA*V[ni][nj]
                    else:
                        Q = reward
                    state_Qs.append(Q)
                V[i][j] = max(state_Qs)
                delta = max(delta,np.abs(v-V[i][j]))
        if delta < THETA:
            break
    #----------------------------------------------------------------------------------------------------------------------------------------
    #iterativley learn succesor features
    #----------------------------------------------------------------------------------------------------------------------------------------
    while True:
        #loop through every state
        delta = 0
        for i in range (10):
            for j in range (10):
                m = M[i][j]
                s_tab = env.state2tab(i,j)
                state_Qs = []
                state_Ms = []
                total_occupancies = []
                for a_index in range(len(actions)):
                    next_state, reward, done, _ = env.get_next_state((i,j),a_index)
                    # print (reward)
                    ni,nj = next_state
                    #and not (ni == i and nj == j)
                    if not done:
                        Q = reward + GAMMA*V[ni][nj]
                        m = s_tab + FGAMMA*M[ni][nj]
                    else:
                        Q = reward
                        m = s_tab
                    state_Qs.append(Q)
                    state_Ms.append(m)

                M[i][j] = state_Ms[np.argmax(state_Qs)]
                print (np.sum(np.abs((m-M[i][j]))))
                delta = max(delta,np.sum(np.abs((m-M[i][j]))))

        # print ("=======================================================")
        if delta < THETA:
            break


    # checks that the reward array*successor features == state value
    # for i in range (10):
    #     for j in range (10):
    #         m = M[i][j]
    #         V_pred = np.dot(m,env.reward_array)
    #         print (V[i][j])
    #         print (V_pred)
    #         print (m)
    #         print ("\n")
    #         assert (np.abs(V[i][j]) - np.abs(V_pred) <= 1 and np.abs(V[i][j]) - np.abs(V_pred) >= 0)
    #

# Q = np.load("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/boards/2021-07-29_sparseboard2-notrap_Qs.npy")
value_iteration()
