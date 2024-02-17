import ctypes
import numpy as np

# Load the C library
lib = ctypes.CDLL("./libdiskaccretion.so")

# Define the Particle struct
class Particle(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double),
                ("y", ctypes.c_double),
                ("vx", ctypes.c_double),
                ("vy", ctypes.c_double)]

# Function to generate the initial state of the accretion disk
def generate_disk(N_PARTICLES):
    particles = (Particle * N_PARTICLES)()  # Create an array of particles

    # Define the disk parameters
    DISK_RADIUS = 1.0e6  # Radius of the disk

    for i in range(N_PARTICLES):
        # Sample random radial distance within the disk region
        r = np.random.uniform(0, DISK_RADIUS)
        # Sample random angle
        theta = np.random.uniform(0, 2*np.pi)
        # Convert polar coordinates to Cartesian coordinates
        particles[i].x = r * np.cos(theta)
        particles[i].y = r * np.sin(theta)
        # Randomly assign velocities
        particles[i].vx = np.random.normal(0, 1)
        particles[i].vy = np.random.normal(0, 1)

    return particles

# Function to run the simulation
def run_simulation(N_PARTICLES, SIMULATION_DURATION, dt):
    # Generate the initial state of the accretion disk
    particles = generate_disk(N_PARTICLES)

    # Simulation variables
    time = 0
    iteration = 0

    # Run the simulation
    while iteration < SIMULATION_DURATION:
        # Open file for writing particle data for this iteration
        filename = f"./simulationdata/particle_data_iteration_{iteration}.txt"
        with open(filename, "w") as file:
            # Calculate gravitational and pressure forces on each particle
            for i in range(N_PARTICLES):
                r = np.sqrt(particles[i].x * particles[i].x + particles[i].y * particles[i].y)
                fx, fy = ctypes.c_double(0), ctypes.c_double(0)  # Initialize forces as ctypes doubles
                lib.calculate_forces(ctypes.byref(particles[i]), ctypes.c_double(r), ctypes.byref(fx), ctypes.byref(fy))
                # Integrate equations of motion using RK4
                lib.integrate_particle(ctypes.byref(particles[i]), ctypes.c_double(dt), fx, fy, ctypes.c_double(1.0))  # Assuming unit particle mass

                # Write particle data to file for this iteration
                file.write(f"{particles[i].x} {particles[i].y} {particles[i].vx} {particles[i].vy}\n")
        
        # Update time and iteration count
        time += dt
        iteration += 1
        print(f'tempo:: {time}, iteração:: {iteration}')

if __name__ == "__main__":
    N_PARTICLES = 32000
    SIMULATION_DURATION = 5000
    dt = 1/5000

    run_simulation(N_PARTICLES, SIMULATION_DURATION, dt)
