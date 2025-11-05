import numpy as np
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator

# --- FUNCTIONS ---

def five_qubits_with_random_Pauli(x1, x2, p):

    # 1) Create register for the 5 qubits
    qr = QuantumRegister(5, "q")
    qcirc = QuantumCircuit(qr)

    # 2) Prepare the logical  |xL>  state based on the given booleans x1, x2. Save the decoded,
    # initialized qubits to retrieve them later.

    if (x1,x2)==(0,0):
        alpha, beta = 1,0
    elif (x1,x2)==(0,1):
        alpha, beta = 0,1
    elif (x1,x2)==(1,0):
        alpha, beta = 1/np.sqrt(2),  1/np.sqrt(2)
    elif (x1,x2)==(1,1):
        alpha, beta = 1/np.sqrt(2), -1/np.sqrt(2)

    θ = 2*np.arccos(np.abs(alpha))
    φ = np.angle(beta) - np.angle(alpha)
    if abs(θ)>1e-12:
        qc.ry(θ, qr[0])
    if abs(φ)>1e-12:
        qc.rz(φ, qr[0])

    qcirc.h(qr[0])
    qcirc.cx(qr[0], qr[2])
    qcirc.cx(qr[2], qr[1])
    qcirc.cx(qr[1], qr[3])
    qcirc.cx(qr[3], qr[4])
    qcirc.cz(qr[0], qr[4])

    dcirc = qcirc.inverse() # decoder for later use
    qcirc.barrier()
    # draw here

    # 3) Add one random Pauli error on each of the  5  qubits with probability  p .

    for i in range(5):
        r = np.random.rand()
        if r < p/3:
            qcirc.x(qr[i])
        elif r < 2*p/3:
            qcirc.y(qr[i])
        elif r < p:
            qcirc.z(qr[i])


    qcirc.barrier()
    # draw here

    # 4) Use stabilizer components to detect errors as syndrome in  4  ancillas.
    ar    = QuantumRegister(4, "a")
    qcirc.add_register(ar)

    P = ['IXZZX',
         'XIXZZ',
         'ZXIXZ',
         'XZZXI']

    for i in range(len(P)):
        qcirc.h(ar[i])
        for j in range(len(P[i])):
            if P[i][j] == 'X':
                qcirc.cx(qr[j], ar[i])
            if P[i][j] == 'Z':
                qcirc.cz(qr[j], ar[i])
        qcirc.h(ar[i])

    # 5) Measure the syndromes as classical bits.
    sy   = ClassicalRegister(4, "s")
    qcirc.add_register(sy)

    qcirc.measure(ar[0], sy[0])
    qcirc.measure(ar[1], sy[1])
    qcirc.measure(ar[2], sy[2])
    qcirc.measure(ar[3], sy[3])

    qcirc.barrier()
    # draw here

    # 6) Correct the error on the qubits based on the detected syndrome

    corrections = {
    # no error
    '0000': ('I', None),

    # qubit 1
    '1110': ('X', 0),
    '0111': ('Y', 0),
    '1001': ('Z', 0),

    # qubit 2
    '1011': ('X', 1),
    '1101': ('Y', 1),
    '0100': ('Z', 1),

    # qubit 3
    '1100': ('X', 2),
    '1010': ('Y', 2),
    '0011': ('Z', 2),

    # qubit 4
    '1000': ('X', 3),
    '1111': ('Y', 3),
    '0110': ('Z', 3),

    # qubit 5
    '0101': ('X', 4),
    '0001': ('Y', 4),
    '1110': ('Z', 4)
    }

    for s_type, (corr, qidx) in corrections.items():
        if corr == 'I':
            continue
        s_int = int(s_type[::-1], 2)
        with qcirc.if_test((sy, s_int)):
            if corr == 'X':
                qcirc.x(qr[qidx])
            elif corr == 'Y':
                qcirc.y(qr[qidx])
            elif corr == 'Z':
                qcirc.z(qr[qidx])

    qcirc.barrier()
    # draw here


    # 7) use the decoder to measure the first single logical qubit.
    qcirc.compose(dcirc, qr, inplace=True)
    mr    = ClassicalRegister(1, "m")   # final logical measurement after decode
    qcirc.add_register(mr)
    qcirc.measure(qr[0], mr[0])

    return qcirc

# --- MAIN ---
# User's choice: define 2 booleans x1, x2
x1, x2 = 0, 0

# Run the circuit 100 times for a wide range of error rates p

simulator = AerSimulator()

sprobs = []

for p in np.linspace(0.0, 1.0, 50):
    successes = 0  # reset once per p
    for attempt in range(100):
        qcirc = five_qubits_with_random_Pauli(x1, x2, p)
        compiled_circuit = transpile(qcirc, simulator)
        job = simulator.run(compiled_circuit, shots=500)
        counts = job.result().get_counts()
        bit_str = max(counts, key=counts.get)
        bit = int(bit_str.replace(" ", ""), 2)

        # logical success condition
        if (x1, x2) == (0, 0) or (x1, x2) == (1, 0):
            if bit == 0:
                successes += 1
        else:
            if bit == 1:
                successes += 1

    sprob = successes / 100
    print(f'error rate = {p:.2f} --> success probability = {sprob:.3f}')
    sprobs.append(sprob)

# Now plot the results: we can clearly observe an exponential decay toward 0, 
# because the higher the error rate, the less likely is the 5-qubit codes to correct it

plt.figure(figsize=(12,7))
plt.plot(np.linspace(0.0, 1.0, 50), sprobs, marker = 'o', linewidth=1.5)
plt.xlabel("error rate p", fontsize=22)
plt.ylabel("success probability", fontsize=22)

ax = plt.gca()
ax.get_xaxis().get_major_formatter().set_useOffset(False)
for tick in ax.xaxis.get_major_ticks():
    tick.label1.set_fontsize(18)
ax.get_yaxis().get_major_formatter().set_useOffset(False)
for tick in ax.yaxis.get_major_ticks():
    tick.label1.set_fontsize(18)
plt.show()
