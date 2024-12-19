import pyglet
import moderngl
import numpy as np


class PygletModernglGrid(pyglet.window.Window):

    def __init__(self, width, height, grid_width, grid_height):
        super().__init__(width=width,
                         height=height,
                         caption="Grid with TRIANGLE_STRIP")

        # Creazione del contesto ModernGL
        self.ctx = moderngl.create_context()

        # Generazione della griglia
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.vertices = self.create_grid()

        # Creazione del Vertex Buffer Object (VBO)
        self.vbo = self.ctx.buffer(self.vertices.tobytes())

        # Shader per il riempimento
        self.fill_program = self.ctx.program(vertex_shader='''
            #version 330
            in vec3 in_vert;
            in vec3 in_color;
            out vec3 vert_color;                                             
            void main() {
                gl_Position = vec4(in_vert, 1.0);
                vert_color = in_color;
            }
            ''',
                                             fragment_shader='''
            #version 330
            in  vec3 vert_color;
            out vec4 fragColor;
            void main() {
                //fragColor = vec4(0.2, 0.06, 0.08, 1.0); // Colore di riempimento
                //fragColor = vec4(0.8, 0.6, 0.8, 1.0); // Colore di riempimento
                vec3 col = vert_color * 1.; // * 0.000001;
                col += 0 ; //vec3(.1,.1,.3);
                // vec3 col2 = vec3(0) + vec3(col.r * 1e-9,0.,0.);   
                fragColor = vec4(col,1.0);
            }
            ''')

        # Shader per il wireframe
        self.wireframe_program = self.ctx.program(vertex_shader='''
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
                fragColor = vec4(0.20, 1.0, 1.0, 1.0); // Colore wireframe bianco
            }
            ''')

        # Creazione del VAO per il riempimento
        self.fill_vao = self.ctx.simple_vertex_array(self.fill_program,
                                                     self.vbo, 'in_vert', 'in_color')
        # Creazione del VAO per il wireframe
        self.wireframe_vao = self.ctx.simple_vertex_array(
            self.wireframe_program, self.vbo, 'in_vert')

    def create_grid(self):
        """
        Crea i vertici della griglia come triangoli indipendenti.
        Ogni triangolo viene costruito a partire dai vertici della griglia.
        """
        grid_w = self.grid_width
        grid_h = self.grid_height

        # Calcolo della griglia in coordinate normalizzate (-1 a 1)
        x_vals = np.linspace(-.70, .70, grid_w + 1)
        y_vals = np.linspace(-.70, .70, grid_h + 1)

        vertices = []

        for y in range(grid_h):
            for x in range(grid_w):
                # Vertici del primo triangolo
                # Vertice in basso a sinistra
                vertices.append((x_vals[x], y_vals[y], 0.0, 0, 1, 0))
                
                # Vertice in basso a destra
                vertices.append((x_vals[x + 1], y_vals[y],0.0, 0, 1, 0))  
                
                # Vertice in alto a sinistra
                vertices.append((x_vals[x], y_vals[y + 1],0.0, 0, 1, 0))  

                # Vertici del secondo triangolo
                
                # Vertice in alto a sinistra
                vertices.append((x_vals[x], y_vals[y + 1], 0.0, 1,0,0))  
                
                # Vertice in basso a destra
                vertices.append((x_vals[x + 1], y_vals[y], 0.0, 1,0,0))  
                
                # Vertice in alto a destra
                vertices.append((x_vals[x + 1], y_vals[y + 1], 0.0, 1,0,0))  

        return np.array(vertices, dtype='f4')

    def on_draw(self):
        """Disegna la griglia con TRIANGLE_STRIP e wireframe."""
        self.clear()
        self.ctx.clear(0.01, 0.01, 0.1)  # Colore di sfondo

        # mia nota: è importante l'ordine di esecuzione
        # Durante il rendering, usa moderngl.TRIANGLES

        # POINTS) # LINE_LOOP) # POINTS) # TRIANGLES)
        self.fill_vao.render(moderngl.TRIANGLES)
        self.ctx.wireframe = False#True

        # self.wireframe_vao.render(moderngl.TRIANGLES)
        # self.ctx.wireframe = False


        new_color = np.array([1.0, 1.0, 1.0], dtype='f4')  # Colore aggiornato
        vertex_index = 2
        offset = vertex_index * 24 + 12
        self.vbo.write(new_color.tobytes(),offset)

        new_position = np.array([-1.0, -1.0, 0.0], dtype='f4')  # Posizione aggiornata
        offset = vertex_index * 24  # Inizio del vertice
        self.vbo.write(new_position.tobytes(), offset=offset)        




if __name__ == "__main__":
    window = PygletModernglGrid(600, 600, grid_width=2, grid_height=2)
    pyglet.app.run()
