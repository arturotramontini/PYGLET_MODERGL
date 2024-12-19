import pyglet
import moderngl
import numpy as np

from pyglet import gl


class PygletDynamicColor(pyglet.window.Window):
    def __init__(self, width, height):
        super().__init__(width=width, height=height, caption="Dynamic Uniform Color")

        # Creazione del contesto ModernGL
        self.ctx = moderngl.create_context()

        # Vertici del TRIANGLE_STRIP
        self.vertices = np.array([
            -0.5, -0.5, 0.0,  # Vertice 1
             0.5, -0.5, 0.0,  # Vertice 2
            -0.5,  0.5, 0.0,  # Vertice 3
             0.5,  0.5, 0.0   # Vertice 4
        ], dtype='f4')

        # Buffer per i vertici
        self.vbo = self.ctx.buffer(self.vertices.tobytes())

        # Programma GLSL con uniform per il colore
        self.program = self.ctx.program(
            vertex_shader='''
            #version 330
            in vec3 in_vert;
            void main() {
                gl_Position = vec4(in_vert, 1.0);
            }
            ''',
            fragment_shader='''
            #version 330
            uniform vec2 u_resolution;            
            uniform vec3 color;
            out vec4 fragColor;
            void main() {
                fragColor = vec4(color, 1.0);
            }
            '''
        )

        # Creazione del VAO
        self.vao = self.ctx.simple_vertex_array(self.program, self.vbo, 'in_vert')

        # Inizializzazione del colore uniforme
        self.program['color'] = (1.0, 0.0, 0.0)  # Rosso iniziale

        # self.program['u_resolution'] = (800., 600.) # float(width),float(height))  # dimensioni finestra

    def on_draw(self):
        """Renderizza la scena nella finestra."""
        self.clear()
        # Aggiorna dinamicamente il colore (ad esempio oscillando nel tempo)
        time = pyglet.clock.get_default().time()
        self.program['color'] = (np.abs(np.sin(time)), np.abs(np.cos(time)), 0.5)
        self.vao.render(moderngl.TRIANGLE_STRIP)


if __name__ == "__main__":
    # Avvia la finestra
    window = PygletDynamicColor(800, 600)
    pyglet.app.run()
