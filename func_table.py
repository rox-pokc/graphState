import numpy as np
from functools import cmp_to_key

class BooleanFunction:
    num_args = 0
    truth_table = []
    inverse_table_and = []
    full_perm_table = []
    inputs_perm_table = []

    def __init__(self, num_args):
        self.num_args = num_args
        self.truth_table = self.truth_table()
        self.inverse_table_and = np.linalg.inv(self.truth_table_and()).astype(int) % 2
        self.full_perm_table = self.generate_permutations(num_args, with_zeros=True)
        self.inputs_perm_table = self.generate_permutations(num_args, with_zeros=False)

    @staticmethod
    def compare_bit_vecs(bit_vec1, bit_vec2):
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
    @staticmethod
    def generate_permutations(num_args, with_zeros=False, sort = True):
        table = []
        if with_zeros:
            table.append([0 for i in range(num_args)])
        for i in range(1, 2**num_args):
            bits = [int(x) for x in np.binary_repr(i, width=num_args)]
            table.append(bits)
        if sort:
            table = sorted(table, key = cmp_to_key(BooleanFunction.compare_bit_vecs))
        return table

    def and_convolution(self, bit_vec, control_vec):
        # And convolution of two bit vectors
        # b0,b1,b2 & c0,c1,c2 = &_i(b_i & c_i) for c_i = 1
        assert len(bit_vec) == len(control_vec), "Bit vectors must have the same length"
        res = 1
        for i in range(len(bit_vec)):
            if control_vec[i] != 0:
                res = res & (bit_vec[i] & control_vec[i])
        return res
    

    def truth_table(self):
        # Generate permutation for xor: 001 means x[2], 100 means x[0], 011 means x[1]^x[2], etc.
        xor_table = self.generate_permutations(self.num_args)

        # Generate truth table: for 3 args, x1, x2, x3, x1^x2, x1^x3, x2^x3, x1^x2^x3
        truth_table = []
        for i in range(2**self.num_args):
            row = []
            bits = np.array([int(x) for x in np.binary_repr(i, width=self.num_args)])
            for k in range(len(xor_table)):
                row.append((bits * xor_table[k]).sum() % 2)
            truth_table.append(row)

        return truth_table

    def truth_table_and(self):
        # Generate permutation for xor: 001 means x[2], 100 means x[0], 011 means x[1]&x[2], etc.
        and_table = self.generate_permutations(self.num_args)

        # Generate truth table: for 3 args, x1, x2, x3, x1&x2, x1&x3, x2&x3, x1&x2&x3
        truth_table = []
        for i in range(2**self.num_args):
            row = [1]
            bits = np.array([int(x) for x in np.binary_repr(i, width=self.num_args)])
            for k in range(len(and_table)):
                row.append(self.and_convolution(bits, and_table[k]))
            truth_table.append(row)
        return truth_table

    def from_function_to_truth_table(self, bool_func):
        # Generate truth table with a column for the function value
        truth_table = self.truth_table
        for i in range(len(truth_table)):
            truth_table[i].append(bool_func(truth_table[i][:self.num_args]))
        return truth_table

    def from_output_to_coeffs(self, f_x):
        return (self.inverse_table_and.dot(f_x) % 2).astype(int)

    def from_output_to_function(self, f_x, return_coeffs = False):
        coeffs = self.from_output_to_coeffs(f_x)

        perm_table = self.full_perm_table
        f_str = ""
        if coeffs[0] == 1:
            f_str = "^1"
        for i in range(1, len(coeffs)):
            if coeffs[i] == 1:
                cur_str = ""
                for j in range(len(perm_table[i])):
                    if perm_table[i][j] == 1:
                        cur_str += "&" + "x[" + str(j) + "]"
                if len(cur_str) > 0:
                    f_str += "^" + cur_str[1:]
        f_str = f_str[1:]
        if len(f_str) == 0:
            f_str = "0"
        if return_coeffs:
            return coeffs, f_str
        return f_str

    def from_truth_table_to_function(self, truth_table):
        f_x = [row[-1] for row in truth_table]
        return self.from_output_to_function(f_x)

    def from_outputs_to_functions(self, f_xs):
        res = []
        for f_x in f_xs:
            f_str = self.from_output_to_function(f_x)
            res.append(f_str)
        return res

    def from_eigen_to_function(self, eigenvalues, encoding = {1: 0, -1: 1}):
        assert len(eigenvalues) == 2**self.num_args, "Eigenvalues must have the same length as the number of rows in the truth table"
        f_x = [encoding[e] for e in eigenvalues]
        return self.from_output_to_function(f_x)

    def from_eigens_to_functions(self, eigens):
        res = []
        for eigenvalues in eigens:
            f_str = self.from_eigen_to_function(eigenvalues)
            res.append(f_str)
        return res

    def inputs_from_indexes(self, idxs):
        # For 3-input truth table: x1, x2, x3, x1&x2, x1&x3, x2&x3, x1&x2&x3
        assert(len(idxs) == 2**self.num_args - 1), "Input indexes must have the same length as the number of rows in the truth table"
        perm_table = self.inputs_perm_table
        inputs = []
        for i in range(len(idxs)):
            if idxs[i] == 1:
                cur_str = ""
                for j in range(len(perm_table[i])):
                    if perm_table[i][j] == 1:
                        cur_str += "^" + "x_" + str(j)
                if len(cur_str) > 0:
                    inputs.append(cur_str[1:])
        return inputs

