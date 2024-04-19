from qiskit import QuantumCircuit
from qiskit.quantum_info import StabilizerState
from state.stabilizer import *
from function.function_table import *
import itertools


def test_function(x): return (x[0] and x[1]) ^ (x[1] and x[2])


EV_COMPARE_CHOICES = {
    'direct': 0,
    'reverse': 1
}

INPUT_COMPARE_CHOICES = {
    'II': 0,
    'IX': 1,
    'IY': 2,
    'IZ': 3,
    'XI': 4,
    'XX': 5,
    'XY': 6,
    'XZ': 7,
    'YI': 8,
    'YX': 9,
    'YY': 10,
    'YZ': 11,
    'ZI': 12,
    'ZX': 13,
    'ZY': 14,
    'ZZ': 15
}


def get_name_compare_choice(number):
    return [name for name, value in INPUT_COMPARE_CHOICES.items() if value == number][0]


def transform_input(input, choice):
    if choice == INPUT_COMPARE_CHOICES['II']:
        return "I"
    elif choice == INPUT_COMPARE_CHOICES['IX']:
        if input == 0:
            return "I"
        else:
            return "X"
    elif choice == INPUT_COMPARE_CHOICES['IY']:
        if input == 0:
            return "I"
        else:
            return "Y"
    elif choice == INPUT_COMPARE_CHOICES['IZ']:
        if input == 0:
            return "I"
        else:
            return "Z"
    elif choice == INPUT_COMPARE_CHOICES['XI']:
        if input == 0:
            return "X"
        else:
            return "I"
    elif choice == INPUT_COMPARE_CHOICES['XX']:
        return "X"
    elif choice == INPUT_COMPARE_CHOICES['XY']:
        if input == 0:
            return "X"
        else:
            return "Y"
    elif choice == INPUT_COMPARE_CHOICES['XZ']:
        if input == 0:
            return "X"
        else:
            return "Z"
    elif choice == INPUT_COMPARE_CHOICES['YI']:
        if input == 0:
            return "Y"
        else:
            return "I"
    elif choice == INPUT_COMPARE_CHOICES['YX']:
        if input == 0:
            return "Y"
        else:
            return "X"
    elif choice == INPUT_COMPARE_CHOICES['YY']:
        return "Y"
    elif choice == INPUT_COMPARE_CHOICES['YZ']:
        if input == 0:
            return "Y"
        else:
            return "Z"
    elif choice == INPUT_COMPARE_CHOICES['ZI']:
        if input == 0:
            return "Z"
        else:
            return "I"
    elif choice == INPUT_COMPARE_CHOICES['ZX']:
        if input == 0:
            return "Z"
        else:
            return "X"
    elif choice == INPUT_COMPARE_CHOICES['ZY']:
        if input == 0:
            return "Z"
        else:
            return "Y"
    elif choice == INPUT_COMPARE_CHOICES['ZZ']:
        return "Z"


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
    choices = list(itertools.product(range(16), repeat=qubits_number))
    for combination in combinations:
        for order in EV_COMPARE_CHOICES:
            for choice in choices:
                found = True
                for row in range(len(truth_table)):
                    table_row_stabilizer = ''
                    for column in combination:
                        table_row_stabilizer += transform_input(truth_table[row][column],
                                                                choice[combination.index(column)])
                    if not ((table_row_stabilizer in stabilizers_eigen_values) and
                            (compare(truth_table[row][len(truth_table[row]) - 1],
                                     stabilizers_eigen_values[table_row_stabilizer],
                                     order))):
                        found = False
                        break
                if found:
                    return combination, choice, order
    raise Exception("No solution found!")


# qubits_number = 4
#
# qc = QuantumCircuit(qubits_number)
# qc.h(0)
# qc.cx(0, 1)
# qc.cx(0, 2)
# qc.cx(0, 3)

qubits_number = 7

qc = QuantumCircuit(qubits_number)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)
qc.cx(0, 3)
qc.cx(0, 4)
qc.cx(0, 5)
qc.cx(0, 6)

state = StabilizerState(qc)
print(state)

stabilizers_eigen_values = find_all_stabilizers(state, False)
for stabilizer in stabilizers_eigen_values:
    print(stabilizer, "\t", stabilizers_eigen_values[stabilizer])

# TODO: check if f.__code__.co_stacksize is really a number of inputs
truth_table = get_truth_table(test_function, test_function.__code__.co_stacksize)
print('x1\tx2\tx3\tx1^x2\tx1^x3\tx2^x3\tx1^x2^x3\tf')
print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in truth_table]))

combination, choice, order = brute_force_connect(truth_table, stabilizers_eigen_values, qubits_number)
print("Combination of columns: ", combination, "\nRules for each column: ",
      [get_name_compare_choice(item) for item in choice], "\nComparison order for ev and function outcome: ", order)
