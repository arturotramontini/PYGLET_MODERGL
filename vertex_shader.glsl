
// #version 330
// in vec3 in_vert; // Posizione del vertice
// uniform vec3 offset;
// void main() {
//     gl_Position = vec4(in_vert + offset, 1.0);
// }

#version 330
uniform mat4 mvp;  // Matrice di trasformazione
in vec2 in_vert;
void main() {
    gl_Position = mvp * vec4(in_vert, 0.0, 1.0);
}
