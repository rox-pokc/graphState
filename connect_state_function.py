import itertools
import multiprocessing
import functools
from function.function_table import *


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


def combination_processing(combination, function, stabilizers_eigen_values, qubits_number):
    if event.is_set():
        return
    truth_table = function.truth_table
    for choice in itertools.product(range(len(INPUT_COMPARE_CHOICES)), repeat=qubits_number):
        if all(outcome for outcome in outcomes.values()):
            event.set()
            return
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
                    outputs.append(1)
                else:
                    outputs.append(0)
            obtained_outcome = tuple(outputs)
            if obtained_outcome in outcomes:
                outcomes[obtained_outcome] = True


def get_set_of_functions_outcomes(filename):
    file = open(filename)
    functions_outcomes = dict()
    while True:
        content = file.readline()
        if not content:
            break
        truth_table = BooleanFunction(3).from_function_to_truth_table(lambda x: eval(content))
        function_outcomes = []
        for row in truth_table:
            function_outcomes.append(row[len(row) - 1])
        functions_outcomes[tuple(function_outcomes)] = False
    file.close()
    return functions_outcomes


def init_worker(GHZ_outcomes, shared_event):
    global outcomes
    outcomes = GHZ_outcomes

    global event
    event = shared_event


def parallel_search_each_class(GHZ_outcomes, function, stabilizers_eigen_values, qubits_number):
    with multiprocessing.Manager() as manager:
        shared_event = manager.Event()
        pool = multiprocessing.Pool(initializer=init_worker, initargs=(GHZ_outcomes, shared_event,))
        with pool:
            results = pool.map_async(functools.partial(combination_processing,
                                                       function=function,
                                                       stabilizers_eigen_values=stabilizers_eigen_values,
                                                       qubits_number=qubits_number),
                                     itertools.permutations(list(range(len(function.truth_table[0]))), qubits_number),
                                     )
            results.wait()
            pool.close()
            pool.join()
        return shared_event.is_set()


def search_functions(function, stabilizers_eigen_values, qubits_number):
    GHZ_7_coverage = parallel_search_each_class(
        get_set_of_functions_outcomes("function/dictionary/7-GHZ_functions.txt"),
        function, stabilizers_eigen_values, qubits_number)
    if GHZ_7_coverage:
        print("GHZ-7 functions class coverage")
    else:
        GHZ_4_coverage = parallel_search_each_class(
            get_set_of_functions_outcomes("function/dictionary/4-GHZ_functions.txt"),
            function, stabilizers_eigen_values, qubits_number)
        if GHZ_4_coverage:
            print("GHZ-4 functions class coverage")
        else:
            GHZ_3_coverage = parallel_search_each_class(
                get_set_of_functions_outcomes("function/dictionary/3-GHZ_functions.txt"),
                function, stabilizers_eigen_values, qubits_number)
            if GHZ_3_coverage:
                print("GHZ-3 functions class coverage")
            else:
                print("GHZ-2 functions class coverage")
