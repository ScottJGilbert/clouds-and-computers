import bge
from bge import logic
from scripts.global_manager import GlobalControllerManager, GlobalStorage

def save_orbital():
    '''
    Saves the current orbital configuration.
    This is useful for restoring previous states.
    '''
    obj = logic.getCurrentController().owner

    GlobalStorage.past_state_vectors.append(GlobalStorage.state_vector.copy())

def delete_orbital():
    '''
    Deletes the last saved orbital configuration.
    This is useful for managing memory and state history.
    '''
    obj = logic.getCurrentController().owner

def toggle_visibility():
    '''
    Toggles the visibility of the orbital representation.
    This is useful for focusing on different aspects of the simulation.
    '''
    obj = logic.getCurrentController().owner

GlobalControllerManager.save_orbital_function = save_orbital
GlobalControllerManager.delete_orbital_function = delete_orbital
GlobalControllerManager.toggle_visibility_function = toggle_visibility
