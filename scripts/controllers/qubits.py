import bge
from bge import logic
import numpy as np
from scripts.global_manager import GlobalControllerManager, GlobalStorage

def align_qubits() -> None:
    '''
    Aligns qubits to a specific basis.
    '''

    ve = GlobalStorage.state_vector

    obj = logic.getCurrentController().owner

def select_qubit_one() -> None:
    '''
    Selects a specific qubit for operations.
    This is useful for targeted quantum gate applications.
    '''
    obj = logic.getCurrentController().owner

    selected_index = obj["qubit_index"]
    
    prev_selected_two = GlobalStorage.selected_qubit_two
    if (prev_selected_two <= selected_index):
        GlobalStorage.selected_qubit_two = 0 if (selected_index == 4) else selected_index + 1

    GlobalStorage.selected_qubit_one = selected_index

def select_qubit_two() -> None:
    '''
    Selects a specific qubit for operations.
    This is useful for targeted quantum gate applications.
    '''
    obj = logic.getCurrentController().owner
    blender_obj = obj.blenderObject

    selected_index = blender_obj["qubit_index"]
    
    prev_selected_one = GlobalStorage.selected_qubit_one
    if (prev_selected_one >= selected_index):
        GlobalStorage.selected_qubit_one = selected_index - 1
    
    GlobalStorage.selected_qubit_two = selected_index

GlobalControllerManager.align_qubits_function = align_qubits
GlobalControllerManager.select_qubit_one_function = select_qubit_one
GlobalControllerManager.select_qubit_two_function = select_qubit_two