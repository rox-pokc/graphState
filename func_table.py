import numpy as np
from functools import cmp_to_key


def CompareBitVecs(bit_vec1, bit_vec2):
    # Check if bit_vec1 is greater than bit_vec2
    # For 2 bits: [1,0], [0,1], [1,1] - x1, x2, x1^x2
    # For 3 bits: [1,0,0], [0,1,0], [0,0,1], [1,1,0], [1,0,1], [0,1,1], [1,1,1] - x1, x2, x3, x1^x2, x1^x3, x2^x3, x1^x2^x3
    assert len(bit_vec1) == len(bit_vec2), "Bit strings must have the same length"
    if (sum(bit_vec1) > sum(bit_vec2)):
        return 1
    elif (sum(bit_vec1) < sum(bit_vec2)):
        return -1
    else:
        val1 = int("".join(str(i) for i in bit_vec1), 2)
        val2 = int("".join(str(i) for i in bit_vec2), 2)
        if val1 > val2:
            return -1
        elif val1 < val2:
            return 1
    return 0
def GeneratePermutations(num_args, with_zeros=False, sort = True):
    table = []
    if with_zeros:
        table.append([0 for i in range(num_args)])
    for i in range(1, 2**num_args):
        bits = [int(x) for x in np.binary_repr(i, width=num_args)]
        table.append(bits)
    if sort:
        table = sorted(table, key = cmp_to_key(CompareBitVecs))
    return table

def AndConvolution(bit_vec, control_vec):
    # And convolution of two bit vectors
    # b0,b1,b2 & c0,c1,c2 = &_i(b_i & c_i) for c_i = 1
    assert len(bit_vec) == len(control_vec), "Bit vectors must have the same length"
    res = 1
    for i in range(len(bit_vec)):
        if control_vec[i] != 0:
            res = res & (bit_vec[i] & control_vec[i])
    return res
    

def TruthTable(num_args):
    # Generate permutation for xor: 001 means x[2], 100 means x[0], 011 means x[1]^x[2], etc.
    xor_table = GeneratePermutations(num_args)

    # Generate truth table: for 3 args, x1, x2, x3, x1^x2, x1^x3, x2^x3, x1^x2^x3
    truth_table = []
    for i in range(2**num_args):
        row = []
        bits = np.array([int(x) for x in np.binary_repr(i, width=num_args)])
        for k in range(len(xor_table)):
            row.append((bits * xor_table[k]).sum() % 2)
        truth_table.append(row)

    return truth_table

def TruthTableAnd(num_args):
    # Generate permutation for xor: 001 means x[2], 100 means x[0], 011 means x[1]&x[2], etc.
    and_table = GeneratePermutations(num_args)

    # Generate truth table: for 3 args, x1, x2, x3, x1&x2, x1&x3, x2&x3, x1&x2&x3
    truth_table = []
    for i in range(2**num_args):
        row = [1]
        bits = np.array([int(x) for x in np.binary_repr(i, width=num_args)])
        for k in range(len(and_table)):
            row.append(AndConvolution(bits, and_table[k]))
        truth_table.append(row)

    return truth_table

def FromFuntionToTruthTable(bool_func, num_args):
    # Generate truth table with a column for the function value
    truth_table = TruthTable(num_args)
    for i in range(len(truth_table)):
        truth_table[i].append(bool_func(truth_table[i][:num_args]))
    return truth_table

def FromOutputToFuntion(f_x):
    num_args = int(np.log2(len(f_x)))
    and_table = TruthTableAnd(num_args)

    coeffs = []
    flag = 0
    for i in range(2**(2**num_args)):
        flag = 1
        coeffs = np.array([int(x) for x in np.binary_repr(i, width=2**num_args)])
        for j in range(len(and_table)):
            res = (coeffs * and_table[j]).sum() % 2
            if res != f_x[j]:
                flag = 0
                break
        if flag == 1:
            break

    perm_table = GeneratePermutations(num_args, with_zeros=True)
    f_str = ""
    if coeffs[0] == 1:
        f_str = "^1"
    for i in range(len(coeffs)):
        if coeffs[i] == 1:
            cur_str = ""
            for j in range(len(perm_table[i])):
                if perm_table[i][j] == 1:
                    cur_str += "&" + "x[" + str(j) + "]"
            if len(cur_str) > 0:
                f_str += "^(" + cur_str[1:] + ")"
    f_str = f_str[1:]
    if len(f_str) == 0:
        f_str = "0"
    return coeffs, f_str

