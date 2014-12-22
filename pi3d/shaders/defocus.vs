#include std_head_vs.inc

varying float dist;

void main(void) {
  gl_Position = modelviewmatrix[1] * vec4(vertex, 1.0);
  dist = gl_Position.z;
  gl_Position.z -= 0.01; // move a tiny bit nearer so it overwrites a non-blurred version
}
