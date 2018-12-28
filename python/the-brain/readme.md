# Disclaimer
This is not a real project and only served for me to get acquainted with Python Development. TODO: Parametrize all the insanity described below.

# The Brain

A grandiose attempt at emulating spasmodic neural network behavior using only rudimentary knowledge of what a neuron is and very fresh python skills.
At the moment it is simulating smoke. Fitting.

## Getting Started
The "brain" is just a grid where each position (neuron) can have a charge between 0.0 and 1.0.

There are a few aspects that affect a neuron:
* firing probability - a probability of a neuron firing at a certain iteration is determined by 0.2*current_charge. If it fires it affects all adjacent neurons. If adjancencies are outside of the brain boundaries, the power gets reflected to the mirror adjacencies.
* power - charge a neuron gets incremented when being fired upon by another,
* decay - charge a neuron gets decremented at each iteration of the brain,
* burn out - charge at a neuron is considered burned and loses all charge (it is still usable in later iterations),
* adjacent neurons - neurons that are directly adjacent in 3D (along x, y and z individually; i.e. no diagonals)

The script is generating 20 generations of the brain with 1000 iterations each and dropping the plot into a gif.
Each generation starts with a cube where each position (neuron) is constantly charged and the adjacency calculation has been forced to return only positive movements on the grid. Gives it that smoky taste.

### Prerequisites

Create a folder named "exports" in the same directory as the simulate_brain.py script. Fat gifs will be dropped there.
You must use Python 3 on 64 Bits or else memory goes bye-bye at 2GB. This is a Proof of Concept (concept being "I can learn Python"), therefore not optimized.
Install the matplotlib package on your virtual environment.

### Execution
Run simulate_brain.py.

## Authors

* **Ricardo Silva** - [ohCancio](https://github.com/ohCancio)

## License

This project is licensed under the MIT License.

## Acknowledgments

* Hat tip to João Galego for help on existential aspects of the code.

