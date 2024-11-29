import numpy as np

epsilon = 0.1
n_actions = 2
q_values = np.zeros(n_actions)
action_counts = np.zeros(n_actions)

n_steps = 10000

def binaryBanditA(action):
    p = [0.1, 0.2]
    return 1 if np.random.rand() < p[action] else 0

def binaryBanditB(action):
    p = [0.8, 0.9]
    return 1 if np.random.rand() < p[action] else 0

for step in range(n_steps):
    if np.random.rand() < epsilon:
        action = np.random.randint(n_actions)
    else:
        action = np.argmax(q_values)

    reward = binaryBanditA(action) if np.random.rand() < 0.5 else binaryBanditB(action)

    action_counts[action] += 1
    n = action_counts[action]
    q_values[action] += (1/n) * (reward - q_values[action])

print(f"Q-value for Action 1: {q_values[0]}")
print(f"Q-value for Action 2: {q_values[1]}")