# import moderngl
# import numpy as np
# from pyrr import Matrix44

# import pyglet
# import pyglet.window.key


# # Crea un contesto moderngl
# ctx = moderngl.create_standalone_context()

# # Crea un programma shader
# prog = ctx.program(
#     vertex_shader="""
#     #version 330 core
#     uniform mat4 mvp;
#     in vec3 in_position;
#     void main() {
#         gl_Position = mvp * vec4(in_position, 1.0);
#     }
#     """,
#     fragment_shader="""
#     #version 330 core
#     out vec4 fragColor;
#     void main() {
#         fragColor = vec4(1.0, 0.5, 0.2, 1.0);
#     }
#     """,
# )

# # Definisci i vertici di un triangolo
# vertices = np.array([
#     [-0.5, -0.5, 0.0],
#     [0.5, -0.5, 0.0],
#     [0.0, 0.5, 0.0],
# ], dtype='f4')

# # Crea un Vertex Buffer Object
# vbo = ctx.buffer(vertices.tobytes())

# # Configura il Vertex Array Object
# vao = ctx.simple_vertex_array(prog, vbo, 'in_position')

# # Crea matrici
# projection = Matrix44.orthogonal_projection(-1, 1, -1, 1, -1, 1)
# angle = np.radians(45)
# rotation = Matrix44.from_y_rotation(angle)
# transformation = projection @ rotation

# # Scrivi la matrice agli shader
# prog['mvp'].write(transformation.astype('f4').tobytes())

# # Renderizza
# ctx.clear(1.0, 1.0, 1.0)
# vao.render(moderngl.TRIANGLES)


# Fend = False

# def on_key_press(symbol, modifiers):
#     print(symbol)
#     # if symbol == pyglet.window.key.A :
#     #     print('chiedo acquisizione frame con self.Ftone = True')
#     #     self.F01= True
#     #     self.dispatch_event('on_draw')            
#     #     self.Fone = True
#     #     self.dispatch_event('on_draw')            
#     if symbol == pyglet.window.key.ESCAPE :
#         Fend = True
#     pass  

# import time
# cnt = 0
# while not Fend:
#         cnt += 1
#         print(cnt)
#         time.sleep(0.2)

# print('fine programma')

import moderngl
import numpy as np
from pyrr import Matrix44
import pyglet
from pyglet.gl import *

# Configura la finestra
window = pyglet.window.Window(800, 600, "Moderngl Proiezione Ortografica", resizable=True)

# Contexto moderngl
ctx = moderngl.create_context()

# Crea un programma shader
prog = ctx.program(
    vertex_shader="""
    #version 330 core
    uniform mat4 mvp;
    in vec3 in_position;
    void main() {
        gl_Position = mvp * vec4(in_position, 1.0);
    }
    """,
    fragment_shader="""
    #version 330 core
    out vec4 fragColor;
    void main() {
        fragColor = vec4(1.0, 0.5, 0.2, 1.0);
    }
    """,
)

# Definisci i vertici di un triangolo
vertices = np.array([
    [-0.5, -0.5, 0.0],
    [0.5, -0.5, 0.0],
    [0.0, 0.5, 0.0],
], dtype='f4')

# Crea un Vertex Buffer Object
vbo = ctx.buffer(vertices.tobytes())

# Configura il Vertex Array Object
vao = ctx.simple_vertex_array(prog, vbo, 'in_position')

# Crea matrici iniziali
projection = Matrix44.orthogonal_projection(-1, 1, -1, 1, -1, 1)
angle = 0.0

@window.event
def on_draw():
    global angle
    window.clear()

    # Incrementa l'angolo di rotazione
    angle += 0.01

    # Crea la matrice di rotazione e combinazione
    rotation = Matrix44.from_y_rotation(angle)
    transformation = projection @ rotation

    # Scrivi la matrice allo shader
    prog['mvp'].write(transformation.astype('f4').tobytes())

    # Renderizza
    ctx.clear(1.0, 1.0, 1.0)
    vao.render(moderngl.TRIANGLES)

# Avvia il ciclo principale
pyglet.app.run()