def test_from_function_to_truth_table():

    # Test 1 - smallest case
    f1 = lambda x: (x[0] and x[1])
    bf2 = BooleanFunction(num_args = 2)
    result_table1 = np.matrix([[0,0,0,0],
                               [0,1,1,0],
                               [1,0,1,0],
                               [1,1,0,1]])
    truth_table = bf2.from_function_to_truth_table(f1)
    assert np.array_equal(truth_table, result_table1)

    # Test 2 - GHZ case
    f2 = lambda x: (x[0] and x[1]) ^ (x[1] and x[2])
    bf3 = BooleanFunction(num_args = 3)
    result_table2 = [[0,0,0,0,0,0,0,0],
                     [0,0,1,0,1,1,1,0],
                     [0,1,0,1,0,1,1,0],
                     [0,1,1,1,1,0,0,1],
                     [1,0,0,1,1,0,1,0],
                     [1,0,1,1,0,1,0,0],
                     [1,1,0,0,1,1,0,1],
                     [1,1,1,0,0,0,1,0]]
    truth_table = bf3.from_function_to_truth_table(f2)
    assert np.array_equal(truth_table, result_table2)

    # Test 3 - 4 args
    f3 = lambda x: (x[0] and x[1]) ^ (x[2] and x[3])
    num_args = 4
    bf4 = BooleanFunction(num_args)
    result_table3 = []
    for i in range(2**num_args):
        x = np.array([int(b) for b in np.binary_repr(i, width=num_args)])
        row = [x[0], x[1], x[2], x[3],
              x[0]^x[1], x[0]^x[2], x[0]^x[3], x[1]^x[2], x[1]^x[3], x[2]^x[3],
              x[0]^x[1]^x[2], x[0]^x[1]^x[3], x[0]^x[2]^x[3], x[1]^x[2]^x[3], 
              x[0]^x[1]^x[2]^x[3], 
              f3(x)]
        result_table3.append(row)
    truth_table = bf4.from_function_to_truth_table(f3)
    assert np.array_equal(truth_table, result_table3)

    print("All function-to-table tests passed")
    return


def test_from_truth_table_to_function():
    bf2 = BooleanFunction(2)
    bf3 = BooleanFunction(3)
    bf4 = BooleanFunction(4)

    # print(bf2.inputs_from_indexes(np.ones(3)))
    # print(bf3.inputs_from_indexes(np.ones(7)))
    # print(bf4.inputs_from_indexes(np.ones(15)))

    # print(bf2.from_eigen_to_function([+1, +1, +1, -1], encoding = {1: 1, -1: 0}))
    # print(bf3.from_eigens_to_functions([[+1, +1, +1, -1, -1, -1, -1, +1], [+1, +1, -1, -1, -1, +1, +1, +1]]))
    # print(bf4.from_eigen_to_function([+1, +1, -1, -1, -1, +1, +1, -1, -1, +1, +1, -1, +1, -1, -1, -1]))

    truth_table = [[0,0,0,0,0,0,0,0],
                   [0,0,1,0,1,1,1,0],
                   [0,1,0,1,0,1,1,0],
                   [0,1,1,1,1,0,0,1],
                   [1,0,0,1,1,0,1,0],
                   [1,0,1,1,0,1,0,0],
                   [1,1,0,0,1,1,0,1],
                   [1,1,1,0,0,0,1,0]]
    num_args = 3
    bf3 = BooleanFunction(num_args)
    f_str = bf3.from_truth_table_to_function(truth_table)
    f = lambda x: eval(f_str)
    for i in range(len(truth_table)):
        assert f(truth_table[i][:num_args]) == truth_table[i][-1]

    perm2 = BooleanFunction.generate_permutations(2, with_zeros=True, sort=False)
    perm3 = BooleanFunction.generate_permutations(3, with_zeros=True, sort=False)
    perm4 = BooleanFunction.generate_permutations(4, with_zeros=True, sort=False)
    perm8 = BooleanFunction.generate_permutations(8, with_zeros=True, sort=False)
    
    for f_x in perm4:
        f_str = bf2.from_output_to_function(f_x)
        f = lambda x: eval(f_str)
        for i in range(len(perm2)):
            assert f(perm2[i]) == f_x[i]
    print("All table-to-function 2-input tests passed")

    for f_x in perm8:
        f_str = bf3.from_output_to_function(f_x)
        f = lambda x: eval(f_str)
        for i in range(len(perm3)):
            assert f(perm3[i]) == f_x[i]
    print("All table-to-function 3-input tests passed")

    for i in range(200):
        f_x = np.random.randint(0,2, 2**4)
        f_str = bf4.from_output_to_function(f_x)
        f = lambda x: eval(f_str)
        for i in range(len(perm4)):
            assert f(perm4[i]) == f_x[i]
    
    # Test 5-input function - doesn't work because of linalg inversion
    # f_x = [0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0]
    # f_coeffs = bf5.from_output_to_coeffs(f_x)
    # print(f_coeffs)
    # f_str = "x[1]^x[4]^x[0]&x[1]^x[0]&x[3]^x[1]&x[2]^x[3]&x[4]^x[0]&x[2]&x[4]^x[1]&x[3]&x[4]^x[2]&x[3]&x[4]^x[0]&x[1]&x[2]&x[3]^x[0]&x[1]&x[2]&x[4]^x[1]&x[2]&x[3]&x[4]^x[0]&x[1]&x[2]&x[3]&x[4]"
    # f = lambda x: eval(f_str)
    # for i in range(len(perm5)):
    #     assert f(perm5[i]) == f_x[i]

    print("All table-to-function tests passed")
    return

test_from_function_to_truth_table()
test_from_truth_table_to_function()