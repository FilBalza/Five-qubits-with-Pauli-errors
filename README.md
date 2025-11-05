# Five-Qubit Code Under Random Pauli Error
This repository was created in reference to the mini-project #5 (second batch) of the Quantum Computing Boot Camp sponsored by the [Erdős Institute](https://www.erdosinstitute.org/). 

# The problem
Write a Qiskit function that takes the following inputs:
(1) A pair of Booleans, $x \in \mathbb{F}_2$
(2) An error probability $p$

The output of the function is a quantum circuit that prepares (not necessearily fault tolerantly) the logical state, $\ket{x_L}$, for the $5$-qubit code, runs it through a random Pauli error channel, with error rate $p$ (for each qubit), measures syndromes, applies the recovery operations (if needed), and measures the data qubits. 
The success probability is the probability that you measure a component of $\ket{x_L}$ at the end. Visualize the dependence of the success probability for various values of $p$.

You can use built-in initial state preparation methods or prepare the logical sate, $\ket{x_L}$ (or do it "by hand" using elementary gates). Beyond that, you may only use Clifford gates, measurements, and classically controlled Pauli operations.


## Strategy implemented

## Comments on the results



# Repository content
In the $scripts$ folder, there are 2 Jupyter Notebooks and 1 Python script:
1. **stepwise_circuit.ipynb** $\to$ This script contains a step-by-step implementation of the described strategy, with the possibility at the end to check if the quantum circuit was able to correct the random Pauli errors. The user can decide the values of $x_1$, $x_2$, and $p$.
2. **plot_p_dependence.ipynb** $\to$ This script contains the "stepwise_circuit" implementation inside a function and runs it $100$ times for each error rate $p$ sampled uniformely $50$ times in $[0, 1]$. At the end, it prints the corresponding success probability and plots the dependence w.r.t the various values of $p$. The user can decide the values of $x_1$ and $x_2$.
3. **plot_p_dependence.py** $\to$ This script is a standalone version of the "plot_p_dependence" Jupyter notebook, intended for users who prefer running the code as a standard Python script.

## Installing Dependencies
This project requires some Python packages to run. The user can install them using one of the two following options:

**1. Using pip**\
[pip](https://pypi.org/project/pip/) is the package installer for Python. To install the dependencies with pip, the user should run:
```bash
pip install .
```

**2. Using conda**\
[Conda](https://anaconda.org/anaconda/conda) is an open source package management system and environment management system for installing multiple versions of software packages and their dependencies and switching easily between them. To install the dependencies with conda, the user should run:
```bash
conda env create -f environment.yml
```

**3. Using Pixi**\
[Pixi](https://pixi.sh/latest/) is a fast, modern, and reproducible package management tool for developers of all backgrounds. To install the dependencies in your Pixi environment, the user should run:
```bash
pixi install
```

# Resources used
(1) L. Finotti, [Notes on Quantum Computing](https://github.com/lrfinotti/qc_notes/blob/main/quantum.pdf), 2025\
(2) Wikipedia, [Five-qubit error correcting code](https://en.wikipedia.org/wiki/Five-qubit_error_correcting_code)\
(2) M. A. Nielsen and I. L. Chuang, [Computation and Quantum Information](https://profmcruz.wordpress.com/wp-content/uploads/2017/08/quantum-computation-and-quantum-information-nielsen-chuang.pdf), 2010\
(3) R. Laflamme, C. Miquel, J. P. Paz and W. H. Zurek, [Perfect Quantum Error Correcting Code](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.77.198), 1996

ChatGPT was used to better understand concepts, correct grammar, help preparing the logical state $\ket x_L$ and polish the code improving interpretability.

# Acknowledgments
The author thanks Ákos Nagy for the inspiring lectures and Cindy Zhang for the insightful practice sessions.
