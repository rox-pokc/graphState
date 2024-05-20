from qiskit import QuantumCircuit
from qiskit.quantum_info import StabilizerState
from state.stabilizer import *
from function.function_table import *
from connect_state_function import *
import time


def test_function(x): return x[0] & x[1] ^ x[0] & x[2] ^ x[1] & x[2]


def main():
    qubits_number = 5

    qc = QuantumCircuit(qubits_number)
    qc.h(0)
    qc.h(1)
    qc.h(2)
    qc.h(3)
    qc.h(4)
    qc.cz(0, 1)
    qc.cz(0, 2)
    qc.cz(0, 3)
    qc.cz(0, 4)

    state = StabilizerState(qc)

    stabilizers_eigen_values = find_all_stabilizers(state)
    for stabilizer in stabilizers_eigen_values:
        print(stabilizer, "\t", stabilizers_eigen_values[stabilizer])

    function = BooleanFunction(num_args=3)
    truth_table = function.from_function_to_truth_table(test_function)
    print("x1\tx2\tx3\tx1^x2\tx1^x3\tx2^x3\tx1^x2^x3\tf")  # TODO: see if there is any other way to do it nicely
    print("\n".join(["\t".join([str(cell) for cell in row]) for row in truth_table]))

    start = time.time()  # TODO: get rid of time measurement
    results = brute_force_connect(truth_table, stabilizers_eigen_values, qubits_number)
    end = time.time()

    results = filter(lambda x: len(x["combination"]) != 0, results)
    results = sorted(results, key=lambda x: x["combination"])
    for result in results:
        print(result)
    print("Total amount: ", len(results))

    print("Elapsed: ", end - start)


if __name__ == '__main__':
    main()
