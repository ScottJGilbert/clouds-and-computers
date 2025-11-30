import numpy as np
import math
from scipy.special import genlaguerre, sph_harm_y
from numpy.typing import NDArray

a = 5.29177210903e-11  # Bohr Radius in meters
hbar = 1.054571817e-34  # Reduced Planck's constant in J·s
m_e = 9.10938356e-31  # Electron mass in kg

'''
For hydrogen-like atomic orbitals!
'''

def wavefunction(r: NDArray[np.float64], theta: NDArray[np.float64], phi: NDArray[np.float64], n: int, l: int, m: int):
    """Calculate the hydrogen-like atomic orbital wavefunction value at given spherical coordinates.

    Args:
        r (NDArray[np.float64]): Radial distances from the nucleus.
        theta (NDArray[np.float64]): Polar angles (0 to pi).
        phi (NDArray[np.float64]): Azimuthal angles (0 to 2pi).
        n (int): Principal quantum number.
        l (int): Azimuthal quantum number.
        m (int): Magnetic quantum number.

    Returns:
        complex: Value of the wavefunction at the given coordinates.
    """

    over_n = (2) / (n * a)

    square_root = math.sqrt(over_n * (math.factorial(n - l - 1) / (2 * n * (math.factorial(n + l)) ** 3)))
    
    exponential = math.exp(-r / (n * a))

    power = (over_n * r) ** l

    L = genlaguerre(n - l - 1, 2 * l + 1)
    # laguerre = laguerre_polynomial((2 * r) / (n * a), n, l)

    radial_component = square_root * power * exponential * L((2 * r) / (n * a))

    angular_component = sph_harm_y(l, m, theta, phi) # type: ignore

    return radial_component * angular_component

# ...existing code...
def guiding_equation(r: NDArray[np.float64], theta: NDArray[np.float64], phi: NDArray[np.float64],
                     n: int, l: int, m: int):
    """Calculate the guiding equation (probability current) for the hydrogen-like atomic orbital.

    Args:
        r (NDArray[np.float64]): Radial distances from the nucleus.
        theta (NDArray[np.float64]): Polar angles (0 to pi).
        phi (NDArray[np.float64]): Azimuthal angles (0 to 2pi).
        n (int): Principal quantum number.
        l (int): Azimuthal quantum number.
        m (int): Magnetic quantum number.
    Returns:
        NDArray[np.float64]: Velocity components (v_r, v_theta, v_phi)
    """
    psi = wavefunction(r, theta, phi, n, l, m)  # expected shape (Nr, Ntheta, Nphi), complex
    psi_conj = np.conj(psi)

    # derivatives: return tuple (d/dr, d/dtheta, d/dphi)
    dpsi_dr, dpsi_dtheta, dpsi_dphi = np.gradient(psi, r, theta, phi, axis=(0, 1, 2), edge_order=2)

    # probability current components in spherical coords
    j_r = (hbar / m_e) * np.imag(psi_conj * dpsi_dr)
    j_theta = (hbar / m_e) * np.imag(psi_conj * (1.0 / r[:, None, None]) * dpsi_dtheta)
    # broadcast 1/(r*sin(theta)) over grid
    inv_r_sin = 1.0 / (r[:, None, None] * np.sin(theta)[None, :, None])
    j_phi = (hbar / m_e) * np.imag(psi_conj * inv_r_sin * dpsi_dphi)

    prob_density = np.abs(psi) ** 2
    eps = 1e-20
    safe_den = np.where(prob_density <= eps, np.nan, prob_density)  # or use eps instead of nan

    v_r = j_r / safe_den
    v_theta = j_theta / safe_den
    v_phi = j_phi / safe_den

    return v_r, v_theta, v_phi
# ...existing code...

# def guiding_equation(r: NDArray[np.float64], theta: NDArray[np.float64], phi: NDArray[np.float64], n: int, l: int, m: int):
#     """Calculate the guiding equation (probability current) for the hydrogen-like atomic orbital.

