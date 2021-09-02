import gym
import numpy as np
from collections import defaultdict
# import plotting
from grid_world import GridWorldEnv
import random
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
#https://github.com/manantomar/DSR/blob/master/SR/SR-TD-Learning.py
#https://github.com/awjuliani/successor_examples/blob/master/SR-SARSA.ipynb

# def sample_action(state,EPSILON,observation_size,action_size,M):
#
#     if np.random.sample() < EPSILON:
#         action = np.random.choice(action_size)
#     else:
#         ones = np.zeros(observation_size)
#         ones[state] = 1
#         action = np.argmax(np.matmul(M[:,state,:],ones))
#         print (action)
#     return action

def SARSA_train():

    # env = GridworldEnv()
    env = GridWorldEnv("2021-07-29_sparseboard2-notrap")

    EPSILON = 1
    GAMMA = 0.99
    LEARNING_RATE = 5e-2
    NUM_EPISODES = 500
    NUM_MINIBATCHES = 10
    BATCH_SIZE = 100
    # initialize Q
    Q = defaultdict(lambda: np.zeros(env.action_space))
    # M = np.zeros((env.observation_space.n, env.observation_space.n))
    M = np.identity(env.observation_space)
    w = np.zeros(env.observation_space)

    D = []
    n_samples = 0
    sample_n2sample = {}
    total_rewards = []
    all_batch_td_errors = []

    for i in range(NUM_EPISODES):
        env.set_start_state((0,0))
        state = env.reset()
        #state = convert(env.agentPos)
        steps = 0
        total_reward = 0
        while True:

            if np.random.sample() < EPSILON:
                action = np.random.choice(env.action_space)
            else:
                ones = np.zeros(env.observation_space)
                ones[state] = 1
                action = np.argmax(np.matmul(M[state],ones))

            next_state, reward, done, _ = env.step(action)
            # env.render()
            D.append((state,reward,action,next_state,done,n_samples))
            sample_n2sample[n_samples] = (state,reward,action,next_state,done,n_samples)
            n_samples+=1
            total_reward += reward

            state = next_state
            steps += 1
            if done:
                break
        total_rewards.append(total_reward)


        batch_td_errors = []
        for j in range(NUM_MINIBATCHES):
            #sample from memory replay and train
            if (len(D) > BATCH_SIZE):
                samples = random.sample(D,BATCH_SIZE)
            else:
                samples = D

            for sample in samples:
                state,reward,action,next_state,done,sample_n = sample
                ones = np.zeros(env.observation_space)
                ones[state] = 1

                next_ones = np.zeros(env.observation_space)
                next_ones[next_state] = 1
                if done:
                    td_error = ones + GAMMA*next_ones - M[state]
                else:
                    # _,_,next_action,_,_,_ = sample_n2sample.get(sample_n)

                    td_error = ones + GAMMA * M[next_state] - M[state]

                batch_td_errors.append(td_error)
                #update future occurances of next state table
                M[state] += LEARNING_RATE * td_error
                #update rewards weights
                # print (w[next_state])
                reward_error = reward - w[next_state]

                w[next_state] += LEARNING_RATE * reward_error
        all_batch_td_errors.append(np.mean(batch_td_errors))
    plt.plot(all_batch_td_errors)
    # plt.plot(total_rewards)
    plt.show()


def policy_train(Q):

    # env = GridworldEnv()
    env = GridWorldEnv("2021-07-29_sparseboard2-notrap")

    EPSILON = 1
    GAMMA = 0.99
    LEARNING_RATE = 5e-2
    NUM_EPISODES = 200
    NUM_MINIBATCHES = 10
    BATCH_SIZE = 100
    MAX_STEPS = 50
    # initialize Q
    # Q = defaultdict(lambda: np.zeros(env.action_space))
    # M = np.zeros((env.observation_space.n, env.observation_space.n))
    M = np.identity(env.observation_space)
    w = np.zeros(env.observation_space)

    D = []
    n_samples = 0
    sample_n2sample = {}
    total_rewards = []
    all_batch_td_errors = []

    for i in range(NUM_EPISODES):
        env.set_start_state((0,0))
        state = env.reset()
        #state = convert(env.agentPos)
        steps = 0
        total_reward = 0
        while True:

            if np.random.sample() < EPSILON:
                action = np.random.choice(env.action_space)
            else:
                # ones = np.zeros(env.observation_space)
                # ones[state] = 1
                x = state // 10
                y = state % 10
                action = env.find_action_index(np.argmax(Q[x][y]))

            next_state, reward, done, _ = env.step(action)
            # env.render()
            D.append((state,reward,action,next_state,done,n_samples))
            sample_n2sample[n_samples] = (state,reward,action,next_state,done,n_samples)
            n_samples+=1
            total_reward += reward

            state = next_state
            steps += 1
            if done or steps > MAX_STEPS:
                break
        total_rewards.append(total_reward)


        batch_td_errors = []
        for j in range(NUM_MINIBATCHES):
            #sample from memory replay and train
            if (len(D) > BATCH_SIZE):
                samples = random.sample(D,BATCH_SIZE)
            else:
                samples = D

            for sample in samples:
                state,reward,action,next_state,done,sample_n = sample
                ones = np.zeros(env.observation_space)
                ones[state] = 1

                next_ones = np.zeros(env.observation_space)
                next_ones[state] = 1
                if done:
                    td_error = ones + GAMMA*next_ones - M[state]
                else:
                    # _,_,next_action,_,_,_ = sample_n2sample.get(sample_n)

                    td_error = ones + GAMMA * M[next_state] - M[state]

                batch_td_errors.append(td_error)
                #update future occurances of next state table
                M[state] += LEARNING_RATE * td_error
                #update rewards weights
                # print (w[next_state])
                reward_error = reward - w[next_state]

                w[next_state] += LEARNING_RATE * reward_error
        all_batch_td_errors.append(np.mean(batch_td_errors))
    plt.plot(all_batch_td_errors)
    # plt.plot(total_rewards)
    plt.show()
