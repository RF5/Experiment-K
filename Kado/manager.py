import gym
from wam import Wam
from tau_buffer import TauBuffer, Rollout
import numpy as np
import random

sigma = 0.002
gamma = 0.99
n_population = 40
trunc_size = 4

def train():
    env = gym.make('CartPole-v0')
    env.reset()

    pop = []
    next_gen = []

    for i in range(n_population):
        pop.append(Wam('ID:' + str(i)))
        next_gen.append(Wam('2/ID:' + str(i)))

    total_timesteps = 0

    for g in range(6):

        if g != 0:
            for ii in range(n_population):
                kappa = random.sample(pop[0:trunc_size], 1)
                mutate(kappa[0], next_gen[ii])

            tmp = pop
            pop = next_gen
            next_gen = tmp
        
        for agent in pop:
            agent.score = 0
            observation = env.reset()

            for t in range(150):
                #env.render()
                #print(observation)
                action = agent.predict(observation)

                observation, reward, done, info = env.step(action)
                total_timesteps += 1
                agent.score = gamma*agent.score + reward

                if done:
                    print("Episode finished after {} timesteps with reward: {} ({})".format(t+1, agent.score, agent.name))
                    break

        pop = sorted(pop, key=lambda agent: agent.score, reverse=True)

    print("-----------------------------------------")
    for agent in pop[:trunc_size]:
        print(agent)
    print("solved in {} timesteps".format(total_timesteps))

def mutate(parent, child):
    old_params = parent.model.get_weights()
    new_params = []
    for param in old_params:
        new_params.append(param + sigma*np.random.randn(*param.shape))
    child.model.set_weights(new_params)

if __name__ == '__main__':
    train()