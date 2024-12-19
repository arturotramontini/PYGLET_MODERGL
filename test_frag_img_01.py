
# https://chatgpt.com/c/675d4d29-3254-8002-98bb-cabbac69385b


import moderngl
import pyglet
import pyglet.window.key
import numpy as np
from PIL import Image

import math
import time
import os

class FramebufferExample(pyglet.window.Window):
    def __init__(self, width, height):



        super().__init__(width=width, height=height, caption="Framebuffer Example",vsync=False)


        # --- per ricaricare fragment_shader quando lo modicico 
        # Path al fragment shader
        self.fragment_shader_path = "fragment_shader.glsl"

        # Timestamp di modifica iniziale
        self.last_modified = self.get_file_mod_time()
        # ------------


        self.set_location(50,900)

        self.width = width
        self.height = height    

        self.Fone = False
        self.F01 = True

        # Contexto ModernGLa
        self.ctx = moderngl.create_context()

        # # Crea una texture per immagazzinare il rendering
        # self.texture = self.ctx.texture((width, height), 4)
        # self.texture.filter = (moderngl.NEAREST, moderngl.NEAREST)

        # # Framebuffer offscreen
        # self.fbo = self.ctx.framebuffer(color_attachments=[self.texture])

        # Carica gli shader dai file
        self.vertex_shader = self.load_shader("vertex_shader.glsl")
        self.fragment_shader = self.load_shader("fragment_shader.glsl")

        # # Programma Shader
        # self.program = self.ctx.program(
        #     vertex_shader='''
        #     #version 330
        #     in vec2 in_vert;
        #     void main() {
        #         gl_Position = vec4(in_vert, 0.0, 1.0);
        #     }
        #     ''',
        #     fragment_shader='''
        #     #version 330
        #     uniform vec2 u_resolution;
        #     uniform vec3 color;
        #     out vec4 fragColor;
        #     void main() {

        #         vec2 st = gl_FragCoord.xy  / u_resolution;
        #         // st -= vec2(0.5);
        #         vec3 col = color ; //- vec3(st,0.0);

        #         float pct = 0.0;
        #         // // a. The DISTANCE from the pixel to the center
        #         pct = distance(st,vec2(0.5)) ;
        #         vec4 d = 2 * vec4(vec3(pct),0.0);
        #         fragColor = vec4(col, 1.0) - d;

        #         //fragColor = vec4(col, 1.0) ;
        #     }
        #     '''
        # )


        # Programma Shader
        self.program = self.ctx.program(vertex_shader=self.vertex_shader, fragment_shader=self.fragment_shader)



        # VBO per un quadrato pieno schermo
        self.vertices = self.ctx.buffer(np.array([
            -1., -1.,  # Vertice 1
             1., -1.,  # Vertice 2
            -1.,  1.,  # Vertice 3
             1.,  1.,  # Vertice 4
        ], dtype='f4').tobytes())

        self.vao = self.ctx.simple_vertex_array(self.program, self.vertices, 'in_vert')
        self.program['u_resolution'] = ( self.width, self.height)  # 

        # pyglet.clock.schedule_interval(lambda dt: self.on_draw(), 1/60.0)  # 60 FPS


    def get_file_mod_time(self):
        """Ottieni il timestamp di modifica del file shader."""
        try:
            return os.path.getmtime(self.fragment_shader_path)
        except FileNotFoundError:
            print(f"File {self.fragment_shader_path} non trovato.")
            return None



    def compile_shader(self):


        # Carica gli shader dai file
        self.vertex_shader = self.load_shader("vertex_shader.glsl")
        self.fragment_shader = self.load_shader("fragment_shader.glsl")

        """Compila o ricompila il fragment shader e aggiorna il programma."""
        try:
            # with open(self.fragment_shader_path, 'r') as f:
            #     fragment_shader = f.read()

            # Ricrea il programma
            self.program = self.ctx.program(
                vertex_shader=self.vertex_shader,
                fragment_shader=self.fragment_shader
            )

            # Ricrea il VAO con il nuovo programma
            # self.vao = self.ctx.simple_vertex_array(self.program, self.vbo, 'in_vert')
            self.vao = self.ctx.simple_vertex_array(self.program, self.vertices, 'in_vert')
            # print("Fragment shader ricaricato con successo.")
        except Exception as e:
            print(f"Errore nella compilazione del fragment shader: {e}")









    def on_draw(self):



        if self.Fone :
            print(self.Fone)
            self.Fone = False
            # Salva un frame con colore specificato
            self.save_frame(color=(1.0, 1.0, 0.0))  

        if self.F01:




            # self.vao = self.ctx.simple_vertex_array(self.program, self.vertices, 'in_vert')
            # self.program['u_resolution'] = ( self.width, self.height)  # 
            # self.F01 = False
        
            # print(time.time())    

            """Esegue il rendering sulla finestra."""
            self.clear()


            # self.compile_shader()
            # Controlla se il file shader è stato modificato
            current_mod_time = self.get_file_mod_time()
            if current_mod_time and current_mod_time != self.last_modified:
                print("Modifica rilevata nel fragment shader. Ricompilazione...")
                self.last_modified = current_mod_time
                self.compile_shader()



            self.program['u_resolution'] = (self.width, self.height)  # 

            self.ctx.clear(0.1, 0.1, 0.1)
            # self.ctx.screen.use()  # Ripristina il rendering sulla finestra principale
        
            # Aggiorna dinamicamente le uniform (esempio)
            t = pyglet.clock.get_default().time()        
            # self.program['color'] = ( math.fabs(np.sin(t/10)), 0.5, 0.5)  # Cambia colore
            self.program['color'] = ( 0.0, 0.0, 0.0)  # Cambia colore
            # self.program['u_resolution'] = ( self.width, self.height)  # Cambia colore
            
            self.vao.render(moderngl.TRIANGLE_STRIP)
            # self.ctx.wireframe = True


            # """Aggiorna dinamicamente il colore e disegna sulla finestra."""
            # self.clear()
            # self.ctx.screen.use()  # Ripristina il rendering sulla finestra principale
            # self.program['color'] = (np.sin(pyglet.clock.get_default().time()), 0.5, 0.8)
            # self.vao.render(moderngl.TRIANGLE_STRIP)
            
            pass
          

    def load_shader(self, file_path):
        """Carica il contenuto di uno shader da un file."""
        with open(file_path, 'r') as file:
            return file.read()

    def save_frame(self, color=(1.0, 0.0, 0.0)):



        # Crea una texture per immagazzinare il rendering
        self.texture = self.ctx.texture((4000,4000),4) # ((width, height), 4)
        self.program['u_resolution'] = ( 4000,4000) #self.width, self.height)  # 
        self.program['u_mouse'] = ( 2000, 2000) #self.width, self.height)  # 


        self.texture.filter = (moderngl.NEAREST, moderngl.NEAREST)

        # Framebuffer offscreen
        self.fbo = self.ctx.framebuffer(color_attachments=[self.texture])






        """Renderizza un singolo frame sulla framebuffer e salva come immagine."""
        # Aggiorna il colore dello shader
        # self.program['color'] = color
        # self.program['u_resolution'] = ( self.width, self.height)  # Cambia colore

        # Renderizza sulla framebuffer
        self.fbo.use()


        self.fbo.clear(0.0, 0.0, 0.0, 1.0)


        self.vao.render(moderngl.TRIANGLE_STRIP)
        # self.ctx.wireframe = True

        # Legge i dati della texture
        data = self.texture.read(alignment=1)



        image = Image.frombytes('RGBA', self.fbo.size, data)
        # image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Capovolge verticalmente

        # Salva l'immagine
        image.save("frame.png")
        print("Frame salvato come 'frame.png'")



        # # Salvataggio come "raw"
        # with open("output.raw", "wb") as f:
        #     f.write(data)
        # print("image in bytes salvato come 'output.png'")


        self.ctx.screen.use()  # Ripristina il rendering sulla finestra principale



    def on_key_press(self,symbol, modifiers):
        print(symbol)
        if symbol == pyglet.window.key.A :
            print('chiedo acquisizione frame con self.Ftone = True')
            self.F01= True
            self.dispatch_event('on_draw')            
            self.Fone = True
            self.dispatch_event('on_draw')            
        if symbol == pyglet.window.key.ESCAPE :
            print('fine programma')
            self.close()
        pass        


    def on_mouse_motion(self, x, y, dx, dy):
        # x,y,dx,dy = super().on_mouse_motion(x, y, dx, dy)
        self.program['u_mouse'] = (x,y)
        # print(x,y)
        return # super().on_mouse_motion(x, y, dx, dy)
        
    def on_mouse_press(self, x, y, button, modifiers):
        # print(button)
        self.program['u_center1'] = (x,y)
        return # super().on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.program['u_center2'] = (x,y)
        return #super().on_mouse_release(x, y, button, modifiers)

if __name__ == "__main__":
    # window = FramebufferExample(3840>>1, 2160>>1)
    # window = FramebufferExample(960, 1080)
    window = FramebufferExample(800, 800)

    # Salva un frame con colore specificato
    # window.save_frame(color=(0.0, 1.0, 0.0))


    # Esegui il programma
    pyglet.app.run()
