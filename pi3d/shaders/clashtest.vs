precision lowp float;

attribute vec3 vertex;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix[2]; // 0 model movement in real coords, 1 in camera coords
uniform vec3 unib[3];
//uniform vec2 umult, vmult => unib[2]

varying vec2 texcoordout;
varying float dist;

void main(void) {
  texcoordout = texcoord * vec2(unib[2][0], unib[2][1]);
  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
  gl_Position.z += 0.001; // so properly shades version overwrites this
  dist = gl_Position.z;
}
