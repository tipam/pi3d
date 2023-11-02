#include std_head_vs.inc

varying vec2 pix_inv;

void main(void) {
  pix_inv = vec2(1.0, 1.0) / (vec2(unif[15]) + vec2(0.0, 0.0)); // do this division once per vertex as slow per pixel
  gl_Position = vec4(vertex, 1.0);
  gl_Position.z += unif[0][2];
  gl_PointSize = unib[2][2] / gl_Position.z;
}
