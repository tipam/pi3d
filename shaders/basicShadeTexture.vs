attribute vec3 vertex;
attribute vec3 normal;
attribute vec2 texcoord;
uniform mat4 modelviewmatrix;
uniform mat4 normalsmatrix;
varying vec3 normout;
varying vec2 texcoordout;

void main(void) {
  normout=vec3 (modelviewmatrix * vec4(normal,0.0));
  texcoordout = texcoord;
  gl_Position = modelviewmatrix * vec4(vertex,1.0);
}
