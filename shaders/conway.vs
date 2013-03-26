precision highp float;

attribute vec3 vertex;

uniform vec3 unif[16];
//uniform vec3 (w, h, full_h) => unif[15]

varying vec2 pix_inv;

void main(void) {
  pix_inv = vec2(1.0, 1.0) / (unif[15].xy + vec2(-1.0, -1.0)); // do this division once per vertex as slow per pixel
  gl_Position = vec4(vertex, 1.0);
}
