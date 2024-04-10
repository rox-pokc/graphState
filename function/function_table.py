import unittest
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

def XorConvolution(bit_vec1, bit_vec2):
    # Xor convolution of two bit vectors
    # b0,b1,b2 ^ c0,c1,c2 = (b0 & c1) ^ (b1 & c0) ^ (b2 & c2)
    assert len(bit_vec1) == len(bit_vec2), "Bit vectors must have the same length"
    res = 0
    for i in range(len(bit_vec1)):
        res = res ^ (bit_vec1[i] & bit_vec2[i])
    return res


# TODO: do a class truth table with titles, values, overrided toString and so on
def TruthTable(num_args):
    # Generate permutation for xor: 001 means x[2], 100 means x[0], 011 means x[1]^x[2], etc.
    xor_table = []
    for i in range(1, 2**num_args):
        bits = [int(x) for x in np.binary_repr(i, width=num_args)]
        xor_table.append(bits)
    xor_table = sorted(xor_table, key = cmp_to_key(CompareBitVecs))

    # Generate truth table: for 3 args, x1, x2, x3, x1^x2, x1^x3, x2^x3, x1^x2^x3
    truth_table = []
    for i in range(2**num_args):
        row = []
        bits = np.array([int(x) for x in np.binary_repr(i, width=num_args)])
        for k in range(len(xor_table)):
            row.append(XorConvolution(bits, xor_table[k]))
        truth_table.append(row)

    return truth_table

def get_truth_table(bool_func, num_args):
    # Generate truth table with a column for the function value
    truth_table = TruthTable(num_args)
    for i in range(len(truth_table)):
        truth_table[i].append(bool_func(truth_table[i][:num_args]))

    return truth_table

def FromTruthTableToFunction(truth_table):
    num_args = int(np.log2(len(truth_table[0]) + 1))

    f_str = ""
    # for i in range(len(truth_table)):
    #     x = truth_table[i][:num_args]
    #     y = truth_table[i][-1]
    #     if y == 1:
    #         for x_i in x:
    #             if 

    # we need to represent a function as AND of XORs
    # sage has Sbox() function that does this
    # https://doc.sagemath.org/html/en/reference/coding_theory/sage/coding_theory/sbox.html
    # it's likely connected to fft


    return num_args, "x[0] & x[1]"


def test_FromFunctionToTruthTable():

    # Test 1 - smallest case
    f1 = lambda x: (x[0] and x[1])
    num_args = 2
    result_table1 = np.matrix([[0,0,0,0],
                               [0,1,1,0],
                               [1,0,1,0],
                               [1,1,0,1]])
    truth_table = get_truth_table(f1, num_args)
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
    truth_table = get_truth_table(f2, num_args)
    print(truth_table)
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
    truth_table = get_truth_table(f3, num_args)
    assert np.array_equal(truth_table, result_table3)

    print("All function-to-table tests passed")
    return


def test_FromTruthTableToFunction():
    truth_table = [[0,0,0,0],
                    [0,1,1,0],
                    [1,0,1,0],
                    [1,1,0,1]]
    first_col = [row[0] for row in truth_table]
    print(first_col)
    num_args, f_str = FromTruthTableToFunction(truth_table)
    f = lambda x: eval(f_str)
    print(truth_table[0])
    for i in range(len(truth_table)):
        assert f(truth_table[i][:num_args]) == truth_table[i][-1]

    print("All table-to-function tests passed")
    return