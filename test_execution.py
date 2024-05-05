from qiskit import QuantumCircuit
from qiskit.quantum_info import StabilizerState
from state.stabilizer import *
from function.function_table import *
from connect_state_function import *
import time
from datetime import datetime
import sys


def test_function(x): return (x[0] and x[1]) ^ (x[1] and x[2])


def main():
    state_name = "GHZ"
    qubits_number = 3
    inputs_number = 3

    qc = QuantumCircuit(qubits_number)
    qc.h(0)
    qc.h(1)
    qc.h(2)
    qc.cz(0, 1)
    qc.cz(0, 2)

    state = StabilizerState(qc)

    stabilizers_eigen_values = find_all_stabilizers(state)
    for stabilizer in stabilizers_eigen_values:
        print(stabilizer, "\t", stabilizers_eigen_values[stabilizer])

    # TODO: check if f.__code__.co_stacksize is really a number of inputs
    function = BooleanFunction(num_args=inputs_number)
    generic_truth_table = function.truth_table
    print("x1\tx2\tx3\tx1^x2\tx1^x3\tx2^x3\tx1^x2^x3\tf")  # TODO: see if there is any other way to do it nicely
    print("\n".join(["\t".join([str(cell) for cell in row]) for row in generic_truth_table]))

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    start = time.time()  # TODO: get rid of time measurement
    functions = brute_force_connect(function, stabilizers_eigen_values, qubits_number)
    end = time.time()
  
    # Save the current stdout so that we can revert sys.stdou after we complete
    # our redirection
    stdout_fileno = sys.stdout
    # Redirect sys.stdout to the file
    file_name = state_name + "_" + str(qubits_number) + "qubits_" + str(inputs_number) + "inputs.txt"
    sys.stdout = open(file_name, 'w')

    results_number = 0
    for function in functions:
        print(function)
        results_number += 1
    print("\nTotal: ", results_number)
    print("Elapsed: ", end - start)

    # Close the file
    sys.stdout.close()
    # Restore sys.stdout to our old saved file handler
    sys.stdout = stdout_fileno

    print("Total: ", results_number)
    print("Elapsed: ", end - start)


if __name__ == '__main__':
    main()
