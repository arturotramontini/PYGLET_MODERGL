import tkinter as tk
from tkinter import Canvas
import moderngl
import numpy as np
from PIL import Image, ImageTk


class OpenGLCanvas(Canvas):
    def __init__(self, master, width, height, **kwargs):
        super().__init__(master, width=width, height=height, **kwargs)
        self.width = width
        self.height = height

        # Integrazione Tkinter con OpenGL
        self.bind("<Configure>", self.resize)
        self.bind("<Expose>", self.draw)

        self.init_opengl()

    def init_opengl(self):
        # Crea un contesto OpenGL
        self.ctx = moderngl.create_standalone_context()

        # Definisce il viewport iniziale
        self.ctx.viewport = (0, 0, self.width, self.height)

        # Programma vertex e fragment shader
        self.program = self.ctx.program(
            vertex_shader="""
            #version 330
            in vec2 in_position;
            in vec3 in_color;
            out vec3 color;
            void main() {
                gl_Position = vec4(in_position, 0.0, 1.0);
                color = in_color;
            }
            """,
            fragment_shader="""
            #version 330
            in vec3 color;
            out vec4 fragColor;
            void main() {
                fragColor = vec4(color, 1.0);
            }
            """,
        )

        # Dati per un quadrato
        vertices = np.array([
            # Posizione       # Colore
            -0.5, -0.5,       1.0, 0.0, 0.0,  # Rosso
             0.5, -0.5,       0.0, 1.0, 0.0,  # Verde
            -0.5,  0.5,       0.0, 0.0, 1.0,  # Blu
             0.5,  0.5,       1.0, 1.0, 0.0,  # Giallo
        ], dtype='f4')

        self.vbo = self.ctx.buffer(vertices.tobytes())
        self.vao = self.ctx.simple_vertex_array(
            self.program, self.vbo, 'in_position', 'in_color'
        )

        # Buffer per l'immagine finale
        self.image_buffer = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture((self.width, self.height), 4)]
        )

    def resize(self, event):
        # Gestisce il resize della finestra
        self.width, self.height = event.width, event.height
        self.ctx.viewport = (0, 0, self.width, self.height)
        self.image_buffer = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture((self.width, self.height), 4)]
        )
        self.draw()

    def draw(self, event=None):
        # Renderizza la scena OpenGL
        self.image_buffer.use()
        self.ctx.clear(0.0, 0.0, 0.0, 1.0)
        self.vao.render(moderngl.TRIANGLE_STRIP)

        # Legge i pixel dal buffer
        data = self.image_buffer.read(components=3)
        image = Image.frombytes('RGB', (self.width, self.height), data)
        image = image.transpose(Image.FLIP_TOP_BOTTOM)

        # Mostra l'immagine nel canvas Tkinter
        self.tk_image = ImageTk.PhotoImage(image)
        self.create_image(0, 0, image=self.tk_image, anchor=tk.NW)


# Configura la finestra principale
root = tk.Tk()
root.title("Tkinter + ModernGL")

canvas = OpenGLCanvas(root, width=512, height=512, bg="black")
canvas.pack(fill=tk.BOTH, expand=True)

root.mainloop()
