import ctypes
import os
import matplotlib.pyplot as plt
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))

lib = ctypes.CDLL(os.path.join(script_dir, 'libcolumb.so'))

lib.columbForce.restype = ctypes.c_double
lib.columbForce.argtypes = (ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double)

d1 = float(input("Enter value for d1: "))
d2 = float(input("Enter value for d2: "))
q1 = float(input("Enter value for q1: "))
q2 = float(input("Enter value for q2: "))

case_type = int(input())

if int(case_type)==4:
    i=d1
    distant = []
    result = []
    for i in np.arange(d1, d2 * 3, 0.05):
        r = abs(d2 - d1)
        print(r)
        d2 = d2 + i
        force = lib.columbForce(case_type, d1, d2, q1, q2, r)
        print(force)
        result.append(force)
        distant.append(i)
    plt.plot(distant, result, label='Força eletrica pela distancia:')
    plt.xlabel('Distancia')
    plt.ylabel('Força')
    plt.show()
else:
    result = lib.columbForce(case_type,d1, d2, q1, q2, 0)
    print("Coulomb force:", result)
