attribute vec3 vertex;
attribute vec3 normal;
attribute vec2 texcoord;
uniform mat4 modelviewmatrix;
varying vec2 texcoordout;

void main(void) {
  texcoordout = texcoord;
  gl_Position = modelviewmatrix * vec4(vertex,1.0);
}
