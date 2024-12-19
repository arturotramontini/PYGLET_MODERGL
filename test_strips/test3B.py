import pyglet
from pyglet.gl import *
from ctypes import POINTER, c_float
import numpy as np

class PygletGridWindow(pyglet.window.Window):
    def __init__(self, width, height, grid_width, grid_height):
        super().__init__(width=width, height=height, caption="Grid with TRIANGLE_STRIP")

        # Dimensioni della griglia
        self.grid_width = grid_width
        self.grid_height = grid_height

        # Genera i vertici della griglia
        self.vertices = self.create_grid()

        # Crea un Vertex Buffer Object (VBO) per i vertici
        self.vertex_vbo = GLuint()
        glGenBuffers(1, self.vertex_vbo)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices.ctypes.data_as(POINTER(c_float)), GL_STATIC_DRAW)

    def create_grid(self):
        """
        Crea i vertici della griglia con TRIANGLE_STRIP.
        Ogni vertice ha formato (x, y, z).
        """
        grid_w = self.grid_width
        grid_h = self.grid_height

        # Calcolo della griglia in coordinate normalizzate (-1 a 1)
        x_vals = np.linspace(-1.0, 1.0, grid_w + 1)
        y_vals = np.linspace(-1.0, 1.0, grid_h + 1)

        vertices = []

        for y in range(grid_h):
            for x in range(grid_w + 1):
                # Vertice inferiore
                vertices.append((x_vals[x], y_vals[y], 0.0))
                # Vertice superiore
                vertices.append((x_vals[x], y_vals[y + 1], 0.0))

        return np.array(vertices, dtype='f4')

    def on_draw(self):
        """Disegna la griglia con TRIANGLE_STRIP."""
        self.clear()
        glClearColor(0.1, 0.1, 0.1, 1.0)

        # Abilita gli array di vertici
        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_vbo)
        glVertexPointer(3, GL_FLOAT, 0, None)

        # Disegna la griglia
        glDrawArrays(GL_TRIANGLE_STRIP, 0, len(self.vertices))

        # Disabilita gli array di vertici
        glDisableClientState(GL_VERTEX_ARRAY)

if __name__ == "__main__":
    window = PygletGridWindow(800, 600, grid_width=600, grid_height=400)
    pyglet.app.run()
