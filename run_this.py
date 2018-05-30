from QLearning import QL
from traffic_sim import TrafficSimulator

def run():
    for i in range(100):
        observation = env.restart()
        q.initial_State(observation)
        











if __name__ == '__main__':
    env = TrafficSimulator()
    q = QL([str(i) for i in range(env.n_action)], 0.9, 0.9, 0.1)
    env.after(100,run)
    env.mainloop()