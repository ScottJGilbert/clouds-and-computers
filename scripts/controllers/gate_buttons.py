from bge import logic
import numpy as np
# from scripts.global_manager import GlobalControllerManager

def collapse_state_vector() -> None:
    '''
    Collapses the state vector to a random weighted bit sequence.
    The vector will end with a certain defined magnitude/direction/color.
    '''
    # Logic for collapsing GlobalStorage.state_vector

    ve = logic.globalDict.get("state_vector", np.array([]))
    num_states = len(ve)
    
    probabilities = np.abs(ve)**2
    probabilities /= np.sum(probabilities)
    
    collapsed_index = np.random.choice(num_states, p=probabilities)
    
    new_ve = np.zeros_like(ve)
    new_ve[collapsed_index] = 1.0
    
    logic.globalDict["state_vector"] = new_ve

def hadamard_gate() -> None:
    '''
    Applies the Hadamard gate to the state vector.
    This creates superposition states.
    '''
    # Logic for applying Hadamard gate to GlobalStorage.state_vector

    matrix = (1/np.sqrt(2)) * np.array([[1, 1], [1, -1]])
    ve = logic.globalDict.get("state_vector", np.array([]))

    ve = apply_gate(ve, matrix, logic.globalDict.get("selected_qubit_one", -1))

    logic.globalDict["state_vector"] = ve

def pauli_x_gate() -> None:
    '''
    Applies the Pauli-X gate to the state vector.
    This flips the qubit state.
    '''
    # Logic for applying Pauli-X gate to GlobalStorage.state_vector

    matrix = np.array([[0, 1], [1, 0]])
    ve = logic.globalDict.get("state_vector", np.array([]))

    ve = apply_gate(ve, matrix, logic.globalDict.get("selected_qubit_one", -1))

    logic.globalDict["state_vector"] = ve

def pauli_y_gate() -> None:
    '''
    Applies the Pauli-Y gate to the state vector.
    This introduces a phase flip along with state flip.
    '''
    # Logic for applying Pauli-Y gate to GlobalStorage.state_vector

    matrix = np.array([[0, -1j], [1j, 0]], dtype=complex)
    ve = logic.globalDict.get("state_vector", np.array([]))

    ve = apply_gate(ve, matrix, logic.globalDict.get("selected_qubit_one", -1))

    logic.globalDict["state_vector"] = ve

def pauli_z_gate() -> None:
    '''
    Applies the Pauli-Z gate to the state vector.
    This introduces a phase flip.
    '''
    # Logic for applying Pauli-Z gate to GlobalStorage.state_vector

    matrix = np.array([[1, 0], [0, -1]])
    ve = logic.globalDict.get("state_vector", np.array([]))

    ve = apply_gate(ve, matrix, logic.globalDict.get("selected_qubit_one", -1))

    logic.globalDict["state_vector"] = ve

def cnot_gate() -> None:
    '''
    Applies the CNOT gate to the state vector.
    This entangles two qubits.
    '''
    # Logic for applying CNOT gate to GlobalStorage.state_vector

    matrix = np.array([[1, 0, 0, 0],
                       [0, 1, 0, 0],
                       [0, 0, 0, 1],
                       [0, 0, 1, 0]])
    ve = logic.globalDict.get("state_vector", np.array([]))

    ve = apply_gate(ve, matrix, logic.globalDict.get("selected_qubit_one", -1))

    logic.globalDict["state_vector"] = ve

def swap_gate() -> None:
    '''
    Applies the SWAP gate to the state vector.
    This swaps the states of two qubits.
    '''
    # Logic for applying SWAP gate to GlobalStorage.state_vector

    matrix = np.array([[1, 0, 0, 0],
                       [0, 0, 1, 0],
                       [0, 1, 0, 0],
                       [0, 0, 0, 1]])
    ve = logic.globalDict.get("state_vector", np.array([]))

    ve = apply_gate(ve, matrix, logic.globalDict.get("selected_qubit_one", -1))

    logic.globalDict["state_vector"] = ve

def imaginary_swap_gate() -> None:
    '''
    Applies the iSWAP gate to the state vector.
    This swaps the states of two qubits with a phase factor.
    '''
    # Logic for applying iSWAP gate to GlobalStorage.state_vector

    matrix = np.array([[1, 0, 0, 0],
                       [0, 0, 1j, 0],
                       [0, 1j, 0, 0],
                       [0, 0, 0, 1]])
    ve = logic.globalDict.get("state_vector", np.array([]))

    ve = apply_gate(ve, matrix, logic.globalDict.get("selected_qubit_one", -1))

    logic.globalDict["state_vector"] = ve

def apply_gate(state_vector: np.ndarray, gate: np.ndarray, qubit_index: int) -> np.ndarray:
    """
    Applies a quantum gate to a specific qubit in a multi-qubit system.
    
    Parameters:
        state_vector (numpy.ndarray): The state vector of the multi-qubit system.
        gate (numpy.ndarray): The gate matrix (2x2 for single-qubit, larger for multi-qubit gates).
        qubit_index (int): The index of the qubit (0-based) to which the gate should be applied.
        num_qubits (int): The total number of qubits in the system.
        
    Returns:
        numpy.ndarray: The new state vector after applying the gate.
    """

    num_qubits = 4

    # Identity matrix of size 2 (for single qubit)
    I = np.array([[1, 0], [0, 1]])

    # Build the full gate matrix using tensor product
    full_gate = I
    for i in range(num_qubits):
        if i == qubit_index:
            full_gate = np.kron(full_gate, gate)  # Apply the gate on the desired qubit
        else:
            full_gate = np.kron(full_gate, I)  # Apply identity on other qubits
    
    # Apply the full gate to the state vector
    new_state = np.dot(full_gate, state_vector)
    
    return new_state