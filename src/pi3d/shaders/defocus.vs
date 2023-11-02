#include std_head_vs.inc

void main(void) {
  gl_Position = modelviewmatrix[1] * vec4(vertex, 1.0);
  dist = gl_Position.z;
#include std_fog_start.inc
  gl_Position.z -= 0.01; // move a tiny bit nearer so it overwrites a non-blurred version
}
