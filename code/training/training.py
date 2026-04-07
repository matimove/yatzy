from algorithms.q_learning import Qlearn
from  algorithms.random_pick import RandomPick
from game.yatzy import Yatzy
from game.stats import Stats



#---------------------#
agent = Qlearn()
agent.load_q_table("qtable.txt")
agent.load_model("model_params.txt")
#agent = RandomPick()
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
    
    if episode % 10000 == 0:
        avg_score = sum(scores[-10000:]) / len(scores[-10000:])
        avg_bonus = sum(bonuses[-10000:]) / len(bonuses[-10000:]) * 100
        print(f"Episode {episode} | Avg Score: {avg_score:.2f} | Bonus %: {avg_bonus:.2f} | Epsilon: {agent.epsilon:.3f}")
        #print("Unique states visited:", len(agent.Q_table))
        #stats.add_score(avg_score)

    if episode % 10000 == 0:
        agent.save_q_table("qtable.txt")
        agent.save_model("model_params.txt")


#stats.show_stats()

