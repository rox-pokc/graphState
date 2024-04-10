def get_permutations(string, left, right, permutations):
    if left == right:
        permutations.add("".join(string))
    else:
        for i in range(left, right + 1):
            string[left], string[i] = string[i], string[left]
            get_permutations(string, left + 1, right, permutations)
            string[left], string[i] = string[i], string[left]

def get_all_stabilizers(qubits_number):
    permutations = set()
    for i in range(0, qubits_number + 1, 2):
        string_stabilizer = ""
        string_stabilizer += "X" * (qubits_number - i)
        string_stabilizer += "Y" * i
        stringArr = list(string_stabilizer)
        get_permutations(stringArr, 0, qubits_number - 1, permutations)
    return permutations
