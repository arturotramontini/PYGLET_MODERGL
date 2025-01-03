
# https://chatgpt.com/c/675d4d29-3254-8002-98bb-cabbac69385b


import moderngl
import pyglet
import pyglet.window.key
import numpy as np
from PIL import Image

from pyrr import Matrix44

import math
import time
import os

os.system('clear')

class FramebufferExample(pyglet.window.Window):
    def __init__(self, width, height):


        self.niter = 1
        self.niterP = 0
        self.Fnumber = False

        super().__init__(width=width, height=height, caption="Framebuffer Example",vsync=False)


        self.sLabel1 = 'ciipo...HH..0123456789,37 X   ||| H|H|.:;-+@#'
        # Creazione della label per il testo
        self.label1 = pyglet.text.Label( self.sLabel1, #'Hello', 
                                    #   font_name='Arial', 
                                      font_name="Latin Modern Mono Prop",
                                      font_size=18, 
                                    #   x=self.width//2, y=self.height//2,
                                      x=0, y=self.height,
                                      anchor_x='left', anchor_y='top')
                                    #   anchor_x='center', anchor_y='center')



        # --- per ricaricare fragment_shader quando lo modicico 
        # Path al fragment shader
        self.fragment_shader_path = "fragment_shader.glsl"

        # Timestamp di modifica iniziale
        self.last_modified = self.get_file_mod_time()
        # ------------


        self.set_location(0,900)

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
            -1, -1,  # Vertice 1
             1, -1,  # Vertice 2
            -1,  1,  # Vertice 3
             1,  1,  # Vertice 
        ], dtype='f4').tobytes())

        self.vao = self.ctx.simple_vertex_array(self.program, self.vertices, 'in_vert')
        self.program['u_resolution'] = ( self.width, self.height)  # 


        # Definisci i limiti della tua proiezione ortografica
        self.projection1 = Matrix44.orthogonal_projection(left=-1, right=1, bottom=-1, top=1, near=-1, far=1)
        self.angle = np.radians(90)  # Angolo in radianti
        self.rotation = Matrix44.from_z_rotation(self.angle)  # Rotazione attorno all'asse Y
        self.transformation = self.projection1 @ self.rotation




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


            self.program['u_niter'] = self.niter 

            self.program['u_resolution'] = (self.width, self.height)  # 

            self.ctx.clear(0.1, 0.1, 0.1)
            # self.ctx.screen.use()  # Ripristina il rendering sulla finestra principale
        
            # Aggiorna dinamicamente le uniform (esempio)
            t = pyglet.clock.get_default().time()        
            # self.program['color'] = ( math.fabs(np.sin(t/10)), 0.5, 0.5)  # Cambia colore
            self.program['color'] = ( 0.0, 0.0, 0.0)  # Cambia colore
            # self.program['u_resolution'] = ( self.width, self.height)  # Cambia colore

            self.program['mvp'].write(self.transformation.astype('f4').tobytes())
            
            self.vao.render(moderngl.TRIANGLE_STRIP)
            # self.ctx.wireframe = True


            # """Aggiorna dinamicamente il colore e disegna sulla finestra."""
            # self.clear()
            # self.ctx.screen.use()  # Ripristina il rendering sulla finestra principale
            # self.program['color'] = (np.sin(pyglet.clock.get_default().time()), 0.5, 0.8)
            # self.vao.render(moderngl.TRIANGLE_STRIP)

            self.sLabel1 = str(time.time())
            self.label1.text = str(self.niter)
            self.label1.draw()

            pass
          

    def load_shader(self, file_path):
        """Carica il contenuto di uno shader da un file."""
        with open(file_path, 'r') as file:
            return file.read()

    def save_frame(self, color=(1.0, 0.0, 0.0)):



        # Crea una texture per immagazzinare il rendering
        # self.texture = self.ctx.texture((16000, 13500),4) # ((width, height), 4)
        # self.program['u_resolution'] = ( 16000, 13500) #self.width, self.height)  # 
        # self.texture = self.ctx.texture((3200<<2, 2700<<2),4) # ((width, height), 4)
        # self.program['u_resolution'] = ( 3200<<2, 2700<<2) #self.width, self.height)  # 
        # self.texture = self.ctx.texture((3200, 2700),4) # ((width, height), 4)
        # self.program['u_resolution'] = (3200, 2700) #self.width, self.height)  # 
        # self.texture = self.ctx.texture((3840, 2160),4) # ((width, height), 4)
        # self.program['u_resolution'] = ( 3840, 2160) #self.width, self.height)  # 
        # self.texture = self.ctx.texture((3000>>0, 2000>>0),4) # ((width, height), 4)
        # self.program['u_resolution'] = ( 3000>>0, 2000>>0) #self.width, self.height)  # 
        # self.texture = self.ctx.texture((2400, 1900),4) # ((width, height), 4)
        # self.program['u_resolution'] = ( 2400, 1900) #self.width, self.height)  # 
        # self.texture = self.ctx.texture((2000, 2000),4) # ((width, height), 4)
        # self.program['u_resolution'] = (2000, 2000) #self.width, self.height)  # 
        self.texture = self.ctx.texture((14000, 14000),4) # ((width, height), 4)
        self.program['u_resolution'] = (14000, 14000) #self.width, self.height)  # 




        # self.program['u_mouse'] = ( 0, 0) #self.width, self.height)  # 


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
        image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Capovolge verticalmente

        # Salva l'immagine
        image.save("frame_02.png")
        print("Frame salvato come 'frame_02.jpg'")



        # # Salvataggio come "raw"
        # with open("output.raw", "wb") as f:
        #     f.write(data)
        # print("image in bytes salvato come 'output.png'")


        self.ctx.screen.use()  # Ripristina il rendering sulla finestra principale



    def on_key_press(self,symbol, modifiers):
        
        print(hex(modifiers), hex(symbol))

        if (symbol == pyglet.window.key.MOD_SHIFT):
            print('shift')
        if (symbol == pyglet.window.key.MOD_CTRL):
            print('ctrl')

        n = symbol-48
        if (n>=0) and (n<=9):
            self.niterP = self.niterP * 10 + n
            print(f'symbol:{symbol}, niterP: {self.niterP}  niter: {self.niter}')

        if symbol == pyglet.window.key.E :
            self.niter = self.niterP
            self.niterP = 0


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

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        print(x, y, scroll_x, scroll_y)
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        # x,y,dx,dy = super().on_mouse_motion(x, y, dx, dy)
        self.program['u_mouse'] = (x,y)
        print(2*(x-self.width/2)/self.width, 2*(y-self.height/2)/self.height)
        return # super().on_mouse_motion(x, y, dx, dy)
        
    def on_mouse_press(self, x, y, button, modifiers):
        # print(button)
        self.program['u_center1'] = (x,y)
        return # super().on_mouse_press(x, y, button, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.program['u_center2'] = (x,y)
        return #super().on_mouse_release(x, y, button, modifiers)



if __name__ == "__main__":


    w = 1000
    h = 1000

    # window = FramebufferExample(3840>>1, 2160>>1)
    # window = FramebufferExample(960, 1080)
    # window = FramebufferExample(1600,1350)
    # window = FramebufferExample(1600,1350)
    # window = FramebufferExample(3200>>1,2700>>1)
    # window = FramebufferExample(2400>>1,1900>>1)
    # window = FramebufferExample(1000>>0,1428>>0)
    window = FramebufferExample(w,h)

    # Salva un frame con colore specificato
    # window.save_frame(color=(0.0, 1.0, 0.0))

    @window.event
    def on_move(x, y):
        print(f"La finestra è stata spostata a: ({x}, {y})")

    @window.event    
    def on_resize(width, height):
        print(f"La finestra è stata ridimensionata a: {width}x{height}")

    # Esegui il programma
    pyglet.app.run() 
