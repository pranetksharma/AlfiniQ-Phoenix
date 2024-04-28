import pennylane as qml
from math import ceil, log2

def QPM():
    """
    The main function that runs the Quantum Pattern Matching algorithm.
    """
    A = 4
    N = 8  # Reference Genome size
    w = "01233210"  # randStr(2,N) # Reference Genome
    M = 2  # Short Read size
    p = "10"  # randStr(2,M) # Short Read
    s = ceil(log2(N - M))
    print(s)
    total_qubits = 2 * s * M - 2

    dev = qml.device('default.qubit', wires=total_qubits)

    @qml.qnode(dev)
    def circuit():
        """
        The quantum circuit that implements the Quantum Pattern Matching algorithm.

        Returns:
            list: The probabilities of the qubit states.
        """
        Circ1(qml.wires, s, M)
        fa = []
        fc = []
        fg = []
        ft = []
        for wi in range(N):
            if w[wi] == '0':
                fa.append(True)
                fc.append(False)
                fg.append(False)
                ft.append(False)
            elif w[wi] == '1':
                fa.append(False)
                fc.append(True)
                fg.append(False)
                ft.append(False)
            elif w[wi] == '2':
                fa.append(False)
                fc.append(False)
                fg.append(True)
                ft.append(False)
            else:
                fa.append(False)
                fc.append(False)
                fg.append(False)
                ft.append(True)
        print(f"Reference Genome: {w}")
        print(f"Short Read: {p}")
        match_idx = w.find(p)
        if match_idx != -1:
            print(f"The short read '{p}' appears in the reference genome at index {match_idx}")
        else:
            print(f"The short read '{p}' does not appear in the reference genome")
        for pi in range(M):
            if p[pi] == '0':
                Circ2(qml.wires, fa, s, pi * s, s * M)
            elif p[pi] == '1':
                Circ2(qml.wires, fc, s, pi * s, s * M)
            elif p[pi] == '2':
                Circ2(qml.wires, fg, s, pi * s, s * M)
            else:
                Circ2(qml.wires, ft, s, pi * s, s * M)
        Circ3(qml.wires, s, M)
        return qml.probs(wires=range(total_qubits))

    circuit()

def Circ1(qubits, s, M):
    """
    Initializes the quantum circuit with the reference genome.

    Args:
        qubits (list): A list of qubits.
        s (int): The number of qubits required to represent the reference genome.
        M (int): The length of the short read.
    """
    for Qi in range((s + 1) * M):
        qml.PauliX(wires=Qi)
    for si in range(s):
        qml.Hadamard(wires=si)
    for Mi in range(M - 1):
        for si in range(s):
            qml.CNOT(wires=[Mi * s + si, Mi * s + s + si])
        for si in range(s):
            qml.PauliX(wires=Mi * s + s - 1 - si)
            nc = [Mi * s + s - 1 - sj for sj in range(si + 1)]
            nc.extend([Mi * s + s + s - 1 - sj for sj in range(si + 1)])
            qml.MultiControlledX(control_wires=nc, wires=s * M)
            qml.PauliX(wires=Mi * s + s - 1 - si)

def Circ2(qubits, f, s, q, anc):
    """
    Implements the oracle kernel for the Quantum Pattern Matching algorithm.

    Args:
        qubits (list): A list of qubits.
        f (list): A list representing the reference genome.
        s (int): The number of qubits required to represent the reference genome.
        q (int): The starting qubit for the short read.
        anc (int): The number of ancilla qubits.
    """
    for fi in range(len(f)):
        if f[fi]:
            fis = format(fi, '0' + str(s) + 'b')
            for fisi in range(s):
                if fis[fisi] == '0':
                    qml.PauliX(wires=q + fisi)
            qml.Hadamard(wires=q + s - 1)
            nc = [q + sj for sj in range(s - 1)]
            qml.MultiControlledX(control_wires=nc, wires=q + s - 1)
            qml.Hadamard(wires=q + s - 1)
            for fisi in range(s):
                if fis[fisi] == '0':
                    qml.PauliX(wires=q + fisi)

def Circ3(qubits, s, M):
    """
    Implements the Grover Amplitude Amplification for the Quantum Pattern Matching algorithm.

    Args:
        qubits (list): A list of qubits.
        s (int): The number of qubits required to represent the reference genome.
        M (int): The length of the short read.
    """
    for si in range(s * M):
        qml.Hadamard(wires=si)
        qml.PauliX(wires=si)
    qml.Hadamard(wires=s * M - 1)
    nc = [sj for sj in range(s * M - 1)]
    qml.MultiControlledX(control_wires=nc, wires=s * M)
    qml.Hadamard(wires=s * M - 1)
    for si in range(s * M):
        qml.PauliX(wires=si)
        qml.Hadamard(wires=si)

if __name__ == '__main__':
    QPM()
