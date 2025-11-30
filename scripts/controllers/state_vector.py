import bge
from bge import logic
from scripts.global_manager import GlobalControllerManager, GlobalStorage

def align_state_vector() -> None:
    '''
    Aligns the state vector to a specific basis.
    This is useful for preparing states for measurement.
    '''
    obj = logic.getCurrentController().owner

    ve = GlobalStorage.state_vector

# def collapse_state_vector(): 
#     '''
#     Collapses the state vector to a random weighted bit sequence.
#     The vector will end with a certain defined magnitude/direction/color.
#     '''
#     obj = logic.getCurrentController().owner


GlobalControllerManager.align_state_vector_function =  align_state_vector

