#GHZ-state
from qiskit import QuantumCircuit
from qiskit.quantum_info import StabilizerState, Pauli

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(0, 2)
stab = StabilizerState(qc)

exp_value = stab.expectation_value(Pauli('XYZ'))

print(stab)
print(exp_value)