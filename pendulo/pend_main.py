import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ctypes

lib = ctypes.CDLL('./libpendulum.so')
lib.pendulum_edo.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_double]
pendulum_ode = lib.pendulum_edo
num_series =  1

def rk4_step(y, t, dt, ode_func):
    """
    Perform a single step of the Runge-Kutta 4th order method.

    Parameters:
        y: Current state vector.
        t: Current time.
        dt: Time step.
        ode_func: Function defining the Ordinary Differential Equations (ODEs).

    Returns:
        Updated state vector after a single step.
    """
    k1 = ode_func(y, t)
    y_value = y.contents.value  # Dereference y to access its value
    k2 = ode_func(ctypes.c_double(y_value + k1 * dt / 2), t + dt / 2)  # Create a new c_double instance with the result
    k3 = ode_func(ctypes.c_double(y_value + k2 * dt / 2), t + dt / 2)  # Create a new c_double instance with the result
    k4 = ode_func(ctypes.c_double(y_value + k3 * dt), t + dt)  # Create a new c_double instance with the result
    return y_value + (k1 + 2 * k2 + 2 * k3 + k4) * dt / 6



def process_data(file_path):
    data = pd.read_csv(file_path, header=None, names=["theta", "omega"])
    y = np.array([data.iloc[0]["theta"], data.iloc[0]["omega"]], dtype=np.float64)
    dt = 0.4/len(data) # Example value for the time step

    theta_values = []  # List to store theta values for plotting
    omega_values = []  # List to store omega values for plotting

    for t in range(len(data)):
        # Apply angle wrapping to y[0] which contains theta
        y[0] = (y[0] + np.pi) % (2 * np.pi) - np.pi

        # Convert the numpy array to ctypes pointer
        y_ptr = y.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

        # Call the RK4 step function with the ctypes pointer to the numpy array
        rk4_step(y_ptr, t * dt, dt, pendulum_ode)

        # Optionally, you can retrieve the updated values from the ctypes array
        # Note: This assumes that pendulum_ode modifies the values in-place
        y = np.ctypeslib.as_array(y_ptr, shape=(2,))

        # Append theta and omega values for plotting
        theta_values.append(y[0])
        omega_values.append(y[1])

    # Plotting
    plt.plot(range(len(data)), theta_values, label="Theta")
    plt.plot(range(len(data)), omega_values, label="Omega")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.title("Processed Data")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    lib.generate_pendulums()
    # Loop para processar os arquivos CSV gerados pelo programa em C
    for i in range(num_series):
        file_path = f"./dataset/pendulum_{i}.csv"
        process_data(file_path)