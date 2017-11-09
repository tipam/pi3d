#include std_head_vs.inc

varying vec2 texcoordout;

void main(void) {
  texcoordout = texcoord * unib[2].xy + unib[3].xy;
  texcoordout.y = 1.0 - texcoordout.y;
  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
}
