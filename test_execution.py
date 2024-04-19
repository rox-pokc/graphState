import time

from qiskit import QuantumCircuit
from qiskit.quantum_info import StabilizerState
from state.stabilizer import *
from function.function_table import *
from connect_state_function import *
import multiprocessing
import os


def test_function(x): return (x[0] and x[1]) ^ (x[1] and x[2])


def main():
    qubits_number = 7

    qc = QuantumCircuit(qubits_number)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.cx(0, 3)
    qc.cx(0, 4)
    qc.cx(0, 5)
    qc.cx(0, 6)

    # qubits_number = 7
    #
    # qc = QuantumCircuit(qubits_number)
    # qc.h(0)
    # qc.cx(0, 1)
    # qc.cx(0, 2)
    # qc.cx(0, 3)
    # qc.cx(0, 4)
    # qc.cx(0, 5)
    # qc.cx(0, 6)

    state = StabilizerState(qc)
    print(state)

    stabilizers_eigen_values = find_all_stabilizers(state, False)
    for stabilizer in stabilizers_eigen_values:
        print(stabilizer, "\t", stabilizers_eigen_values[stabilizer])

    # TODO: check if f.__code__.co_stacksize is really a number of inputs
    truth_table = get_truth_table(test_function, test_function.__code__.co_stacksize)
    print("x1\tx2\tx3\tx1^x2\tx1^x3\tx2^x3\tx1^x2^x3\tf")
    print("\n".join(["\t".join([str(cell) for cell in row]) for row in truth_table]))

    print(multiprocessing.cpu_count())
    print(os.cpu_count())

    start = time.time()
    results = brute_force_connect(truth_table, stabilizers_eigen_values, qubits_number)
    end = time.time()
    for result in results:
        if result["is_solution"]:
            print("Combination of columns: ", result["combination"], "\nRules for each column: ",
                  [get_name_compare_choice(item) for item in result["choice"]],
                  "\nComparison order for ev and function outcome: ", result["order"])
    print("Elapsed: ", end - start)


if __name__ == '__main__':
    main()
