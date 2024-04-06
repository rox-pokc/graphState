from qiskit import QuantumCircuit
from qiskit.quantum_info import StabilizerState, Pauli
from qiskit.primitives import StatevectorEstimator as Estimator
from qiskit.quantum_info import SparsePauliOp
from numpy import round
from StabilizerList import *

qc = QuantumCircuit(4)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)
qc.cx(0, 3)
state = StabilizerState(qc)

allStabilizers = getAllStabilizers(4)
eigenValues = {}
plusStabilizers = set()
minusStabilizers = set()
for stabilizer in allStabilizers:
    ev = state.expectation_value(Pauli(stabilizer))
    eigenValues[stabilizer] = state.expectation_value(Pauli(stabilizer))
    if ev == 1:
        plusStabilizers.add(stabilizer)
    else:
        if ev == -1:
            minusStabilizers.add(stabilizer)
print(plusStabilizers)
print(minusStabilizers)

# checked ev using estimator and finding expectation value of operator
estimator = Estimator()
for stabilizer in allStabilizers:
    job = estimator.run([(qc, SparsePauliOp(stabilizer), [])])
    job_result = job.result()
    print(stabilizer, " ", round(job_result[0].data.evs))



