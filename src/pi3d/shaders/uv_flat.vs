#include std_head_vs.inc

varying vec2 texcoordout;

void main(void) {
  texcoordout = texcoord * unib[2].xy + unib[3].xy;
  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
  dist = gl_Position.z;
#include std_fog_start.inc
  gl_PointSize = unib[2][2] / dist;
}
