def getPermutations(string, left, right, permutations):
    if left == right:
        permutations.add("".join(string))
    else:
        for i in range(left, right + 1):
            string[left], string[i] = string[i], string[left]
            getPermutations(string, left + 1, right, permutations)
            string[left], string[i] = string[i], string[left]

def getAllStabilizers(qubitsNumber):
    permutations = set()
    for i in range(0, qubitsNumber + 1, 2):
        stringStabilizer = ""
        stringStabilizer += "X" * (qubitsNumber - i)
        stringStabilizer += "Y" * i
        stringArr = list(stringStabilizer)
        getPermutations(stringArr, 0, qubitsNumber - 1, permutations)
    return permutations
