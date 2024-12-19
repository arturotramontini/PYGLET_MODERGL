import pyglet
import moderngl
import numpy as np

class PygletModernglGrid(pyglet.window.Window):
    def __init__(self, width, height, grid_width, grid_height):
        super().__init__(width=width, height=height, caption="Grid with TRIANGLE_STRIP")

        # Creazione del contesto ModernGL
        self.ctx = moderngl.create_context(wireframe=True)

        # Generazione della griglia
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.vertices = self.create_grid()

        # Creazione del Vertex Buffer Object (VBO)
        self.vbo = self.ctx.buffer(self.vertices.tobytes())

        # Creazione del Vertex Array Object (VAO)
        self.vao = self.ctx.simple_vertex_array(
            self.ctx.program(
                vertex_shader='''
                #version 330
                in vec3 in_vert;
                void main() {
                    gl_Position = vec4(in_vert, 1.0);
                }
                ''',
                fragment_shader='''
                #version 330
                out vec4 fragColor;
                void main() {
                    // fragColor = vec4(0.2, 0.6, 0.8, 1.0);
                    fragColor = vec4(0.2, 0.06, 0.08, 1.0);
                }
                '''
            ),
            self.vbo,
            'in_vert'
        )

    def create_grid(self):
        """
        Crea i vertici della griglia con TRIANGLE_STRIP.
        Ogni vertice ha formato (x, y, z).
        """
        grid_w = self.grid_width
        grid_h = self.grid_height

        # Calcolo della griglia in coordinate normalizzate (-1 a 1)
        x_vals = np.linspace(-.70, .70, grid_w + 1)
        y_vals = np.linspace(-.70, .70, grid_h + 1)

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
        self.ctx.clear(0.01, 0.01, 0.01)  # Colore di sfondo
        self.vao.render(moderngl.TRIANGLE_STRIP)

if __name__ == "__main__":
    window = PygletModernglGrid(600, 600, grid_width=40, grid_height=40)
    pyglet.app.run()
