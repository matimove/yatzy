from algorithms.q_learning import Qlearn
from  algorithms.random_pick import RandomPick
from  algorithms.neural_net import NN
from game.yatzy import Yatzy
from game.stats import Stats
import numpy as np

np.random.seed(0)

# tiny dataset
X = np.random.randn(24, 5)   # 5 samples
Y = np.random.randn(47, 5)

model = NN()
model.initialize()

lr = 1e-3

for epoch in range(500):
    total_loss = 0

    for i in range(X.shape[1]):
        x = X[:, i].reshape(-1, 1)
        y = Y[:, i].reshape(-1, 1)

        A1, A2, A3 = model.forward_pass(x)

        # simple MSE loss
        loss = np.mean((A3 - y) ** 2)
        total_loss += loss

        # gradient of MSE
        dA3 = 2 * (A3 - y)

        # backprop
        grads = model.backward(x, A1, A2, A3, dA3)

        # update
        for k in model.net:
            model.net[k] -= lr * grads[k]

    if epoch % 10 == 0:
        print(f"Epoch {epoch}, Loss: {total_loss:.4f}")