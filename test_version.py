import pyglet
import moderngl
import numpy as np


# print(moderngl.create_context().version_code)

# Dimensioni della finestra
WIDTH, HEIGHT = 512, 512

# Creazione di una finestra Pyglet
window = pyglet.window.Window(WIDTH, HEIGHT, "Compute Shader Example")

# Contesto moderngl
ctx = moderngl.create_context()

print(moderngl.create_context().version_code)
