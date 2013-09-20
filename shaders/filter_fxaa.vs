precision highp float;

attribute vec3 vertex;
attribute vec2 texcoord;

uniform mat4 modelviewmatrix[2]; // 0 model movement in real coords, 1 in camera coords
uniform vec3 unib[4];
//uniform vec2 umult, vmult => unib[2]
//uniform vec2 u_off, v_off => unib[3]
uniform vec3 unif[20];
//w => unif[15][0] set in PostProcess to display size
//h => unif[15][1]

float delta = 1.0; // sample distance

varying vec2 uv;
varying vec2 dNW;
varying vec2 dNE;
varying vec2 dSW;
varying vec2 dSE;

void main(void) {
  uv = texcoord * unib[2].xy + unib[3].xy;
  uv.y = 1.0 - uv.y; // flip vertically
  dNW = vec2(-delta / unif[15][0], -delta / unif[15][1]);
  dNE = vec2(delta / unif[15][0], -delta / unif[15][1]);
  dSW = vec2(-delta / unif[15][0], delta / unif[15][1]);
  dSE = vec2(delta / unif[15][0], delta / unif[15][1]);
  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
}
