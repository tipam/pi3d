precision highp float;

attribute vec3 vertex;
attribute vec3 normal;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix;

varying float dist;

void main(void) {
  vec4 relPosn = modelviewmatrix * vec4(vertex,1.0);
  dist = length(relPosn);
  gl_Position = relPosn;
}
