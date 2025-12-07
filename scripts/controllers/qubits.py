import math
from bge import logic
import numpy as np
from scripts.global_manager import GlobalConstants
# from scripts.global_manager import GlobalControllerManager

def align_qubits() -> None:
    '''
    Aligns qubits to a specific basis.
    '''

    obj = logic.getCurrentController().owner
    blender_obj = obj.blenderObject

    selected_index = obj.get("qubit_index", -1)

    max_scale = GlobalConstants.max_scale

    superposition = derive_superposition(selected_index)

    blender_obj.scale = (
        blender_obj.scale[0],
        superposition * max_scale,
        blender_obj.scale[2]
    )


def derive_superposition(index: int) -> float:
    '''
    Derives the superposition value for a given qubit index.
    This is useful for quantum state manipulations.
    '''
    ve = logic.globalDict.get("state_vector", np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]))

    if index < 0 or index >= math.log2(len(ve)):
        raise IndexError("Qubit index out of range.")
    
    sum: float = 0.0
    
    for index, value in enumerate(ve):
        # Convert to binary array
        binary_sequence: list[int] = [int(x) for x in bin(index)[2:].zfill(int(math.log2(len(ve))))]
        if binary_sequence[index] == 1:
            sum += value
        else:
            sum -= value

    return sum


def select_qubit() -> None:
    '''
    Selects a specific qubit for operations.
    This is useful for targeted quantum gate applications.
    '''
    obj = logic.getCurrentController().owner

    selected_index = obj.get("qubit_index")

    prev_selected_one = logic.globalDict.get("selected_qubit_one", -1)
    prev_selected_two = logic.globalDict.get("selected_qubit_two", -1)

    if (selected_index == prev_selected_one or selected_index == prev_selected_two):
        return  # No change needed
    
    if (prev_selected_one == -1):
        logic.globalDict["selected_qubit_one"] = selected_index
    elif (prev_selected_two == -1):
        logic.globalDict["selected_qubit_two"] = selected_index
    else:
        logic.globalDict["selected_qubit_two"] = logic.globalDict["selected_qubit_one"]  # Shift the first to second
        logic.globalDict["selected_qubit_one"] = selected_index  # Set the new first qubit