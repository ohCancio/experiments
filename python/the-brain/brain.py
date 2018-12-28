"""Brain simulator, aka 'Glorified Cellular Automaton'

Pro-tip:
    Disconnect all your network adapters to avoid world-wide domination.

Usage:
    The Simulator class implements an iterator for the sequential states of the brain.
    The brain state is represented by a dictionary of charged neurons with keys being 3D positions (tuples)
    and the values being the floating point charge in the interval [0-1]
"""

import random
import gc


class NeuronInfo:
    def __init__(self, power=0.4, probability=0.2, decay=0.15, burn_point=1.5):
        self.power = power
        self.probability = probability
        self.decay = decay
        self.burn_point = burn_point


class Brain:
    def __init__(self, size, neuron_info, initial_state, fixed_positions):
        if not isinstance(size, tuple) and len(size) != 3:
            raise ValueError("Size is not a 3-tuple.")
        self.brain_size = size
        self.brain_map = {}
        self.neuron_info = neuron_info
        self.fixed_positions = fixed_positions
        for e in initial_state:
            self.brain_map[e] = initial_state[e]
        for e in fixed_positions:
            self.brain_map[e] = fixed_positions[e]

    def get_adjacent_positions(self, position):
        if not isinstance(position, tuple) and len(position) != 3:
            raise ValueError("Position is not a 3-tuple.")

        result = []
        for x, y, z in [(position[0] + i, position[1] + j, position[2] + k)
                        for i in (-0, 0, 1) for j in (-0, 0, 1) for k in (-0, 0, 1)
                        if (i == j == 0 or i == k == 0 or j == k == 0) and not i == j == k
                        ]:
            if (0 <= x < self.brain_size[0] and
                    0 <= y < self.brain_size[1] and
                    0 <= z < self.brain_size[2] and
                    (x, y, z) not in self.fixed_positions):  # exclude fixed-positions
                result.append((x, y, z))

        return result

    def fire(self):
        for loc in list(self.brain_map.keys())[:]:

            charge = self.brain_map[loc]
            trigger_adjacent = False

            if charge >= self.neuron_info.burn_point:
                del self.brain_map[loc]
                continue

            if random.randint(0, 101) < 100 * self.neuron_info.probability * charge:
                self.brain_map[loc] = 0
                trigger_adjacent = True

            if trigger_adjacent:
                adjacent_positions = self.get_adjacent_positions(loc)
                for adj in adjacent_positions:
                    if adj in self.brain_map.keys():
                        self.brain_map[adj] += self.neuron_info.power * 6 / len(adjacent_positions)  #self.neuron_info.power
                    else:
                        self.brain_map[adj] = self.neuron_info.power * 6 / len(adjacent_positions)  #self.neuron_info.power

            self.brain_map[loc] -= self.neuron_info.decay

            charge = self.brain_map[loc]
            if charge > 1:
                self.brain_map[loc] = 1
            elif charge <= 0:
                del self.brain_map[loc]

            if loc in self.fixed_positions:
                self.brain_map[loc] = self.fixed_positions[loc]


class BrainSimulator:
    def __init__(self, size=(20, 20, 30), neuron_info=NeuronInfo(), initial_state=[], fixed_positions=[]):
        self.simulated_brain = Brain(size, neuron_info, initial_state, fixed_positions)
        self.step = 0

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.simulated_brain.brain_map) == 0:
            raise StopIteration

        self.simulated_brain.fire()
        self.step += 1
        gc.collect()
        return self.simulated_brain.brain_map
