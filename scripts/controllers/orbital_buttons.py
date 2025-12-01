import bge
from bge import logic
from scripts.global_manager import GlobalControllerManager, GlobalStorage, OrbitalData

def save_orbital():
    '''
    Saves the current orbital configuration.
    This is useful for restoring previous states.

    When determining quantum numbers, take the percent of available numbers and round to nearest integer.
    n: principal quantum number | 1 - 4
    l: azimuthal quantum number | 0 - 3
    m: magnetic quantum number  | -2 - 2
    '''
    obj = logic.getCurrentController().owner

    ve = GlobalStorage.state_vector

    orbital_data: OrbitalData = {
        "n": round(ve[0].real * 3) + 1,
        "l": round(ve[1].real * 3),
        "m": round((ve[2].real + 1) * 2),
        "color": (ve[3].real, ve[4].real, ve[5].real, ve[6].real, ve[7].real)
    }
    GlobalStorage.orbitals.append(orbital_data)

def clear_orbitals():
    '''
    Deletes the all saved orbital configurations.
    This is useful for managing memory and state history.
    '''
    obj = logic.getCurrentController().owner

    GlobalStorage.orbitals.clear()

GlobalControllerManager.save_orbital_function = save_orbital
GlobalControllerManager.clear_orbitals_function = clear_orbitals