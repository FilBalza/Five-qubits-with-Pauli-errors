# Five-Qubit Code Under Random Pauli Error
This repository was created in reference to the mini-project #5 (second batch) of the Quantum Computing Boot Camp sponsored by the [Erdős Institute](https://www.erdosinstitute.org/). 

# The problem
Write a Qiskit function that takes the following inputs:
(1) A pair of Booleans, $x \in \mathbb{F}_2$
(2) An error probability $p$

The output of the function is a quantum circuit that prepares (not necessearily fault tolerantly) the logical state, $\ket{x_L}$, for the $5$-qubit code, runs it through a random Pauli error channel, with error rate $p$ (for each qubit), measures syndromes, applies the recovery operations (if needed), and measures the data qubits.\
The success probability is the probability that you measure a component of $\ket{x_L}$ at the end. Visualize the dependence of the success probability for various values of $p$.

You can use built-in initial state preparation methods or prepare the logical sate, $\ket{x_L}$ (or do it "by hand" using elementary gates). Beyond that, you may only use Clifford gates, measurements, and classically controlled Pauli operations.


## Strategy implemented
The approach to tackle the problem is divided in some subsequent steps.

### 1. Logical state preparation
The logical qubit $\ket{x_L}$ encodes one logical qubit into five physical ones. The two (user-defined) Boolean values, $x_1$ and $x_2$, determine which logical state is prepared:\
$(0, 0) \to \ket{0_L}$\
$(0, 1) \to \ket{1_L}$\
$(1, 0) \to \ket{+_L} = (\ket{0_L} + \ket{1_L})/\sqrt{2} $\
$(1, 0) \to \ket{-_L} = (\ket{0_L} - \ket{1_L})/\sqrt{2}$

First, the desired single-qubit state $\alpha \ket{0} + \beta \ket{1}$ is prepared using rotations $R_y(\theta)$ and $R_z(\varphi)$, where $\alpha = cos(\theta/2)$ and $\beta = e^{i\varphi}sin(\theta/2)$. Then, a sequence of $H$, $CX$, and $CZ$ gates spreads this information across all five data qubits. This entangling pattern encodes the state into the protected subspace stabilized by the generators of the [[5,1,3]] code. The resulting five-qubit superposition obeys all stabilizer constraints and represents one logical qubit protected against any single-qubit Pauli error.

### 2. Error model
Each of the five qubits is independently subjected to a random Pauli error ($X$, $Y$, or $Z$) with total probability $p$. This step stochastically simulates noise acting on the encoded state, allowing the code’s correction performance to be studied as a function of $p$.

### 3. Syndrome extraction
Four ancilla qubits are added to measure the four stabilizer generators:\
$S_1 = IXZZX$\
$S_2 = XIXZZ$\
$S_3 = ZXIXZ$\
$S_4 = XZZXI$

For each stabilizer $S_i$, the circuit uses $H-CX-CZ-H$ blocks to entangle the ancilla with the data qubits according to the pattern of $X$ and $Z$ operators. Measuring the ancillas yields a $4$-bit syndrome, which is stored in a classical register to identify which physical qubit (if any) experienced an error.

### 4 Conditional error correction
Each syndrome pattern maps uniquely to a Pauli correction ($X$, $Y$, or $Z$) on one of the five data qubits. A dictionary of corrections implements this mapping, and Qiskit’s "if_test()" control structure applies the corresponding correction only when the measured syndrome matches the dictionary key.

### 5 Decoding and measurement
After correction, the encoded state must be decoded back into a single qubit to verify success. Instead of defining a separate decoder, the script simply inverts the encoding circuit right after the logical state's preparation. The logical information is thus recovered in the first physical qubit, which is the original qubit where the logical state was initialized and is then measured. Note that measuring other qubits would not reflect the decoded logical state because they return to the $\ket{0}$ state after decoding.

### Success-probability estimation
For each error rate $p$, the quantum circuit is run $100$ times with $500$ measurement shots per run. The most frequent measurement result is taken as the logical output bit.\
A run is counted as "successful" if the decoded measurement matches the expected logical bit: $0$ for $\ket{0_L}$ or $\ket{+_L}$, $1$ for $\ket{1_L}$ or $\ket{-_l}$. The success probability is then the ratio of successful runs to total runs, and can be plotted.


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
