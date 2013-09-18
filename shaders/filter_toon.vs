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

float width = 4.0; //charcoal line width

varying vec2 uv;
varying vec2 d;

void main(void) {
  uv = texcoord * unib[2].xy + unib[3].xy;
  uv.y = 1.0 - uv.y; // flip vertically
  d = vec2(width / unif[15][0], width / unif[15][1]);
  gl_Position = modelviewmatrix[1] * vec4(vertex,1.0);
}
