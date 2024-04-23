import itertools
import multiprocessing
import functools
import time
from math import ceil
import numpy as np


def test_function(x): return (x[0] and x[1]) ^ x[2]


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


def choice_processing(products, truth_table, stabilizers_eigen_values):
    start = time.time()
    results = []
    for product in products:
        combination = product[0]
        choice = product[1]
        order = product[2]
        found = True
        for row in range(len(truth_table)):
            table_row_stabilizer = ""
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
            results.append({"combination": combination, "choice": choice, "order": order})
    end = time.time()
    print("One combination on elapsed: ", end - start)
    return results


# def combination_processing(combination, truth_table, stabilizers_eigen_values, qubits_number):
#     start = time.time()
#     results = []
#     choices = list(itertools.product(range(len(INPUT_COMPARE_CHOICES)), repeat=qubits_number))
#     for order in EV_COMPARE_CHOICES:
#         with multiprocessing.Pool() as pool:
#             results.append(pool.map(functools.partial(choice_processing,
#                                                       combination=combination,
#                                                       truth_table=truth_table,
#                                                       stabilizers_eigen_values=stabilizers_eigen_values,
#                                                       order=order),
#                                     choices))
#     end = time.time()
#     print("One combination on elapsed: ", end - start)
#     return results


def brute_force_connect(truth_table, stabilizers_eigen_values, qubits_number):
    start = time.time()
    combinations = list(itertools.combinations(list(range(len(truth_table[0]) - 1)), qubits_number))
    # results = []
    # for combination in combinations:
    #     results.append(combination_processing(combination, truth_table, stabilizers_eigen_values, qubits_number))

    choices = list(itertools.product(range(len(INPUT_COMPARE_CHOICES)), repeat=qubits_number))
    product = list(itertools.product(combinations, choices, EV_COMPARE_CHOICES))
    end = time.time()
    print("Beginning ", end - start)
    with multiprocessing.Pool() as pool:
        chunksize = ceil(len(product) / len(pool._pool))
        worker_load = [product[i:i + chunksize] for i in range(0, len(product), chunksize)]
        returns = []
        s = time.time()
        returns = pool.map(functools.partial(choice_processing,
                                             truth_table=truth_table,
                                             stabilizers_eigen_values=stabilizers_eigen_values),
                           worker_load
                           )

        e = time.time()
        print("returns ", e - s)
        return np.concatenate(returns)
    # with pool:
    #     return pool.map(functools.partial(combination_processing,
    #                                       truth_table=truth_table,
    #                                       stabilizers_eigen_values=stabilizers_eigen_values,
    #                                       qubits_number=qubits_number),
    #                     combinations)
    # return results
