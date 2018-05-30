from QLearning import QL
from traffic_sim import TrafficSimulator

# from sys import platform as sys_pf
# if sys_pf == 'darwin':
#     import matplotlib
#     matplotlib.use("TkAgg")
# import matplotlib.pyplot as plt


def run():
    # plt.figure()
    for i in range(20):
        observation = env.restart()
        q.initial_State(observation)
        sum_info = 0
        for j in range(1000):
            # env.render()
            _, info = q.learning(env_step = env.step)
            sum_info += info
        # plt.plot(i, sum_info, 'g-*')
        print(f"({sum_info}, {i})")
    # plt.show()





if __name__ == '__main__':
    env = TrafficSimulator()
    q = QL([str(i) for i in range(env.n_action)], 0.9, 0.9, 0.1)
    # env.after(100,run)
    run()
    env.mainloop()