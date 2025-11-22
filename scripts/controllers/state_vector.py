from bge import logic

def align_state_vector():
    '''
    Aligns the state vector to a specific basis.
    This is useful for preparing states for measurement.
    '''
    obj = logic.getCurrentController().owner 

# def collapse_state_vector(): 
#     '''
#     Collapses the state vector to a random weighted bit sequence.
#     The vector will end with a certain defined magnitude/direction/color.
#     '''
#     obj = logic.getCurrentController().owner



