import pennylane as qml
from pennylane import numpy as np

# Function to encode a DNA base to a qubit state
def encode_dna_base(base):
    """
    Encodes a DNA base (A, T, C, or G) into a qubit state represented by a list of 0s and 1s.

    Args:
        base (str): A single-character string representing a DNA base (A, T, C, or G).

    Returns:
        list: A list of two integers (0 or 1) representing the qubit state encoding of the DNA base.
            - [0, 0] for 'A'
            - [1, 1] for 'T'
            - [0, 1] for 'C'
            - [1, 0] for 'G'
    """
    if base == "A":
        return [0, 0]
    elif base == "T":
        return [1, 1]
    elif base == "C":
        return [0, 1]
    elif base == "G":
        return [1, 0]

# Define a device
num_bases = 4  # This is the length of the DNA sequences
dev = qml.device('default.qubit', wires=2 * num_bases * 2 + num_bases)  # Each base uses 2 qubits, plus one ancilla per base

# Function to encode a sequence of DNA bases to qubit states
def encode_dna_sequence(sequence):
    """
    Encodes a sequence of DNA bases into a list of qubit states.

    Args:
        sequence (list): A list of single-character strings representing DNA bases (A, T, C, or G).

    Returns:
        list: A list of lists, where each inner list represents the qubit state encoding of a DNA base in the sequence.
    """
    return [encode_dna_base(base) for base in sequence]

@qml.qnode(dev)
def dna_sequence_compare_circuit(ref_sequence, read_sequence):
    """
    Quantum circuit to compare a reference DNA sequence with a read sequence.

    Args:
        ref_sequence (list): A list of single-character strings representing the reference DNA sequence.
        read_sequence (list): A list of single-character strings representing the read DNA sequence.

    Returns:
        list: A list of floating-point values representing the expectation values of the ancilla qubits.
              A value close to -1 indicates a difference between the reference and read sequences at that position.
              A value close to 1 indicates a match between the reference and read sequences at that position.
    """
    ref_encoded = encode_dna_sequence(ref_sequence)
    read_encoded = encode_dna_sequence(read_sequence)

    # Initialize the qubits based on DNA base encoding
    for i in range(num_bases):
        # Set the qubits for the reference base
        if ref_encoded[i][0] == 1:
            qml.PauliX(wires=i * 2)
        if ref_encoded[i][1] == 1:
            qml.PauliX(wires=i * 2 + 1)

        # Set the qubits for the read base
        if read_encoded[i][0] == 1:
            qml.PauliX(wires=num_bases * 2 + i * 2)
        if read_encoded[i][1] == 1:
            qml.PauliX(wires=num_bases * 2 + i * 2 + 1)

        # Apply CNOT gates for comparison
        qml.CNOT(wires=[i * 2, num_bases * 2 + i * 2])
        qml.CNOT(wires=[i * 2 + 1, num_bases * 2 + i * 2 + 1])

        # Use Toffoli to set the ancilla
        qml.Toffoli(wires=[num_bases * 2 + i * 2, num_bases * 2 + i * 2 + 1, 2 * num_bases * 2 + i])

    # Measure the ancilla qubits
    return [qml.expval(qml.PauliZ(i)) for i in range(2 * num_bases * 2, 2 * num_bases * 2 + num_bases)]

# Example DNA sequences
ref_sequences = [["A", "T", "G", "C"], ["A", "C", "G", "T"], ["T", "G", "C", "A"], ["A", "T", "G", "C"],
                 ["C", "G", "T", "A"], ["T", "C", "G", "A"], ["A", "G", "T", "C"]]
read_sequences = ["A", "T", "G", "C"]

print("now we're returning")

# Execute the circuit
comparison_results = []
for i in range(len(ref_sequences)):
    ref_sequence = ref_sequences[i]
    read_sequence = read_sequences
    comparison_results.append(dna_sequence_compare_circuit(ref_sequence, read_sequence))

total_diff = []
index = 0
final_data = [element for innerList in comparison_results for element in innerList]
print("Comparison results:")
for i in final_data:
    index += 1
    print(i)
    if i < 0:
        total_diff.append(index)

print("You should insert the read sequence at", total_diff)
