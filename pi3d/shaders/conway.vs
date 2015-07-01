#include std_head_vs.inc

varying vec2 pix_inv;

void main(void) {
  pix_inv = vec2(1.0, 1.0) / (unif[15].xy + vec2(+0.5, +0.5)); // do this division once per vertex as slow per pixel
  gl_Position = vec4(vertex, 1.0);
}
