import pyglet
import moderngl
import numpy as np
import time
import math

class PygletModernglWithShaders(pyglet.window.Window):
    def __init__(self, width, height, grid_width, grid_height):
        super().__init__(width=width, height=height, caption="Grid with External Shaders")

        # Creazione del contesto ModernGL
        self.ctx = moderngl.create_context()

        # Generazione della griglia
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.vertices = self.create_grid()

        # Creazione del Vertex Buffer Object (VBO)
        self.vbo = self.ctx.buffer(self.vertices.tobytes())


        # Carica gli shader dai file
        vertex_shader = self.load_shader("vertex_shader.glsl")
        fragment_shader = self.load_shader("fragment_shader.glsl")


        self.program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        # Creazione del Vertex Array Object (VAO)
        self.vao = self.ctx.simple_vertex_array(
            # self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader),
            self.program,    
            self.vbo,
            'in_vert'
        )

        # Imposta valori iniziali delle uniform
        self.program['offset'] = (0.1, 0.0, 0.0)  # Offset iniziale
        self.program['color'] = (0.2, 0.6, 0.8)  # Colore iniziale



    def create_grid(self):
        """Crea i vertici della griglia con TRIANGLE_STRIP."""
        x_vals = np.linspace(-0.7, 0.7, self.grid_width + 1)
        y_vals = np.linspace(-0.7, 0.7, self.grid_height + 1)

        vertices = []
        for y in range(self.grid_height):
            for x in range(self.grid_width + 1):
                # Vertice inferiore
                vertices.append((x_vals[x], y_vals[y], 0.0))
                # Vertice superiore
                vertices.append((x_vals[x], y_vals[y + 1], 0.0))

        return np.array(vertices, dtype='f4')

    def load_shader(self, file_path):
        """Carica il contenuto di uno shader da un file."""
        with open(file_path, 'r') as file:
            return file.read()

    def on_draw(self):
        """Disegna la griglia."""
        self.clear()
        self.ctx.clear(0.1, 0.1, 0.1)
        self.vao.render(moderngl.TRIANGLE_STRIP)

        # Aggiorna dinamicamente le uniform (esempio)
        t = pyglet.clock.get_default().time()

        self.program['offset'] = (np.sin(t), 0.0, 0.0)  # Muove lungo X
        self.program['color'] = ( math.fabs(np.sin(t)), 0.5, 0.5)  # Cambia colore



if __name__ == "__main__":
    window = PygletModernglWithShaders(600, 600, grid_width=40, grid_height=40)

    t1 = time.time()
    t = pyglet.clock.get_default().time()
    print (t1,t)

    pyglet.app.run()
