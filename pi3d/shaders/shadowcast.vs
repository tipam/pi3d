#include std_head_vs.inc

varying vec2 texcoordout;
varying vec4 position;

void main(void) {
  texcoordout = texcoord * unib[2].xy + unib[3].xy;
  gl_Position = modelviewmatrix[2] * vec4(vertex, 1.0);
  position = gl_Position;
}
