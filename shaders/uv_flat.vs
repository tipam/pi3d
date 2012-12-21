precision highp float;

attribute vec3 vertex;
attribute vec3 normal;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix;
uniform mat4 cameraviewmatrix;

varying vec2 texcoordout;
varying float dist;

void main(void) {
  vec4 relPosn = modelviewmatrix * vec4(vertex,1.0);
  dist = length(relPosn);
  texcoordout = texcoord;
  gl_Position = relPosn;
}
