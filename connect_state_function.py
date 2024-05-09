import itertools
import multiprocessing
import functools

EV_COMPARE_CHOICES = {
    "direct": 0,
    "reverse": 1
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
        return 'I'
    elif choice == INPUT_COMPARE_CHOICES['IX']:
        if input == 0:
            return 'I'
        else:
            return 'X'
    elif choice == INPUT_COMPARE_CHOICES['IY']:
        if input == 0:
            return 'I'
        else:
            return 'Y'
    elif choice == INPUT_COMPARE_CHOICES['IZ']:
        if input == 0:
            return 'I'
        else:
            return 'Z'
    elif choice == INPUT_COMPARE_CHOICES['XI']:
        if input == 0:
            return 'X'
        else:
            return 'I'
    elif choice == INPUT_COMPARE_CHOICES['XX']:
        return 'X'
    elif choice == INPUT_COMPARE_CHOICES['XY']:
        if input == 0:
            return 'X'
        else:
            return 'Y'
    elif choice == INPUT_COMPARE_CHOICES['XZ']:
        if input == 0:
            return 'X'
        else:
            return 'Z'
    elif choice == INPUT_COMPARE_CHOICES['YI']:
        if input == 0:
            return 'Y'
        else:
            return 'I'
    elif choice == INPUT_COMPARE_CHOICES['YX']:
        if input == 0:
            return 'Y'
        else:
            return 'X'
    elif choice == INPUT_COMPARE_CHOICES['YY']:
        return 'Y'
    elif choice == INPUT_COMPARE_CHOICES['YZ']:
        if input == 0:
            return 'Y'
        else:
            return 'Z'
    elif choice == INPUT_COMPARE_CHOICES['ZI']:
        if input == 0:
            return 'Z'
        else:
            return 'I'
    elif choice == INPUT_COMPARE_CHOICES['ZX']:
        if input == 0:
            return 'Z'
        else:
            return 'X'
    elif choice == INPUT_COMPARE_CHOICES['ZY']:
        if input == 0:
            return 'Z'
        else:
            return 'Y'
    elif choice == INPUT_COMPARE_CHOICES['ZZ']:
        return 'Z'


def compare(function_outcome, ev, order):
    if order == "direct":
        if (function_outcome == 0 and ev == 1) or (function_outcome == 1 and ev == -1):
            return True
        return False
    elif order == "reverse":
        if (function_outcome == 0 and ev == -1) or (function_outcome == 1 and ev == 1):
            return True
        return False


def combination_processing(combination, function, stabilizers_eigen_values, qubits_number):
    truth_table = function.truth_table
    results = set()
    for choice in itertools.product(range(len(INPUT_COMPARE_CHOICES)), repeat=qubits_number):
        found = True
        suitable_stabilizers = []
        for row in range(len(truth_table)):
            table_row_stabilizer = ""
            for column in combination:
                table_row_stabilizer += transform_input(truth_table[row][column],
                                                        choice[combination.index(column)])
            suitable_stabilizers.append(table_row_stabilizer)
            if not (table_row_stabilizer in stabilizers_eigen_values):
                found = False
                suitable_stabilizers.clear()
                break
        if found:
            outputs = []
            for stabilizer in suitable_stabilizers:
                if stabilizers_eigen_values[stabilizer] == 1:
                    outputs.append(0)
                else:
                    outputs.append(1)
            results.add(function.from_output_to_function(outputs))
            outputs.clear()
            for stabilizer in suitable_stabilizers:
                if stabilizers_eigen_values[stabilizer] == 1:
                    outputs.append(1)
                else:
                    outputs.append(0)
            results.add(function.from_output_to_function(outputs))
    return results


def brute_force_connect(function, stabilizers_eigen_values, qubits_number):
    with multiprocessing.Pool() as pool:
        results = pool.map(functools.partial(combination_processing,
                                             function=function,
                                             stabilizers_eigen_values=stabilizers_eigen_values,
                                             qubits_number=qubits_number),
                           itertools.permutations(list(range(len(function.truth_table[0]))), qubits_number))
    functions = set()
    for result in results:
        for function in result:
            functions.add(function)
    return functions
