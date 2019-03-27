from QLearning import QL
from traffic_sim import TrafficSimulator

from sys import platform as sys_pf
if sys_pf == 'darwin':
    import matplotlib
    matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import scipy.io as sio
import numpy as np

def run():
    sum_info_l = []
    train_times = 500
    timestep = 1000
    for i in range(train_times):
        observation = env.restart()
        q.initial_State(observation)
        sum_info = 0
        for j in range(timestep):
            env.render()
            _, info = q.learning(env_step = env.step)
            sum_info += info
        sum_info_l.append(sum_info)
        # plt.plot(i, sum_info, 'g-*')
        # ax.plot(i, sum_info, color='r', linewidth=1, alpha=0.6)
        # print(f"({sum_info}, {i})")

    save_fn = 'data.mat'
    
    # save_array = np.array([1,2,3,4])
    sio.savemat(save_fn, {'info': np.array(sum_info_l) })

    plt.figure('Performance Graph')
    ax = plt.gca()
    ax.set_xlabel('time')
    ax.set_ylabel('the number of queueing cars')
    x = [i for i in range(train_times)]
    ax.plot(x, sum_info_l, color='r', linewidth=1, alpha=0.6)
    plt.show()





if __name__ == '__main__':
    env = TrafficSimulator()
    q = QL([str(i) for i in range(env.n_action)], epsilon = 1 - 0.1, gamma = 0.9, alpha = 0.1)
    # env.after(100,run)
    run()
    env.mainloop()