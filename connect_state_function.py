from qiskit import QuantumCircuit
from qiskit.quantum_info import StabilizerState
from state.stabilizer import *
from function.function_table import *
import itertools


def test_function(x): return (x[0] and x[1]) ^ (x[1] and x[2])


COMPARE_CHOICES = {
    'direct': 0,
    'reverse': 1
}


def transform_input(input, choice):
    if choice == COMPARE_CHOICES['direct']:
        if input == 0:
            return "X"
        else:
            return "Y"
    elif choice == COMPARE_CHOICES['reverse']:
        if input == 0:
            return "Y"
        else:
            return "X"


def compare(function_outcome, ev, order):
    if order == 'direct':
        if (function_outcome == 0 and ev == 1) or (function_outcome == 1 and ev == -1):
            return True
        return False
    elif order == 'reverse':
        if (function_outcome == 0 and ev == -1) or (function_outcome == 1 and ev == 1):
            return True
        return False


def brute_force_connect(truth_table, stabilizers_eigen_values, qubits_number):
    combinations = list(itertools.combinations(list(range(len(truth_table[0]) - 1)), qubits_number))
    for combination in combinations:
        for order in COMPARE_CHOICES:
            for i in range(pow(2, qubits_number)):
                choices = [int(x) for x in ("{0:0" + str(qubits_number) + "b}").format(i)]
                found = True
                for row in range(len(truth_table)):
                    table_row_stabilizer = ''
                    for column in combination:
                        table_row_stabilizer += transform_input(truth_table[row][column],
                                                                choices[combination.index(column)])
                    if not ((table_row_stabilizer in stabilizers_eigen_values) and
                            (compare(truth_table[row][len(truth_table[row]) - 1],
                                     stabilizers_eigen_values[table_row_stabilizer],
                                     order))):
                        found = False
                        break
                if found:
                    return combination, choices, order
    raise Exception("No solution found!")


qubits_number = 4

qc = QuantumCircuit(qubits_number)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)
qc.cx(0, 3)

state = StabilizerState(qc)

stabilizers_eigen_values = find_all_stabilizers(state, qubits_number)
for stabilizer in stabilizers_eigen_values:
    print(stabilizer, "\t", stabilizers_eigen_values[stabilizer])

# TODO: check if f.__code__.co_stacksize is really a number of inputs
truth_table = get_truth_table(test_function, test_function.__code__.co_stacksize)
print('x1\tx2\tx3\tx1^x2\tx1^x3\tx2^x3\tx1^x2^x3\tf')
print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in truth_table]))

combination, choices, order = brute_force_connect(truth_table, stabilizers_eigen_values, qubits_number)
print(combination, choices, order)