from bge import logic
import numpy as np
from scripts.global_manager import OrbitalData
# from scripts.global_manager import GlobalControllerManager

def save_orbital():
    '''
    Saves the current orbital configuration.
    This is useful for restoring previous states.

    When determining quantum numbers, take the percent of available numbers and round to nearest integer.
    n: principal quantum number | 1 - 4
    l: azimuthal quantum number | 0 - 3
    m: magnetic quantum number  | -2 - 2
    '''

    ve = logic.globalDict.get("state_vector", np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]))

    orbital_data: OrbitalData = {
        "n": round(ve[0].real * 3) + 1,
        "l": round(ve[1].real * 3),
        "m": round((ve[2].real + 1) * 2),
        "color": (ve[3].real, ve[4].real, ve[5].real, ve[6].real, ve[7].real)
    }
    current_orbitals = logic.globalDict.get("orbitals", [])

    current_orbitals.append(orbital_data)
    logic.globalDict["orbitals"] = current_orbitals

def clear_orbitals():
    '''
    Deletes the all saved orbital configurations.
    This is useful for managing memory and state history.
    '''

    logic.globalDict["orbitals"] = []