import ctypes
import numpy as np
import matplotlib.pyplot as plt

# Carregar a biblioteca compartilhada
lib = ctypes.CDLL('./libtextwrite.so')

# Definir o tipo de dados para as entradas e saídas da função C
lib.writingAFile.restype = None
lib.writingAFile.argtypes = [ctypes.c_char_p]

text = input()
text_bytes = text.encode('utf-8')

lib.writingAFile(text_bytes)

print("--------------\n\n\n")
print(lib.readingAFile())
