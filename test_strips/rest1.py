import pyglet
import moderngl
import numpy as np

import time

class PygletModernglWindow(pyglet.window.Window):
    def __init__(self, width, height, title):
        super().__init__(width=width, height=height, caption=title,vsync=False)

        self.F01 = False

        # Creazione del contesto moderngl
        self.ctx = moderngl.create_context()
        # Dati di esempio: un semplice triangolo
        vertices = np.array([
            -0.6, -0.6, 0.0,  # Vertice 1
             0.6, -0.6, 0.0,  # Vertice 2
             0.0,  0.6, 0.0   # Vertice 3
        ], dtype='f4')

        # Buffer dei vertici
        self.vbo = self.ctx.buffer(vertices.tobytes())
        # Creazione di un Vertex Array Object (VAO)
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
                    fragColor = vec4(1.0, 0.5, 0.2, 1.0);
                }
                '''
            ),
            self.vbo,
            'in_vert'
        )

    def on_draw(self):

        if self.F01:
            
            self.F01 = False
            
            print(time.time())

            # Pulizia dello schermo
            self.clear()
            self.ctx.clear(0.1, 0.2, 0.3)  # Colore di sfondo
            # Disegno del triangolo
            self.vao.render(moderngl.TRIANGLES)



    def on_key_press(self,symbol, modifiers):
        
        print(symbol)
        
        if symbol == pyglet.window.key.A :
            print('chiedo redraw')
            self.F01 = True
            self.dispatch_event('on_draw')

        if symbol == pyglet.window.key.ESCAPE :
            print('fine programma')
            self.close()
        pass  


if __name__ == "__main__":
    window = PygletModernglWindow(800, 800, "Pyglet + ModernGL")
    pyglet.app.run()