def FromTruthTableToFuntion(truth_table):
    f_x = [row[-1] for row in truth_table]
    return FromOutputToFuntion(f_x)

def test_FromFuntionToTruthTable():

    # Test 1 - smallest case
    f1 = lambda x: (x[0] and x[1])
    num_args = 2
    result_table1 = np.matrix([[0,0,0,0],
                               [0,1,1,0],
                               [1,0,1,0],
                               [1,1,0,1]])
    truth_table = FromFuntionToTruthTable(f1, num_args)
    assert np.array_equal(truth_table, result_table1)

    # Test 2 - GHZ case
    f2 = lambda x: (x[0] and x[1]) ^ (x[1] and x[2])
    num_args = 3
    result_table2 = [[0,0,0,0,0,0,0,0],
                     [0,0,1,0,1,1,1,0],
                     [0,1,0,1,0,1,1,0],
                     [0,1,1,1,1,0,0,1],
                     [1,0,0,1,1,0,1,0],
                     [1,0,1,1,0,1,0,0],
                     [1,1,0,0,1,1,0,1],
                     [1,1,1,0,0,0,1,0]]
    truth_table = FromFuntionToTruthTable(f2, num_args)
    assert np.array_equal(truth_table, result_table2)

    # Test 3 - 4 args
    f3 = lambda x: (x[0] and x[1]) ^ (x[2] and x[3])
    num_args = 4
    result_table3 = []
    for i in range(2**num_args):
        x = np.array([int(b) for b in np.binary_repr(i, width=num_args)])
        row = [x[0], x[1], x[2], x[3],
              x[0]^x[1], x[0]^x[2], x[0]^x[3], x[1]^x[2], x[1]^x[3], x[2]^x[3],
              x[0]^x[1]^x[2], x[0]^x[1]^x[3], x[0]^x[2]^x[3], x[1]^x[2]^x[3], 
              x[0]^x[1]^x[2]^x[3], 
              f3(x)]
        result_table3.append(row)
    truth_table = FromFuntionToTruthTable(f3, num_args)
    assert np.array_equal(truth_table, result_table3)

    print("All function-to-table tests passed")
    return

def test_FromTruthTableToFuntion():

    truth_table = [[0,0,0,0,0,0,0,0],
                   [0,0,1,0,1,1,1,0],
                   [0,1,0,1,0,1,1,0],
                   [0,1,1,1,1,0,0,1],
                   [1,0,0,1,1,0,1,0],
                   [1,0,1,1,0,1,0,0],
                   [1,1,0,0,1,1,0,1],
                   [1,1,1,0,0,0,1,0]]
    num_args = 3
    coeffs, f_str = FromTruthTableToFuntion(truth_table)
    f = lambda x: eval(f_str)
    for i in range(len(truth_table)):
        assert f(truth_table[i][:num_args]) == truth_table[i][-1]

    perm2 = GeneratePermutations(2, with_zeros=True, sort=False)
    perm3 = GeneratePermutations(3, with_zeros=True, sort=False)
    perm4 = GeneratePermutations(4, with_zeros=True, sort=False)
    perm8 = GeneratePermutations(8, with_zeros=True, sort=False)
    
    for f_x in perm4:
        coeffs, f_str = FromOutputToFuntion(f_x)
        f = lambda x: eval(f_str)
        for i in range(len(perm2)):
            assert f(perm2[i]) == f_x[i]
    print("All table-to-function 2-input tests passed")

    for f_x in perm8:
        f_x = np.random.randint(0,2, 2**3)
        coeffs, f_str = FromOutputToFuntion(f_x)
        f = lambda x: eval(f_str)
        perm = GeneratePermutations(3, with_zeros=True)
        for i in range(len(perm3)):
            assert f(perm3[i]) == f_x[i]
    print("All table-to-function 3-input tests passed")

    for i in range(20):
        f_x = np.random.randint(0,2, 2**4)
        coeffs, f_str = FromOutputToFuntion(f_x)
        f = lambda x: eval(f_str)
        perm = GeneratePermutations(4, with_zeros=True)
        for i in range(len(perm4)):
            assert f(perm4[i]) == f_x[i]

    print("All table-to-function tests passed")
    return

test_FromFuntionToTruthTable()
test_FromTruthTableToFuntion()