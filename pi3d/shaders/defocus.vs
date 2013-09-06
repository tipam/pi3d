precision highp float;

attribute vec3 vertex;

uniform mat4 modelviewmatrix[2]; // 0 model movement in real coords, 1 in camera coords

varying float dist;

void main(void) {
  gl_Position = modelviewmatrix[1] * vec4(vertex, 1.0);
  dist = gl_Position.z;
  gl_Position.z -= 0.01; // move a tiny bit nearer so it overwrites a non-blurred version
}
