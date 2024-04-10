from qiskit import QuantumCircuit
from qiskit.quantum_info import StabilizerState
from state.stabilizer import *
from function.function_table import *
import itertools


def test_function(x): return (x[0] and x[1]) ^ (x[1] and x[2])


def compare_stabilizer_with_row(stabilizer, row_truth_table, direct):
    if direct:
        for i in range(len(stabilizer)):
            if not ((stabilizer[i] == 'X' and row_truth_table[i] == 0) or
                    (stabilizer[i] == 'Y' and row_truth_table[i] == 1)):
                return False
        return True
    else:
        for i in range(len(stabilizer)):
            if not ((stabilizer[i] == 'X' and row_truth_table[i] == 1) or
                    (stabilizer[i] == 'Y' and row_truth_table[i] == 0)):
                return False
        return True


def compare_ev_with_output(ev, output, direct):
    if direct:
        if ((ev == 1 and output == 1) or (ev == -1 and output == 0)):
            return True
        return False
    else:
        if ((ev == 1 and output == 0) or (ev == -1 and output == 1)):
            return True
        return False


def brute_force_make_connection(stabilizers_eigen_values, truth_table):
    array = list(range(len(truth_table[0])))
    combinations = list(itertools.combinations(array, 4))
    for stab_comp in range(2):
        for ev_comp in range(2):
            for combination in combinations:
                used = []
                for i in range(len(truth_table)):
                    used.append(False)
                updated = False
                for stabilizer in stabilizers_eigen_values:
                    for i in range(len(truth_table)):
                        if (not used[i] and
                                compare_stabilizer_with_row(stabilizer,
                                                            [truth_table[i][j] for j in combination],
                                                            stab_comp) and
                                compare_ev_with_output(stabilizers_eigen_values[stabilizer],
                                                       truth_table[i][len(truth_table[i]) - 1],
                                                       ev_comp)):
                            used[i] = True
                            updated = True
                            continue
                    # print(stabilizer)
                    # print(used)
                    if not updated:
                        # print("Start over!!")
                        break
                if all(used):
                    print("This is a solution!")
                    return True
    return False


qc = QuantumCircuit(4)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(2, 3)

state = StabilizerState(qc)

stabilizers_eigen_values = find_all_stabilizers(state)
for stabilizer in stabilizers_eigen_values:
    print(stabilizer, "\t", stabilizers_eigen_values[stabilizer])

# TODO: check if f.__code__.co_stacksize is really a number of inputs
truth_table = get_truth_table(test_function, test_function.__code__.co_stacksize)
print('x1\tx2\tx3\tx1^x2\tx1^x3\tx2^x3\tx1^x2^x3\tf')
print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in truth_table]))

solution_exist = brute_force_make_connection(stabilizers_eigen_values, truth_table)
print(solution_exist)
