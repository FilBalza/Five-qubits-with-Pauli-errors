# Quantum-Calculator
This repository was created in reference to the mini-project #5 (second batch) of the Quantum Computing Boot Camp sponsored by the [Erdős Institute](https://www.erdosinstitute.org/). 

# The problem
Write a Qiskit function that takes one input: a positive integer $d$ and outputs a quantum circuit, QCalc, on $3d+1$ qubits, possibly with further ancillas, that implements the following:

QCalc $\ket x_d \ket y_d \ket z_1 \ket 0_d \mapsto \ket x_d \ket y_d \ket z_1 \ket{x + y \text{ mod } 2^d}_d$ if $z = 0$; $\ket x_d \ket y_d \ket z_1 \ket{xy \text{ mod } 2^d}_d$ if $z = 1$, 

where we use the numerical labeling on the $d$-qubit computational basis:
$\ket x_1 \ket x_2 \dots \ket x_d$. \
The construction may use any number of ancillas, arbitrary 1-qubit gates, C X, and Toffoli gates. No classical
bit and measurements allowed.


## Strategy implemented
This implementation follows a logic similar to Draper’s adder, which performs arithmetic in the Fourier (phase) basis rather than in the computational (binary) basis used by classical or integer adders. Draper’s adder leverages the Quantum Fourier Transform (both forward and inverse) to encode integer values as phases, transforming a computational basis state as

$\text{QFT}\ket x \mapsto \frac{1}{2^{d/2}} \sum_{k=0}^{2^d-1} e^{2\pi i xk / 2^d} \ket k$

Hence, addition by a constant corresponds to a simple phase rotation that can be implemented through a sequence of controlled phase gates. Finally, the inverse QFT needs to be applied to return the result to the computational basis. Since phase shifts naturally add modulo $2^d$, the desired modular reductions are intrinsically handled throughout the circuit. 

In its standard formulation, Draper's adder acts as $D_k \ket T \mapsto \ket{k + T \text{ mod } 2^d}$,  where $k \in \mathbb{Z}$ is a specified integer and and $\ket T$ is a quantum register of $d$ qubits representing an integer in binary form. To tackle the proposed problem, a "quantum" Draper's adder was implemented instead. The idea is to replace the constant $k$ with another quantum register $\ket x$, thus performing the transformation $D_{\ket X} \ket T \mapsto \ket{X + T \text{ mod } 2^d}$. This is possible by exploiting linearity of phase: the QFT of $\ket T$ encodes $T$ into phases $∝ T$, and a controlled phase by a qubit $\ket X_i$ of weight $2^i$ contributes exactly the phase needed to add $2^i$ to $T$ when that control is $\ket 1$. 

In terms of operations in the proposed quantum circuit, each control cubit $X_i$ (bit value of $0$ or $1$) issues a family of controlled-phase gates onto the qubits of the $T$ (always initialized at $T = \ket 0_d$) register with angles scaled by $2^i$ and by the significance of the target qubit. Summing those contributions over all $i$ values produces the coherent addition of the quantum register $X$ into $T$. The same logic then applies simultaneously to $Y$. Hence, for the additive case of $z=0$, adding both $X$ and $Y$ is achieved by applying the controlled phases from both registers, since phase rotations commute and add linearly. \
Multiplication of $X$ by $Y$ (case $z=1$) can be written as the sum of shifted multiples of $X$:

$X \cdot Y = \sum_{j=0}^{d-1}Y_j(X\cdot 2^j)$,

where $Y_j \in {0, 1}$ are the individual bits of $Y$. Thus, the modular product is constructed by performing, for each bit $j$, a controlled addition of $X\cdot 2^j$ into the target $T$ (again, always initialized at $T = \ket 0_d$), conditioned on $Y_j=1$. In terms of Fourier space, this translates into phase rotations: for each pair of bits $X_i$ and $Y_j$, the appropriate phase contribution to the target qubit is proportional to $2^{i+j}$. To implement this multi-controlled phase gate, each two-controlled phase gate gets decomposed  into primitives $cp$ and $cx$ using the standard identity of three single-control phase gates plus two $cx$ gates with half-angles:

$\text{mcp}(\theta, c_1, c_2, T) = \text{cp}(\theta/2, c_1, T)\text{cx}(c_2,c1)\text{cp}(-\theta/2, c_1, T)\text{cx}(c_2,c_1)\text{cp}(\theta/2, c_2, T)$, with $\theta = 2\pi/2^{i+j}$,

which yields the desired conditional phase only when both controls $\ket X_i$ and $\ket Y_i$ are $\ket 1$.

## Analysis of complexity
The QFT/IQFT operations require $O(d^2)$ $2$-qubit controlled-phase (CP) gates, since every qubit is entangled with all subsequent qubits. In case of addition ($z=0$), each pair of bits $(x_i, t_i)$ and $(y_i, t_i)$ contributes one CP gate whenever $i + j < d$, hence leading to approximately $d*(d-1)/2 = O(d^2)$ more operations. In the multiplication branch ($z=1$), each pair of indices $(i, j)$ triggers a sequence of $2$ CX and $3$ CP gates, hence yelding a total count of about $5 d^2 = O(d^2)$. Therefore, the total gate count of the Quantum Calculator scales as $O(d^2)$, e.g. the same order as the underlying QFT/IQFT routines. Since all phase rotations are being applied sequentially, the gate depth also scales as $O(d^2)$. 

Unlike other operations (e.g. Toffoli-based adders or multipliers), this implementation does not employ any ancilla qubits. This is because the implemented quantum Draper’s adder operates directly in the Fourier basis, where addition corresponds to the application of phase shifts proportional to the binary digits of the addends. Hence, this phase-encoding strategy eliminates the need to explicitly propagate carries or temporary sums, which are the main sources of ancilla overhead in integer (binary) adders. The same logic extends to the multiplicative case: by combining controlled-phase operations and reversible CX gates, the circuit effectively performs modular multiplication without allocating extra workspace beyond the required registers $(X, Y, z, T)$.


# Repository content
In the $scripts$ folder, there are 2 Python scripts:
1. **quantum-calculator.py** $\to$ This script contains custom implementations of the Quantum Fourier Transform (QFT), its inverse (IQFT), and of the Quantum Calculator (QCalc) following the described strategy.
2. **run_test.py** $\to$ This script allows to run customizable tests on the Quantum Calculator. The user needs to prompt the dimension $d$ (any positive integer), the value of $z$ (0 or 1), and the verbosity (0 or 1). If verbosity is 1, the final states (both arithmetically and quantum computed) are printed. Be aware that the order of the arithmetic output may differ from Qiskit's ordering.

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

## Examples

# Resources used
(1) L. Finotti, [Notes on Quantum Computing](https://github.com/lrfinotti/qc_notes/blob/main/quantum.pdf), 2025\
(2) M. A. Nielsen and I. L. Chuang, [Computation and Quantum Information](https://profmcruz.wordpress.com/wp-content/uploads/2017/08/quantum-computation-and-quantum-information-nielsen-chuang.pdf), 2010\
(3) T. G. Draper, [Addition on a Quantum Computer](https://arxiv.org/abs/quant-ph/0008033), 2000

ChatGPT was used to better understand concepts, correct grammar, help analyze the complexity in the "big-O" sense and polish the code improving interpretability.

# Acknowledgments
The author thanks Ákos Nagy for the inspiring lectures and Cindy Zhang for the insightful practice sessions.
