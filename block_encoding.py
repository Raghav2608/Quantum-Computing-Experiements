from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import SparsePauliOp
import numpy as np
    
def create_block_encoding(A) -> QuantumCircuit:
    pauli_op = SparsePauliOp.from_operator(A)
    
    n_ancilla = int(np.ceil(np.log2(len(pauli_op.coeffs))))
    n_reg = int(np.ceil(np.log2(len(A))))
    amps = np.sqrt(np.abs(pauli_op.coeffs)/np.linalg.norm(pauli_op.coeffs,ord=1))
    padded_amps = np.zeros(2**n_ancilla)
    padded_amps[:len(amps)] = amps

    ψ = "0"*n_reg
    ctrl_reg = QuantumRegister(n_ancilla,name='ctrl')
    encode_reg = QuantumRegister(n_reg,name='q')
    cl_reg = ClassicalRegister(n_ancilla)
    
    qc  = QuantumCircuit(encode_reg,ctrl_reg,cl_reg)
    qc.prepare_state(ψ,encode_reg)
    qc.prepare_state(padded_amps,ctrl_reg)

    for index, pauli in enumerate(pauli_op.paulis):
        intstr = np.binary_repr(index,n_ancilla)
        control_pauli_k = pauli.to_instruction().control(num_ctrl_qubits=n_ancilla,ctrl_state=intstr)
        qc.append(control_pauli_k,ctrl_reg[:] + encode_reg[::])

    qc.prepare_state(padded_amps,ctrl_reg).inverse()
    qc.draw("mpl")
    return qc

def multiply_block_encoding(A: QuantumCircuit,B:QuantumCircuit):
    qc = QuantumCircuit(A.num_qubits + B.num_qubits)
    qc.append(A.to_instruction(),qc.qubits[:A.num_qubits])
    qc.append(B.to_instruction(),qc.qubits[A.num_qubits:])
    return qc


        