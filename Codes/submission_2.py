import numpy as np
import matplotlib.pyplot as plt

class NonStationaryBandit:
    def _init_(self, n_arms=10):
        self.n_arms = n_arms
        self.mean_rewards = np.zeros(n_arms)

    def step(self, action):
        reward = np.random.normal(self.mean_rewards[action], 1)
        self.mean_rewards += np.random.normal(0, 0.01, self.n_arms)
        return reward

bandit = NonStationaryBandit()
n_steps = 1000
actions = np.zeros(n_steps)
rewards = np.zeros(n_steps)
q_values = np.zeros(bandit.n_arms)
action_counts = np.zeros(bandit.n_arms)
epsilon = 0.1

for step in range(n_steps):
    if np.random.rand() < epsilon:
        action = np.random.randint(bandit.n_arms)
    else:
        action = np.argmax(q_values)

    reward = bandit.step(action)

    action_counts[action] += 1
    n = action_counts[action]
    q_values[action] += (1/n) * (reward - q_values[action])

    actions[step] = action
    rewards[step] = reward

plt.figure(figsize=(12, 6))
plt.plot(rewards)
plt.title("Rewards over time in a Non-Stationary 10-Armed Bandit")
plt.xlabel("Time steps")
plt.ylabel("Reward")
plt.show()