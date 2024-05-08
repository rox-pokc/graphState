from qiskit import QuantumCircuit
from qiskit.quantum_info import StabilizerState
from state.stabilizer import *
from connect_state_function import *
import time
from datetime import datetime


def main():
    qubits_number = 4

    qc = QuantumCircuit(qubits_number)
    qc.h(0)
    qc.h(1)
    qc.h(2)
    qc.h(3)
    qc.cz(0, 1)
    qc.cz(0, 2)
    qc.cz(0, 3)

    state = StabilizerState(qc)

    stabilizers_eigen_values = find_all_stabilizers(state)
    for stabilizer in stabilizers_eigen_values:
        print(stabilizer, "\t", stabilizers_eigen_values[stabilizer])

    # TODO: check if f.__code__.co_stacksize is really a number of inputs
    function = BooleanFunction(num_args=test_function.__code__.co_stacksize)
    generic_truth_table = function.truth_table
    print("x1\tx2\tx3\tx1^x2\tx1^x3\tx2^x3\tx1^x2^x3\tf")  # TODO: see if there is any other way to do it nicely
    print("\n".join(["\t".join([str(cell) for cell in row]) for row in generic_truth_table]))

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    start = time.time()  # TODO: get rid of time measurement
    search_functions(function, stabilizers_eigen_values, qubits_number)
    end = time.time()

    print("Elapsed: ", end - start)


if __name__ == '__main__':
    main()
