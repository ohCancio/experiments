from brain import BrainSimulator
import random
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import imageio
import time
import gc
import threading


if __name__ == '__main__':
    # Determine brain properties
    brain_size = (50, 50, 50)

    # Determine initial state based on cubic-shaped shock to the brain (TODO: review with ethics board.)
    center_position = (10, 10, 10)
    shock_radius = (5, 5, 5)
    shocked_positions = [(center_position[0] + i, center_position[1] + j, center_position[2] + k)
                         for i in range(-shock_radius[0], shock_radius[0])
                         for j in range(-shock_radius[1], shock_radius[1])
                         for k in range(-shock_radius[2], shock_radius[2])]

    constantly_fixed_positions = [(center_position[0] + i, center_position[1] + j, center_position[2] + k)
                                  for i in range(-shock_radius[0], shock_radius[0])
                                  for j in range(-shock_radius[1], shock_radius[1])
                                  for k in range(-shock_radius[2], shock_radius[2])]

    generations = 20
    sem = threading.Semaphore()

    for generation in range(1, generations+1):

        print("Generation {} of {}".format(generation, generations))

        initial_state = {pos: (random.randint(0, 100)/100) for pos in shocked_positions}
        fixed_positions = {pos: (random.randint(0, 100)/100) for pos in constantly_fixed_positions}

        # brain_simulator = BrainSimulator(size=brain_size, initial_state=initial_state, fixed_positions=fixed_positions)
        brain_simulator = BrainSimulator(size=brain_size, fixed_positions=fixed_positions)
        iterations = 1000

        fig = plt.figure()
        plt.interactive(False)
        ax = Axes3D(fig)

        sem.acquire()

        def update(iteration):
            try:
                brain_map = next(brain_simulator)
            except StopIteration:
                return

            (xs, ys, zs, cs) = ([e[0] for e in brain_map.keys()],
                                [e[1] for e in brain_map.keys()],
                                [e[2] for e in brain_map.keys()],
                                [str(-(e-0.5)+0.5 if e <= 1 else 1)
                                 for e in brain_map.values()])  # Reflect color along x=0.5

            print("Iteration {}: {} charged".format(iteration, len(brain_map)))

            if True:  # iteration % 1 == 0:
                ax.clear()
                ax.set_xlim3d([0.0, brain_size[0]])
                ax.set_ylim3d([0.0, brain_size[1]])
                ax.set_zlim3d([0.0, brain_size[2]])
                ax.scatter(xs, ys, zs, color=cs, marker='o')

            if iteration == iterations or not len(brain_map):
                sem.release()
                return


        animation = FuncAnimation(fig, update, frames=range(1, iterations+1), interval=10)

        animation.save('./exports/gen{}.gif'.format(generation), dpi=320)  # Subdirectories must exist
        # plt.show(block=True)
        fig = None
        plt.close(fig)
        gc.collect()
