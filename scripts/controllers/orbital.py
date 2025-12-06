from bge import logic
import numpy as np
from numpy.typing import NDArray
from scripts.global_manager import GlobalConstants
# from scripts.global_manager import GlobalControllerManager
from wavefunction import wavefunction_superposition_multiple, guiding_equation_superposition_multiple

def reshape_orbital() -> None:
    '''
    Reshapes the orbital according to specific parameters.
    This is useful for visualizing different orbital configurations.
    '''
    obj = logic.getCurrentController().owner
    blender_obj = obj.blenderObject

    orbital_data = logic.globalDict.get("orbitals", [])

    pys = blender_obj.particle_systems[0]

    ps = pys.particles

    density_positions = create_density_plot([(data["n"], data["l"], data["m"]) for data in orbital_data])

    for i, particle in enumerate(ps):
        if i < len(density_positions):
            particle.location = density_positions[i].tolist()

def create_density_plot(quantum_numbers: list[tuple[int, int, int]]) -> NDArray[np.float64]:
    '''
    Creates a density plot for the orbital particles.
    This is useful for visualizing particle distributions.
    '''
    positions: NDArray[np.float64] = np.zeros((GlobalConstants.num_particles, 3))

    num_particles = 0

    while (num_particles < GlobalConstants.num_particles):
        # Generate random spherical coordinates
        r = np.random.uniform(0, 1)
        theta = np.random.uniform(0, np.pi)
        phi = np.random.uniform(0, 2 * np.pi)

        r_array = np.array([r])
        theta_array = np.array([theta])
        phi_array = np.array([phi])

        probability = wavefunction_superposition_multiple(r_array, theta_array, phi_array, quantum_numbers)[0] ** 2

        random_value = np.random.uniform(0, 1)

        if random_value > probability:
            continue  # Reject this point

        # Convert to Cartesian coordinates
        x = r * np.sin(theta) * np.cos(phi)
        y = r * np.sin(theta) * np.sin(phi)
        z = r * np.cos(theta)

        positions[num_particles] = [x, y, z]

        num_particles += 1
    
    return positions

def apply_velocity_to_orbital() -> None:
    '''
    Applies velocity to the orbital particles.
    This is useful for simulating orbital dynamics.
    '''
    obj = logic.getCurrentController().owner
    blender_obj = obj.blenderObject

    orbital_data = logic.globalDict.get("orbitals", [])

    # Access the particle system
    pys = blender_obj.particle_systems[0]

    if not pys:
        return

    ps = pys.particles

    if ps.count == 0:
        return

    positions = np.array([particle.location for particle in ps])
    spherical_positions = cartesian_to_spherical(positions[:, 0], positions[:, 1], positions[:, 2])

    velocities = guiding_equation_superposition_multiple(
        spherical_positions[0], spherical_positions[1], spherical_positions[2], [(data["n"], data["l"], data["m"]) for data in orbital_data])

    cartesian_velocities = np.zeros_like(velocities)
    for i in range(len(velocities[0])):
        r, theta, phi = spherical_positions[0][i], spherical_positions[1][i], spherical_positions[2][i]
        v_r, v_theta, v_phi = velocities[0][i], velocities[1][i], velocities[2][i]

        # Convert spherical velocity to Cartesian velocity
        vx = (np.sin(theta) * np.cos(phi)) * v_r + (np.cos(theta) * np.cos(phi)) * v_theta - (np.sin(phi)) * v_phi
        vy = (np.sin(theta) * np.sin(phi)) * v_r + (np.cos(theta) * np.sin(phi)) * v_theta + (np.cos(phi)) * v_phi
        vz = (np.cos(theta)) * v_r - (np.sin(theta)) * v_theta

        cartesian_velocities[i] = [vx, vy, vz]

    # Apply velocities to particles
    for i, particle in enumerate(ps):
        particle.position += cartesian_velocities[i].tolist() * GlobalConstants.timestep
    
def cartesian_to_spherical(x: NDArray[np.float64], y: NDArray[np.float64], z: NDArray[np.float64]) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Convert Cartesian coordinates to spherical coordinates.
    
    Args:
        x, y, z (NDArray[np.float64]): Cartesian coordinates.
        
    Returns:
        r, theta, phi (NDArray[np.float64]): Spherical coordinates.
    """
    r = np.sqrt(x**2 + y**2 + z**2)
    theta = np.arccos(z / r)  # polar angle
    phi = np.arctan2(y, x)    # azimuthal angle
    return r, theta, phi

def spherical_to_cartesian(r: NDArray[np.float64], theta: NDArray[np.float64], phi: NDArray[np.float64]) -> tuple[NDArray[np.float64], NDArray[np.float64], NDArray[np.float64]]:
    """Convert spherical coordinates to Cartesian coordinates.
    
    Args:
        r, theta, phi (NDArray[np.float64]): Spherical coordinates.
        
    Returns:
        x, y, z (NDArray[np.float64]): Cartesian coordinates.
    """
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z