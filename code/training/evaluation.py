from algorithms.q_learning import Qlearn
from  algorithms.random_pick import RandomPick
from game.yatzy import Yatzy
from game.stats import Stats



#---------------------#
agent = Qlearn()
agent.load_q_table("qtable.txt")
agent.load_model("model_params.txt")
#---------------------#
env = Yatzy()
env.set_prints_on()
#---------------------#
stats = Stats()
#---------------------#
episodes = 1
#---------------------#
scores = []
bonuses = []

for episode in range(episodes):
    print("New game begins...")
    state = env.reset()

    done = False

    while True:
        print("----------------------------------------------------------------------------")
        print("State: ", state)
        action = agent.choose_action(state)
        print("Action: ", action)

        next_state, reward, done, final_score, info = env.step(action)

        agent.update(state, action, reward, next_state)

        state = next_state

        print(env.scoreboard.return_scoreboard())

        if done:
            scores.append(final_score[0])
            bonuses.append(final_score[1])
            break
    
    if episode % 10000 == 0:
        avg_score = sum(scores[-10000:]) / len(scores[-10000:])
        avg_bonus = sum(bonuses[-10000:]) / len(bonuses[-10000:]) * 100
        print(f"Episode {episode} | Avg Score: {avg_score:.2f} | Bonus %: {avg_bonus:.2f} | Epsilon: {agent.epsilon:.3f}")
       