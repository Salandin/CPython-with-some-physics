import numpy as np
import matplotlib.pyplot as plt
import ctypes

lib = ctypes.CDLL("./libradioactivedecay.so")
#lib.radioDecay.restype = ctypes.c_double
#lib.radioDecay.argtypes = (ctypes.c_double, ctypes.c_double, ctypes.c_double)
lib.simulateDecay.argtypes = (ctypes.c_double, ctypes.c_double, ctypes.c_double,
                               ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
lib.simulateDecay.restype = None
lib.simulateDecayWithNoise.argtypes = (ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,
                                        ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double))
lib.simulateDecayWithNoise.restype = None


#decay = lib.radioDecay
simulate_decay = lib.simulateDecay
simulate_decay_with_noise = lib.simulateDecayWithNoise

lamb = np.log(2)/3.0
N0 = 1500.0
max_timestep = 150

time_values_decay = np.zeros(150)
atom_values_decay = np.zeros(150)
time_values_noise = np.zeros(150)
atom_values_noise = np.zeros(150)

"""def simulate_decay(N0, lamb, dt = 0.723, time=0.0):
    time_values = []
    atom_values = []
    for i in range(max_timestep):
        N = decay(N0, lamb, time)
        time_values.append(time)
        atom_values.append(N)
        time += dt
    return time_values, atom_values

def simulate_decay_with_noise(N0, lamb,dt = 0.723, total_time=max_timestep):
    time = 0
    N = N0
    time_values = []
    atom_values = []
    while time < total_time and N > 0:
        decayed_fraction = np.random.exponential(lamb)
        decayed_atoms = N * decayed_fraction
        
        N -= decayed_atoms
        time_values.append(time)
        atom_values.append(N)
        time += dt
    return time_values, atom_values
"""       


if __name__ == "__main__":

    simulate_decay(N0, lamb, 0.723, time_values_decay.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                   atom_values_decay.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

    lib.simulateDecayWithNoise(N0, lamb, 0.723, max_timestep,
                            time_values_noise.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                            atom_values_noise.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

    
    plt.plot(time_values_decay, atom_values_decay, label='Decay')
    plt.plot(time_values_noise, atom_values_noise, label='Decay with Noise')
    plt.xlabel('Time')
    plt.ylabel('Number of Atoms')
    plt.title('Radioactive Decay with and without Noise')
    plt.legend()
    plt.show()