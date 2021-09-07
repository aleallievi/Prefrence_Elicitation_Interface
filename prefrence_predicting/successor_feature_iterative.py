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
    phi = np.zeros(env.num_state_types)
    psi = [[np.zeros(len(phi)) for i in range(int(np.sqrt(env.observation_space)))] for j in range (int(np.sqrt(env.observation_space)))]

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
                if env.is_blocked(i,j):
                    continue
                v = V[i][j]
                state_Qs = []
                for a_index in range(len(actions)):
                    next_state, reward, next_state_type, done, _ = env.get_next_state((i,j),a_index)
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
                if env.is_blocked(i,j):
                    continue
                psi_original = psi[i][j]
                # print ("here")
                state_Qs = []
                state_psis = []
                for a_index in range(len(actions)):
                    next_state, reward, phi, done, _ = env.get_next_state((i,j),a_index)
                    # print (reward)
                    ni,nj = next_state
                    if not done:
                        Q = reward + GAMMA*V[ni][nj]
                        psi_temp = phi + FGAMMA*psi[ni][nj]
                    else:
                        Q = reward
                        psi_temp = phi

                    state_Qs.append(Q)
                    state_psis.append(psi_temp)

                psi[i][j] = state_psis[np.argmax(state_Qs)]
                delta = max(delta,np.sum(np.abs((psi_original-psi[i][j]))))

        if delta < THETA:
            breakpoint()
            break


    # # checks that the reward array*successor features == state value
    # for i in range (10):
    #     for j in range (10):
    #         m = M[i][j]
    #         V_pred = 0
    #         # V_pred = np.dot(m,env.reward_array)
    #         # V_pred -= np.abs(env.reward_array[i + 10*j]) #make sure we do not give award for start state
    #         # print ((i,j))
    #         # print (V_pred - V[i][j])
    #         # # print (V_pred)
    #         # print (m)
    #         last_pos = None
    #         for n in range(len(m)):
    #             if m[n] == 1:
    #                 # print(env.reward_array[n])
    #                 x = n % 10
    #                 y = n // 10
    #                 if last_pos != None:
    #                     a = [x-last_pos[0],y-last_pos[1]]
    #                     a_index = env.find_action_index(a)
    #                     next_state, reward, done, _ = env.get_next_state((last_pos[0],last_pos[1]),a_index)
    #                     V_pred += reward
    #
    #                 last_pos =[x,y]

            # # print ("\n")
            # if V[i][j] != V_pred:
            #     last_pos = None
            #     for n in range(len(m)):
            #         if m[n] == 1:
            #             # print(env.reward_array[n])
            #             x = n % 10
            #             y = n // 10
            #             print ((x,y))
            #             if last_pos != None:
            #                 a = [x-last_pos[0],y-last_pos[1]]
            #                 a_index = env.find_action_index(a)
            #                 next_state, reward, done, _ = env.get_next_state((last_pos[0],last_pos[1]),a_index)
            #                 print (reward)
            #                 # V_pred += reward
            #
            #             last_pos =[x,y]
            #             print ("\n")
            #
            #     print ("\n\n")
            #     print (V[i][j])
            #     print (V_pred)
            #     print ("\n")
            #     assert False
            # assert (V[i][j] == V_pred)


# Q = np.load("/Users/stephanehatgiskessell/Desktop/Kivy_stuff/boards/2021-07-29_sparseboard2-notrap_Qs.npy")
value_iteration()
