from qiskit.quantum_info import Pauli
from qiskit.primitives import StatevectorEstimator as Estimator
from qiskit.quantum_info import SparsePauliOp
from numpy import round
from state.stabilizer_list import *


def find_all_stabilizers(state):
    all_stabilizers = get_all_stabilizers(7)  # for now amount of qubits hardcoded
    eigen_values = {}
    plus_stabilizers = set()
    minus_stabilizers = set()
    for stabilizer in all_stabilizers:
        ev = state.expectation_value(Pauli(stabilizer))
        eigen_values[stabilizer] = state.expectation_value(Pauli(stabilizer))
        if ev == 1:
            plus_stabilizers.add(stabilizer)
        else:
            if ev == -1:
                minus_stabilizers.add(stabilizer)
    print("+1: ", plus_stabilizers)
    print("-1: ", minus_stabilizers)

    # checked ev using estimator and finding expectation value of operator
    # estimator = Estimator()
    # for stabilizer in allStabilizers:
    #     job = estimator.run([(qc, SparsePauliOp(stabilizer), [])])
    #     job_result = job.result()
    #     print(stabilizer, " ", round(job_result[0].data.evs))

    return eigen_values