#     Args:
#         r (NDArray[np.float64]): Radial distances from the nucleus.
#         theta (NDArray[np.float64]): Polar angles (0 to pi).
#         phi (NDArray[np.float64]): Azimuthal angles (0 to 2pi).
#         n (int): Principal quantum number.
#         l (int): Azimuthal quantum number.
#         m (int): Magnetic quantum number.
#     Returns:
#         NDArray[np.float64]: Velocity components (v_r, v_theta, v_phi)
#     """

#     psi = wavefunction(r, theta, phi, n, l, m)
#     psi_conj = np.conj(psi)

#     # Gradient of the wavefunction
#     # Note: This is a simplified version and may not be accurate for all cases.
#     dpsi_dr = np.gradient(psi, r, edge_order=2)
#     dpsi_dtheta = np.gradient(psi, theta, edge_order=2)
#     dpsi_dphi = np.gradient(psi, phi, edge_order=2)

#     # Probability current components
#     j_r = (hbar / m_e) * np.imag(psi_conj * dpsi_dr)
#     j_theta = (hbar / m_e) * np.imag(psi_conj * (1/r) * dpsi_dtheta)
#     j_phi = (hbar / m_e) * np.imag(psi_conj * (1/(r * np.sin(theta))) * dpsi_dphi)

#     # Probability density
#     prob_density = np.abs(psi) ** 2

#     # Velocity components
#     v_r = j_r / prob_density
#     v_theta = j_theta / prob_density
#     v_phi = j_phi / prob_density

#     return v_r, v_theta, v_phi


def wavefunction_superposition_multiple(r: NDArray[np.float64], theta: NDArray[np.float64], phi: NDArray[np.float64],
                                        quantum_numbers: list[tuple[int, int, int]]):
    """Calculate the combined wavefunction for a given number of hydrogen-like orbitals.
    
    Args:
        r, theta, phi (NDArray[np.float64]): Radial and angular coordinates.
        quantum_numbers (list): List of tuples, each containing the quantum numbers (n, l, m) for an orbital.

    Returns:
        complex: Combined wavefunction at the given coordinates.
    """
    total_wavefunction = np.zeros_like(r, dtype=complex)  # Initialize with zeroes to sum the wavefunctions
    
    # Sum up the wavefunctions for each orbital
    for (n, l, m) in quantum_numbers:
        total_wavefunction += wavefunction(r, theta, phi, n, l, m)
    
    return total_wavefunction

def guiding_equation_superposition_multiple(r: NDArray[np.float64], theta: NDArray[np.float64], phi: NDArray[np.float64],
                                           quantum_numbers: list[tuple[int, int, int]]):
    """Calculate the guiding equation for the superposition of multiple hydrogen-like orbitals.
    
    Args:
        r, theta, phi (NDArray[np.float64]): Radial and angular coordinates.
        quantum_numbers (list): List of tuples, each containing the quantum numbers (n, l, m) for an orbital.
        
    Returns:
        NDArray[np.float64]: Velocity components (v_r, v_theta, v_phi).
    """
    psi = wavefunction_superposition_multiple(r, theta, phi, quantum_numbers)  # combined wavefunction
    psi_conj = np.conj(psi)
    
    # Compute the gradients
    dpsi_dr, dpsi_dtheta, dpsi_dphi = np.gradient(psi, r, theta, phi, axis=(0, 1, 2), edge_order=2)
    
    # Probability current components
    j_r = (hbar / m_e) * np.imag(psi_conj * dpsi_dr)
    j_theta = (hbar / m_e) * np.imag(psi_conj * (1.0 / r[:, None, None]) * dpsi_dtheta)
    inv_r_sin = 1.0 / (r[:, None, None] * np.sin(theta)[None, :, None])
    j_phi = (hbar / m_e) * np.imag(psi_conj * inv_r_sin * dpsi_dphi)
    
    # Probability density
    prob_density = np.abs(psi) ** 2
    eps = 1e-20
    safe_den = np.where(prob_density <= eps, np.nan, prob_density)  # to avoid division by zero
    
    # Velocity components
    v_r = j_r / safe_den
    v_theta = j_theta / safe_den
    v_phi = j_phi / safe_den

    return v_r, v_theta, v_phi
