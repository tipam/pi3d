precision highp float;

attribute vec3 vertex;
attribute vec3 normal;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix[2]; // 0 model movement in real coords, 1 in camera coords
uniform vec3 unib[3];
//uniform vec2 umult, vmult => unib[2]
uniform vec3 unif[16];
//uniform vec3 eye > unif[6]

varying vec2 texcoordout;
varying float dist;

void main(void) {
  vec4 relPosn = modelviewmatrix[0] * vec4(vertex,1.0);
  vec3 inray = vec3(relPosn - vec4(unif[6], 0.0)); // ----- vector from the camera to this vertex
  dist = length(inray);
  texcoordout = texcoord * vec2(unib[2][0], unib[2][1]);
  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
}
