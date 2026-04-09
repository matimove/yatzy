from algorithms.q_learning import Qlearn
from  algorithms.random_pick import RandomPick
from  algorithms.neural_net import NN
from game.yatzy import Yatzy
from game.stats import Stats



#---------------------#
#agent = RandomPick()
agent = NN()
agent.initialize()
#---------------------#
env = Yatzy()
#---------------------#
stats = Stats()
#---------------------#
episodes = 1_000_000
#---------------------#
scores = []
bonuses = []

for episode in range(episodes):
    
    state = env.reset()

    done = False

    while True:

        action = agent.choose_action(state)

        next_state, reward, done, final_score, info = env.step(action)

        agent.update(state, action, reward, next_state)

        state = next_state

        if done:
            #stats.add_score(final_score)
            scores.append(final_score[0])
            bonuses.append(final_score[1])
            break

    agent.decay_epsilon()
    
    if episode % 100 == 0:
        avg_score = sum(scores[-100:]) / len(scores[-100:])
        avg_bonus = sum(bonuses[-100:]) / len(bonuses[-100:]) * 100
        print(f"Episode {episode} | Avg Score: {avg_score:.2f} | Bonus %: {avg_bonus:.2f} | Epsilon: {agent.epsilon:.3f}")
        #print("Unique states visited:", len(agent.Q_table))
        #stats.add_score(avg_score)

#stats.show_stats()

