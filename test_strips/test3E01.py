import pyglet
from pyglet.gl import *
from ctypes import POINTER, c_float
import numpy as np

class PygletGridWindow(pyglet.window.Window):
    def __init__(self, width, height, grid_width, grid_height, rect_width, rect_height):
        super().__init__(width=width, height=height, caption="Grid with TRIANGLE_STRIP")

        # Dimensioni della griglia
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.rect_width = rect_width
        self.rect_height = rect_height

        # Genera i vertici della griglia
        self.vertices = self.create_grid()

        # Crea un Vertex Buffer Object (VBO) per i vertici
        self.vertex_vbo = GLuint()
        glGenBuffers(1, self.vertex_vbo)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices.ctypes.data_as(POINTER(c_float)), GL_STATIC_DRAW)

    def create_grid(self):
        """
        Crea i vertici della griglia con linee per il wireframe.
        Ogni vertice ha formato (x, y, z).
        """
        grid_w = self.grid_width
        grid_h = self.grid_height

        # Convertire le dimensioni del rettangolo in coordinate normalizzate rispetto alla finestra
        half_rect_w = self.rect_width / 2.0
        half_rect_h = self.rect_height / 2.0

        x_vals = np.linspace(-half_rect_w / self.width, half_rect_w / self.width, grid_w + 1)
        y_vals = np.linspace(-half_rect_h / self.height, half_rect_h / self.height, grid_h + 1)

        vertices = []

        # Linee orizzontali
        for y in range(grid_h + 1):
            for x in range(grid_w):
                vertices.append((x_vals[x], y_vals[y], 0.0))
                vertices.append((x_vals[x + 1], y_vals[y], 0.0))

        # Linee verticali
        for x in range(grid_w + 1):
            for y in range(grid_h):
                vertices.append((x_vals[x], y_vals[y], 0.0))
                vertices.append((x_vals[x], y_vals[y + 1], 0.0))

        return np.array(vertices, dtype='f4')

    def on_draw(self):
        """Disegna la griglia con linee."""
        self.clear()
        glClearColor(0.1, 0.1, 0.1, 1.0)

        # Imposta il colore del wireframe
        glColor3f(1.0, 1.0, 1.0)

        # Abilita gli array di vertici
        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_vbo)
        glVertexPointer(3, GL_FLOAT, 0, None)

        # Disegna la griglia
        glDrawArrays(GL_LINES, 0, len(self.vertices))

        # Disabilita gli array di vertici
        glDisableClientState(GL_VERTEX_ARRAY)

if __name__ == "__main__":
    window = PygletGridWindow(600, 400, grid_width=60, grid_height=40, rect_width=500, rect_height=300)
    pyglet.app.run()
