import bge
from bge import logic
import numpy as np
from numpy.typing import NDArray
from scripts.global_manager import GlobalControllerManager, GlobalStorage

def reshape_orbital() -> None:
    '''
    Reshapes the orbital according to specific parameters.
    This is useful for visualizing different orbital configurations.
    '''
    obj = logic.getCurrentController().owner

    # Logic for clearing old orbital


    vectors = GlobalStorage.past_state_vectors
    if len(vectors) == 0:

        return;

GlobalControllerManager.reshape_orbital_function = reshape_orbital