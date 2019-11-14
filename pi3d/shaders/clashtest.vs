#version 120
//precision mediump float;


attribute vec3 vertex;
attribute vec3 normal;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix[3]; // [0] model movement in real coords, [1] in camera coords, [2] camera at light
uniform vec3 unib[5];
uniform vec3 unif[20];

varying vec2 texcoordout;
varying float dist;

void main(void) {
  texcoordout = texcoord * vec2(unib[2][0], unib[2][1]);
  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
  gl_Position.z += 0.001; // so properly shades version overwrites this
  dist = gl_Position.z;
}
