from typing import Optional, Callable, Any, TypedDict
import numpy as np
from numpy.typing import NDArray
class OrbitalData(TypedDict):
    n: int
    l: int
    m: int
    color: tuple[float, float, float, float, float] # CMYKA

class GlobalStorage:
    # State Vector Storage
    state_vector: NDArray[np.float64] = np.array([])
    orbitals: list[OrbitalData] = []

    # Qubit Selection
    selected_qubit_one: int = 1
    selected_qubit_two: int = 2

class GlobalControllerManager:
    
    # State Vector Management
    align_state_vector_function: Optional[Callable[..., Any]] = None
    @classmethod
    def align_state_vector(cls) -> None:
        if callable(cls.align_state_vector):
            cls.align_state_vector()


    # Qubit Management
    align_qubits_function: Optional[Callable[..., Any]] = None  
    @classmethod
    def align_qubits(cls) -> None:
        if callable(cls.align_qubits_function):
            cls.align_qubits_function()

    select_qubit_one_function: Optional[Callable[..., Any]] = None
    @classmethod
    def select_qubit_one(cls) -> None:
        if callable(cls.select_qubit_one_function):
            cls.select_qubit_one_function()

    select_qubit_two_function: Optional[Callable[..., Any]] = None
    @classmethod
    def select_qubit_two(cls) -> None:
        if callable(cls.select_qubit_two_function):
            cls.select_qubit_two_function()


    # Orbital Management
    save_orbital_function: Optional[Callable[..., Any]] = None
    @classmethod
    def save_orbital(cls) -> None:
        if callable(cls.save_orbital_function):
            cls.save_orbital_function()

    clear_orbitals_function: Optional[Callable[..., Any]] = None
    @classmethod
    def clear_orbitals(cls) -> None:
        if callable(cls.clear_orbitals_function):
            cls.clear_orbitals_function()

    reshape_orbital_function: Optional[Callable[..., Any]] = None
    @classmethod
    def reshape_orbital(cls) -> None:
        if callable(cls.reshape_orbital_function):
            cls.reshape_orbital_function()


    # Quantum Gates
    collapse_state_vector_function: Optional[Callable[..., Any]] = None
    @classmethod
    def collapse_state_vector(cls) -> None:
        if callable(cls.collapse_state_vector_function):
            cls.collapse_state_vector_function()

    apply_hadamard_gate_function: Optional[Callable[..., Any]] = None
    @classmethod
    def apply_hadamard_gate(cls) -> None:
        if callable(cls.apply_hadamard_gate_function):
            cls.apply_hadamard_gate_function()

    apply_pauli_x_gate_function: Optional[Callable[..., Any]] = None
    @classmethod
    def apply_pauli_x_gate(cls) -> None:
        if callable(cls.apply_pauli_x_gate_function):
            cls.apply_pauli_x_gate_function()
    
    apply_pauli_y_gate_function: Optional[Callable[..., Any]] = None
    @classmethod
    def apply_pauli_y_gate(cls) -> None:
        if callable(cls.apply_pauli_y_gate_function):
            cls.apply_pauli_y_gate_function()

    apply_pauli_z_gate_function: Optional[Callable[..., Any]] = None
    @classmethod
    def apply_pauli_z_gate(cls) -> None:
        if callable(cls.apply_pauli_z_gate_function):
            cls.apply_pauli_z_gate_function()
    
    apply_cnot_gate_function: Optional[Callable[..., Any]] = None
    @classmethod
    def apply_cnot_gate(cls) -> None:
        if callable(cls.apply_cnot_gate_function):
            cls.apply_cnot_gate_function()

    apply_swap_gate_function: Optional[Callable[..., Any]] = None
    @classmethod
    def apply_swap_gate(cls) -> None:
        if callable(cls.apply_swap_gate_function):
            cls.apply_swap_gate_function()

    apply_imaginary_swap_gate_function: Optional[Callable[..., Any]] = None
    @classmethod
    def apply_imaginary_swap_gate(cls) -> None:
        if callable(cls.apply_imaginary_swap_gate_function):
            cls.apply_imaginary_swap_gate_function()