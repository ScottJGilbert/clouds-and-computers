import bge
from bge import logic

def align_qubits():
    '''
    Aligns qubits to a specific basis.
    This is useful for preparing qubits for measurement.
    '''
    obj = logic.getCurrentController().owner