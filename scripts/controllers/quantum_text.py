from bge import logic

def edit_principal_quantum_number():
    '''
    Displays all available principal quantum numbers on the UI.
    '''

    obj = logic.getCurrentController().owner
    blender_obj = obj.blenderObject

    orbital_data = logic.globalDict.get("orbitals", [])

    principal_quantum_numbers = sorted(set([data["n"] for data in orbital_data]))

    text = "n: " + ", ".join(str(n) for n in principal_quantum_numbers)
    blender_obj.data.body = text

def edit_azimuthal_quantum_number():
    '''
    Displays all available azimuthal quantum numbers on the UI.
    '''

    obj = logic.getCurrentController().owner
    blender_obj = obj.blenderObject

    orbital_data = logic.globalDict.get("orbitals", [])

    azimuthal_quantum_numbers = sorted(set([data["l"] for data in orbital_data]))

    text = "l: " + ", ".join(str(l) for l in azimuthal_quantum_numbers)
    blender_obj.data.body = text

def edit_magnetic_quantum_number(): 
    '''
    Displays all available magnetic quantum numbers on the UI.
    '''

    obj = logic.getCurrentController().owner
    blender_obj = obj.blenderObject

    orbital_data = logic.globalDict.get("orbitals", [])

    magnetic_quantum_numbers = sorted(set([data["m"] for data in orbital_data]))

    text = "m: " + ", ".join(str(m) for m in magnetic_quantum_numbers)
    blender_obj.data.body = text