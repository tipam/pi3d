precision highp float;

attribute vec3 vertex;

uniform mat4 modelviewmatrix[2]; // 0 model movement in real coords, 1 in camera coords
uniform vec3 unif[16];
//uniform vec2 (w, h, full_h) => unif[15]

varying vec2 pix_inv;

void main(void) {
  pix_inv = vec2(1.0, 1.0) / (vec2(unif[15]) + vec2(0.0, 0.0)); // do this division once per vertex as slow per pixel
  gl_Position = modelviewmatrix[1] * vec4(vertex, 1.0);
}
