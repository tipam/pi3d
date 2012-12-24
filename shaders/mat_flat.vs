precision highp float;

attribute vec3 vertex;
attribute vec3 normal;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix[2]; // 0 model movement in real coords, 1 in camera coords
uniform vec3 unif[11];
//uniform vec3 eye > unif[6]

varying float dist;

void main(void) {
  vec4 relPosn = modelviewmatrix[0] * vec4(vertex,1.0);
  vec3 inray = vec3(relPosn - vec4(unif[6], 0.0)); // ----- vector from the camera to this vertex
  dist = length(inray);
  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
}
