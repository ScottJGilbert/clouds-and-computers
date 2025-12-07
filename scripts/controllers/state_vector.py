from bge import logic
from scripts.global_manager import GlobalConstants
# from scripts.global_manager import GlobalControllerManager
import numpy as np
from numpy.typing import NDArray
from math import sin, cos, asin

def align_state_vector() -> None:
    '''
    Aligns the state vector to a specific basis.
    This is useful for preparing states for measurement.
    '''
    obj = logic.getCurrentController().owner
    blender_obj = obj.blenderObject

    # Rotate the state vector to the desired location around the global origin
    ve: NDArray[np.float64] = logic.globalDict.get("state_vector", np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]))

    [rx, ry, rz] = blender_obj.rotation_euler # type: ignore
    
    material = blender_obj.active_material # Get the first material
    color = material.diffuse_color  # Access the diffuse color

    cmyka_color = convert_rgba_to_cmyka(color)

    old_vector: NDArray[np.float64] = np.zeros_like(ve)
    old_vector[0] = -sin(ry)
    old_vector[1] = cos(ry)*sin(rx)
    old_vector[2] = cos(ry)*cos(rx)
    old_vector[3] = cmyka_color[0]
    old_vector[4] = cmyka_color[1]
    old_vector[5] = cmyka_color[2]
    old_vector[6] = cmyka_color[3]
    old_vector[7] = cmyka_color[4]

    difference_vector = ve - old_vector

    # Rotate the blender object slightly in the direction of the difference vector
    adjustment_factor = GlobalConstants.timestep * 5.0  # Small adjustment factor

    new_ve = old_vector + (difference_vector * adjustment_factor)

    new_rotation = (
        asin(new_ve[1]/cos(asin(-new_ve[0]))),
        -asin(new_ve[0]),
        blender_obj.rotation_euler[2]  # Keep the z-rotation unchanged
    )

    blender_obj.rotation_euler = new_rotation

    new_rgba_color = (
        1 - (new_ve[3] * (1 - new_ve[6])),
        1 - (new_ve[4] * (1 - new_ve[6])),
        1 - (new_ve[5] * (1 - new_ve[6])),
        new_ve[7]
    )

    material.diffuse_color = new_rgba_color


def convert_rgba_to_cmyka(rgba: tuple[float, float, float, float]) -> tuple[float, float, float, float, float]:
    '''
    Converts RGBA color to CMYKA color space.
    This is useful for color representation in different models.
    '''
    r, g, b, a = rgba
    if (r == 0 and g == 0 and b == 0):
        return (0, 0, 0, 1, a)

    c = 1 - r
    m = 1 - g
    y = 1 - b

    k = min(c, m, y)

    c = (c - k) / (1 - k) if (1 - k) != 0 else 0
    m = (m - k) / (1 - k) if (1 - k) != 0 else 0
    y = (y - k) / (1 - k) if (1 - k) != 0 else 0

    return (c, m, y, k, a)

