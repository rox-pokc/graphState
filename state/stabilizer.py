from qiskit.quantum_info import Pauli
import itertools


def get_all_stabilizers(qubits_number):
    permutations = set("".join(i) for i in list(itertools.product(["I", "X", "Z", "Y"], repeat=qubits_number)))
    return permutations


def find_all_stabilizers(state):
    all_stabilizers = get_all_stabilizers(state.num_qubits)
    eigen_values = {}
    plus_stabilizers = set()
    minus_stabilizers = set()
    for stabilizer in all_stabilizers:
        ev = state.expectation_value(Pauli(stabilizer))
        if ev == 1 or ev == -1:
            eigen_values[stabilizer] = ev
            if ev == 1:
                plus_stabilizers.add(stabilizer)
            else:
                if ev == -1:
                    minus_stabilizers.add(stabilizer)
    print("+1: ", plus_stabilizers)     # TODO: mb get rid of printing
    print("+1 amount: ", len(plus_stabilizers))
    print("-1: ", minus_stabilizers)
    print("-1 amount: ", len(minus_stabilizers))

    return eigen_values

