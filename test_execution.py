from qiskit import QuantumCircuit
from qiskit.quantum_info import StabilizerState
from state.stabilizer import *
from function.function_table import *
from connect_state_function import *
import time


def test_function(x): return (x[0] and x[1]) ^ (x[1] and x[2])


def main():
    qubits_number = 4

    qc = QuantumCircuit(qubits_number)
    qc.h(0)
    qc.cx(0, 1)
    qc.cx(0, 2)
    qc.cx(0, 3)

    state = StabilizerState(qc)

    stabilizers_eigen_values = find_all_stabilizers(state)
    for stabilizer in stabilizers_eigen_values:
        print(stabilizer, "\t", stabilizers_eigen_values[stabilizer])

    # TODO: check if f.__code__.co_stacksize is really a number of inputs
    function = BooleanFunction(num_args=test_function.__code__.co_stacksize)
    truth_table = function.from_function_to_truth_table(test_function)
    print("x1\tx2\tx3\tx1^x2\tx1^x3\tx2^x3\tx1^x2^x3\tf")  # TODO: see if there is any other way to do it nicely
    print("\n".join(["\t".join([str(cell) for cell in row]) for row in truth_table]))

    start = time.time()  # TODO: get rid of time measurement
    results = brute_force_connect(truth_table, stabilizers_eigen_values, qubits_number)
    end = time.time()

    no_solutions = 0
    for combination_result in results:
        if len(combination_result) == 0:
            no_solutions += 1
    if no_solutions == len(results):
        print("\nNo solutions")
    else:
        print("\nResults: ")
        results_number = 1
        for combination_results in results:
            for result in combination_results:
                print(results_number, ". Combination of columns: ", result["combination"], "\nRules for each column: ",
                      [get_name_compare_choice(item) for item in result["choice"]],
                      "\nComparison order for ev and function outcome: ", result["order"], "\n")
                results_number += 1

    print("Elapsed: ", end - start)


if __name__ == '__main__':
    main()
